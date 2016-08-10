from django.conf.urls import url
from . import views

app_name = 'website'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^test/$', views.test_folder, name='test'),

    #urls for admin
    url(r'^admin/$', views.admin_view, name='admin_index'),
    url(r'^admin/profile',views.admin_profile, name='admin_profile'),
    url(r'^admin/update',views.admin_profile_update, name='admin_profile_update'),
    url(r'^admin/users',views.admin_show_users, name="admin_show_users"),
    url(r'^admin/create_user',views.admin_create_user,name="admin_create_user"),
    url(r'^admin/user/(?P<user_id>[0-9]+)/$', views.admin_show, name='admin_show'),
    url(r'^admin/user/(?P<user_id>[0-9]+)/delete/$', views.admin_delete, name='admin_delete'),
    url(r'^admin/user/(?P<user_id>[0-9]+)/active/$', views.admin_active, name='admin_active'),
    url(r'^admin/create_admin',views.admin_create_admin,name="admin_create_admin"),
    url(r'^admin/edit/(?P<user_id>[0-9]+)/$', views.admin_edit, name='admin_edit_user'),
    url(r'^admin/password',views.admin_password, name='admin_password_update'),
    url(r'^admin/create_folder',views.admin_create_folder,name="admin_create_folder"),
    url(r'^admin/folder/(?P<folder_id>[0-9]+)/$', views.admin_folder_show, name='admin_show_folder'),
    url(r'^admin/edit_folder',views.admin_edit_folder,name="admin_edit_folder"),
    url(r'^admin/delete_folder',views.admin_delete_folder,name="admin_delete_folder"),
    url(r'^admin/create_file',views.admin_create_file,name="admin_create_file"),


    #urls for users
    url(r'^user/$', views.user_view, name='user_index'),
    url(r'^user/profile',views.user_profile, name='user_profile'),
    url(r'^user/update',views.user_profile_update, name='user_profile_update'),
    url(r'^user/password',views.user_password, name='user_password_update'),
    url(r'^user/create_folder',views.user_create_folder,name="user_create_folder"),
    url(r'^user/folder/(?P<folder_id>[0-9]+)/$', views.user_folder_show, name='user_show_folder'),
    url(r'^user/edit_folder',views.user_edit_folder,name="user_edit_folder"),
    url(r'^user/delete_folder',views.user_delete_folder,name="user_delete_folder"),
    url(r'^user/create_file',views.user_create_file,name="user_create_file"),

]
