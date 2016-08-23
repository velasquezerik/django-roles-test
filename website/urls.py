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
    url(r'^admin/upload_file',views.admin_upload_file,name="admin_upload_file"),
    url(r'^admin/file/(?P<file_id>[0-9]+)/$', views.admin_file_show, name='admin_show_file'),
    url(r'^admin/delete_file/(?P<file_id>[0-9]+)/$', views.admin_delete_file, name='admin_delete_file'),
    url(r'^admin/file_update',views.admin_update_file,name="admin_update_file"),
    url(r'^admin/compile/file/(?P<file_id>[0-9]+)/$', views.admin_compile_file, name='admin_compile_file'),
    url(r'^admin/execute/file/(?P<file_id>[0-9]+)/$', views.admin_execute_file, name='admin_execute_file'),
    url(r'^admin/move_folder',views.admin_move_folder,name="admin_move_folder"),
    url(r'^admin/move_file',views.admin_move_file,name="admin_move_file"),
    url(r'^admin/logs_files',views.admin_show_logs_files, name="admin_show_logs_files"),
    url(r'^admin/logs_folders',views.admin_show_logs_folders, name="admin_show_logs_folders"),
    url(r'^admin/friends',views.admin_friends, name="admin_show_friends"),


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
    url(r'^user/upload_file',views.user_upload_file,name="user_upload_file"),
    url(r'^user/file/(?P<file_id>[0-9]+)/$', views.user_file_show, name='user_show_file'),
    url(r'^user/delete_file/(?P<file_id>[0-9]+)/$', views.user_delete_file, name='user_delete_file'),
    url(r'^user/file_update',views.user_update_file,name="user_update_file"),
    url(r'^user/run_program',views.run_test,name="run_test"),
    url(r'^user/compile/file/(?P<file_id>[0-9]+)/$', views.user_compile_file, name='user_compile_file'),
    url(r'^user/execute/file/(?P<file_id>[0-9]+)/$', views.user_execute_file, name='user_execute_file'),
    url(r'^user/move_folder',views.user_move_folder,name="user_move_folder"),
    url(r'^user/move_file',views.user_move_file,name="user_move_file"),

]
