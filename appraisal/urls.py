from django.conf.urls import url, include
from django.contrib import admin
from achievements.views import review
# from achievements import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^review/$', review, name='review'),
    url(r'^appraisal/', include('achievements.urls', namespace='appraisal')),
]