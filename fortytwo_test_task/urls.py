from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin


from apps.personal_info.views import IndexView
from apps.personal_info.views import RequestsView
from apps.personal_info.views import PersonUpdateView
from apps.personal_info.views import LogInView
from apps.personal_info.views import LogOutView
from fortytwo_test_task.settings import common

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', IndexView.as_view(), name='home'),
    url(r'^requests/', RequestsView.as_view(), name='requests'),
    url(r'^update/', PersonUpdateView.as_view(), name='update'),
    url(r'^accounts/login/$', LogInView.as_view(), name='login'),
    url(r'^logout/', LogOutView.as_view(), name='logout'),

    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += static(
    common.MEDIA_URL, document_root=common.MEDIA_ROOT
)
