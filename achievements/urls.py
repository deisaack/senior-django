from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'^apr/(?P<pk>[0-9]+)/$', views.AppraisalDetailView.as_view(), name='appraisal_detail'),
	url(r'^qn/(?P<pk>[0-9]+)/$', views.QuestionDetailView.as_view(), name='question_detail'),
	url(r'^$', views.AppraisalListView.as_view(), name='appraisal_list'),
	url(r'^qn/$', views.QuestionListView.as_view(), name='question_list'),
	url(r'^qn/create/$', views.QuestionCreateView.as_view(), name='question_create'),
	url(r'^qn/manage/$', views.manage_questions, name='manage_questions')
]
