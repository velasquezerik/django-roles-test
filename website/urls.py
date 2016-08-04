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
    url(r'^admin/profile',views.admin_profile, name='admin_profile'),
    url(r'^admin/update',views.admin_profile_update, name='admin_profile_update'),
    url(r'^admin/users',views.admin_show_users, name="admin_show_users"),
    url(r'^admin/create',views.admin_create_user,name="admin_create_user"),
]
