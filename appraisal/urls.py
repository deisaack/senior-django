from django.conf.urls import url
from django.contrib import admin
from achievements.views import review
from achievements import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^review/$', review, name='review'),
    url(r'^(?P<pk>[0-9]+)/$', views.QuestionDetailView.as_view(), name='supply-detail'),

]