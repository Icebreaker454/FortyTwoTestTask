from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from apps.personal_info.views import IndexView

urlpatterns = patterns(
    '',
    # Examples:
    url(r'^$', IndexView.as_view(), name='home'),

    url(r'^admin/', include(admin.site.urls)),
)
