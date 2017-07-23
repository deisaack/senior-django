from django.conf.urls import url, include
from django.contrib import admin
from achievements.views import review
from django.conf import settings
from django.conf.urls.static import static

# from achievements import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^review/$', review, name='review'),
    url(r'^appraisal/', include('achievements.urls', namespace='appraisal')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
