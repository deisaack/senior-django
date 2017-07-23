from django.contrib.auth.decorators import login_required
from .forms import ReviewForm, QuestionForm
from django.contrib import messages
from django.views.generic import DetailView, ListView, CreateView
from .models import Question, Employee, Appraisal
from django.conf import settings
from django.forms import formset_factory, modelformset_factory
from django.shortcuts import render, redirect

User = settings.AUTH_USER_MODEL

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.db import IntegrityError, transaction
from django.forms.formsets import formset_factory
from django.shortcuts import redirect, render
from .forms import LinkForm, BaseLinkFormSet, ProfileForm, FamilyMemberFormSet, QnForm
from .models import UserLink, Profile
from django.views.generic.edit import FormView
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin
from django.views import View


class AppraDisplay(DetailView):
    model = Appraisal
    template_name = 'achievements/form_detail.html'

    def get_context_data(self, **kwargs):
        context = super(AppraDisplay, self).get_context_data(**kwargs)
        context['form'] = QnForm()
        return context

class ApprFormView(SingleObjectMixin, FormView):
    template_name = 'achievements/form_detail.html'
    form_class = QnForm
    model = Question
    success_url = reverse_lazy()

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        self.object.save()
        return super(ApprFormView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return super(ApprFormView, self).form_valid(form)

    def get_success_url(self):
        return reverse('appraisal:question_detail', kwargs={'pk': self.object.pk})


class AppraDetail(View):

    def get(self, request, *args, **kwargs):
        view = AppraDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ApprFormView.as_view()
        return view(request, *args, **kwargs)


class QnView(FormView):
    template_name = 'achievements/qn_fm.html'
    success_url = '/appraisal/qn/'
    form_class = QnForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return super(QnView, self).form_valid(form)


class ProfileList(ListView):
    model = Profile


class ProfileFamilyMemberCreate(CreateView):
    model = Profile
    fields = ['first_name', 'last_name']
    success_url = reverse_lazy('appraisal:profile')

    def get_context_data(self, **kwargs):
        data = super(ProfileFamilyMemberCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['familymembers'] = FamilyMemberFormSet(self.request.POST)
        else:
            data['familymembers'] = FamilyMemberFormSet()
        return data


    def form_valid(self, form):
        context = self.get_context_data()
        familymembers = context['familymembers']
        with transaction.atomic():
            self.object = form.save()

            if familymembers.is_valid():
                familymembers.instance = self.object
                familymembers.save()
        return super(ProfileFamilyMemberCreate, self).form_valid(form)


@login_required
def profile_settings(request):
    """
    Allows a user to update their own profile.
    """
    user = request.user

    # Create the formset, specifying the form and formset we want to use.
    LinkFormSet = formset_factory(LinkForm, formset=BaseLinkFormSet)

    # Get our existing link data for this user.  This is used as initial data.
    user_links = UserLink.objects.filter(user=user).order_by('anchor')
    link_data = [{'anchor': l.anchor, 'url': l.url}
                    for l in user_links]

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, user=user)
        link_formset = LinkFormSet(request.POST)

        if profile_form.is_valid() and link_formset.is_valid():
            # Save user info
            user.first_name = profile_form.cleaned_data.get('first_name')
            user.last_name = profile_form.cleaned_data.get('last_name')
            user.save()

            # Now save the data for each form in the formset
            new_links = []

            for link_form in link_formset:
                anchor = link_form.cleaned_data.get('anchor')
                url = link_form.cleaned_data.get('url')

                if anchor and url:
                    new_links.append(UserLink(user=user, anchor=anchor, url=url))

            try:
                with transaction.atomic():
                    #Replace the old with the new
                    UserLink.objects.filter(user=user).delete()
                    UserLink.objects.bulk_create(new_links)

                    # And notify our users that it worked
                    messages.success(request, 'You have updated your profile.')

            except IntegrityError: #If the transaction failed
                messages.error(request, 'There was an error saving your profile.')
                return redirect(reverse('profile-settings'))

    else:
        profile_form = ProfileForm(user=user)
        link_formset = LinkFormSet(initial=link_data)

    context = {
        'profile_form': profile_form,
        'link_formset': link_formset,
    }

    return render(request, 'achievements/edit_profile.html', context)

def manage_questions(request):
    QuestionFormSet = modelformset_factory(Question, fields=['appraisal', 'title', 'description', 'rank'], extra=3)
    if request.method == 'POST':
        formset = QuestionFormSet(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
            return redirect('appraisal:profile_f')
    else:
        formset = QuestionFormSet()
    return render(request, 'achievements/question_formset.html', {'formset': formset})


@login_required
def review(request):
    user = request.user
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review.user = form.cleaned_data.get('user')
            review.question.title = form.cleaned_data.get('question')
            review.employe = request.user
            review.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Your review was successfully edited.')

    else:
        form = ReviewForm(instance=user, initial={
            'employee': user,
            })
    return render(request, 'achievements/review_add.html', {'form': form})


class QuestionDetailView(DetailView):
    model = Question
    template_name = 'achievements/qn_detail.html'

    def get_context_data(self, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        # context['user_list'] = User.objects.all()
        # context['appraisal_list'] = Appraisal.objects.all()
        return context


class QuestionListView(ListView):
    model = Question
    template_name = 'achievements/question_list.html'


class AppraisalDetailView(DetailView):
    model = Appraisal
    template_name = 'achievements/apr_detail.html'

    def get_context_data(self, **kwargs):
        context = super(AppraisalDetailView, self).get_context_data(**kwargs)
        # context['user_list'] = User.objects.all()
        context['question_list'] = Question.objects.filter(appraisal=self.kwargs['pk'])
        context['form'] = QnForm
        return context



class AppraisalListView(ListView):
    model = Appraisal
    template_name = 'achievements/appraisal_list.html'


# @parsleyfy
class QuestionCreateView(CreateView):
    model = Question
    fields = ['title', 'description','appraisal', 'rank', ]
    # template_name = 'achievements/new_.html'

# @parsleyfy
class AppraisalCreateView(CreateView):
    model = Appraisal
    fields = ['employee', 'superior', 'total']
    template_name = 'achievements/appraisal_form.html'

