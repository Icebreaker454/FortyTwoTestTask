from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from apps.personal_info.views import IndexView
from apps.personal_info.views import RequestsView
from apps.personal_info.views import PersonUpdateView
from fortytwo_test_task.settings import common



urlpatterns = patterns(
    '',
    url(r'^$', IndexView.as_view(), name='home'),
    url(r'^requests/', RequestsView.as_view(), name='requests'),
    url(r'^update/', PersonUpdateView.as_view(), name='update'),

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
