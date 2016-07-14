from django.conf.urls import url
from . import views

app_name = 'website'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^test/$', views.test, name='test'),
    url(r'^admin/$', views.admin_view, name='admin_index'),
    url(r'^user/$', views.user_view, name='user_index'),
]
