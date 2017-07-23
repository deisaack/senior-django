from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'^apr/(?P<pk>[0-9]+)/$', views.AppraisalDetailView.as_view(), name='appraisal_detail'),
	url(r'^apra/(?P<pk>[0-9]+)/$', views.AppraDetail.as_view(), name='aprr_detail'),
	url(r'^qn/(?P<pk>[0-9]+)/$', views.QuestionDetailView.as_view(), name='question_detail'),
	url(r'^$', views.AppraisalListView.as_view(), name='appraisal_list'),
	url(r'^q/fm/$', views.QnView.as_view(), name='qn_fm'),
	url(r'^qn/$', views.QuestionListView.as_view(), name='question_list'),
	url(r'^qn/create/$', views.QuestionCreateView.as_view(), name='question_create'),
	url(r'^a/create/$', views.AppraisalCreateView.as_view(), name='appraisal_create'),
	url(r'^qn/manage/$', views.manage_questions, name='manage_questions'),
	url(r'^qn/f/$', views.profile_settings, name='profile_settings'),
	url(r'^profile/$', views.ProfileList.as_view(), name='profile'),
	url(r'^profile/f/$', views.ProfileFamilyMemberCreate.as_view(), name='profile_f'),
]
