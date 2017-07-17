from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm
from django.contrib import messages
from django.views.generic import DetailView
from .models import Question, Employee, Superior, Appraisal

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
