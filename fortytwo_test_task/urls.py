from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from apps.personal_info.views import IndexView
from fortytwo_test_task.settings import common

urlpatterns = patterns(
    '',
    # Examples:
    url(r'^$', IndexView.as_view(), name='home'),

    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns(
    '',
    url(
        r'^static/(?P<path>.*)$',
        'django.views.static.serve',
        {
            'document_root': common.MEDIA_ROOT,
            'show_indexes': True
        }
    ),
)
