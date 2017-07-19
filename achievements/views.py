from django.contrib.auth.decorators import login_required
from .forms import ReviewForm, QuestionForm
from django.contrib import messages
from django.views.generic import DetailView, ListView, CreateView
from .models import Question, Employee, Appraisal
from django.conf import settings
from django.forms import formset_factory, modelformset_factory
from django.shortcuts import render, redirect

User = settings.AUTH_USER_MODEL

def manage_questions(request):
    QuestionFormSet = formset_factory(QuestionForm, extra=3)
    if request.method == 'POST':
        formset = QuestionFormSet(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
            return redirect('products_list')
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
        return context

class AppraisalListView(ListView):
    model = Appraisal
    template_name = 'achievements/appraisal_list.html'


class QuestionCreateView(CreateView):
    model = Question
    fields = ['title', 'description','appraisal', 'rank', ]
    # template_name = 'achievements/new_.html'

class AppraisalCreateView(CreateView):
    model = Appraisal
    fields = ['employee', 'superior', 'total']
    template_name = 'supply/new_supply.html'

