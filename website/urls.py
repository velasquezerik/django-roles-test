"""
    <GALATEA WEB: Web system simulations>
    Copyright (C) 2016  Erik Velasquez erikvelasquez.25@gmail.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
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
    url(r'^admin/logs_relations',views.admin_show_logs_relations, name="admin_show_logs_relations"),
    url(r'^admin/friends',views.admin_friends, name="admin_show_friends"),
    url(r'^admin/get_friends',views.admin_get_friends, name="admin_get_friends"),
    url(r'^admin/send/friend/(?P<user_id>[0-9]+)/$', views.admin_send_friend_request, name='admin_send_friend_request'),
    url(r'^admin/notifications_friends',views.admin_friends_notifications, name="admin_show_friends_notifications"),
    url(r'^admin/accept/friend/(?P<request_id>[0-9]+)/$', views.admin_accept_friend_request, name='admin_accept_friend_request'),
    url(r'^admin/denied/friend/(?P<request_id>[0-9]+)/$', views.admin_denied_friend_request, name='admin_denied_friend_request'),
    url(r'^admin/share_file',views.admin_share_file,name="admin_share_file"),
    url(r'^admin/notifications_share_files',views.admin_share_files_notifications, name="admin_show_share_files_notifications"),
    url(r'^admin/accept/share_files/(?P<request_id>[0-9]+)/$', views.admin_accept_share_files_request, name='admin_accept_share_files_request'),
    url(r'^admin/denied/share_files/(?P<request_id>[0-9]+)/$', views.admin_denied_share_files_request, name='admin_denied_share_files_request'),
    url(r'^admin/share/$', views.admin_folder_share_show, name='admin_show_share_folder'),
    url(r'^admin/share/file/(?P<file_id>[0-9]+)/$', views.admin_share_file_show, name='admin_share_show_file'),
    url(r'^admin/share_update',views.admin_update_share,name="admin_update_share"),
    url(r'^admin/permission/file/(?P<file_id>[0-9]+)/$', views.admin_file_permission_show, name='admin_permission_file'),
    url(r'^admin/permission/private/file/(?P<file_id>[0-9]+)/$', views.admin_permission_private_file, name='admin_permission_private_file'),
    url(r'^admin/permission/show/file/(?P<file_id>[0-9]+)/$', views.admin_permission_show_file, name='admin_permission_show_file'),
    url(r'^admin/permission/edit/file/(?P<file_id>[0-9]+)/$', views.admin_permission_edit_file, name='admin_permission_edit_file'),
    url(r'^admin/permission/share/private/file/(?P<file_id>[0-9]+)/$', views.admin_permission_share_private_file, name='admin_permission_share_private_file'),
    url(r'^admin/permission/share/show/file/(?P<file_id>[0-9]+)/$', views.admin_permission_share_show_file, name='admin_permission_share_show_file'),
    url(r'^admin/permission/share/edit/file/(?P<file_id>[0-9]+)/$', views.admin_permission_share_edit_file, name='admin_permission_share_edit_file'),
    url(r'^admin/result_create_file',views.admin_result_create_file,name="admin_result_create_file"),
    url(r'^admin/create_project',views.admin_create_project, name="admin_create_project"),
    url(r'^admin/new_integration',views.admin_new_integration, name="admin_new_integration"),
    url(r'^admin/execute_integration', views.admin_execute_integration, name='admin_execute_integration'),
    url(r'^admin/execute_parameter', views.admin_execute_parameter, name='admin_execute_parameter'),



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
    url(r'^user/friends',views.user_friends, name="user_show_friends"),
    url(r'^user/get_friends',views.user_get_friends, name="user_get_friends"),
    url(r'^user/send/friend/(?P<user_id>[0-9]+)/$', views.user_send_friend_request, name='user_send_friend_request'),
    url(r'^user/notifications_friends',views.user_friends_notifications, name="user_show_friends_notifications"),
    url(r'^user/accept/friend/(?P<request_id>[0-9]+)/$', views.user_accept_friend_request, name='user_accept_friend_request'),
    url(r'^user/denied/friend/(?P<request_id>[0-9]+)/$', views.user_denied_friend_request, name='user_denied_friend_request'),
    url(r'^user/share_file',views.user_share_file,name="user_share_file"),
    url(r'^user/notifications_share_files',views.user_share_files_notifications, name="user_show_share_files_notifications"),
    url(r'^user/accept/share_files/(?P<request_id>[0-9]+)/$', views.user_accept_share_files_request, name='user_accept_share_files_request'),
    url(r'^user/denied/share_files/(?P<request_id>[0-9]+)/$', views.user_denied_share_files_request, name='user_denied_share_files_request'),
    url(r'^user/share/$', views.user_folder_share_show, name='user_show_share_folder'),
    url(r'^user/share/file/(?P<file_id>[0-9]+)/$', views.user_share_file_show, name='user_share_show_file'),
    url(r'^user/share_update',views.user_update_share,name="user_update_share"),
    url(r'^user/permission/file/(?P<file_id>[0-9]+)/$', views.user_file_permission_show, name='user_permission_file'),
    url(r'^user/permission/private/file/(?P<file_id>[0-9]+)/$', views.user_permission_private_file, name='user_permission_private_file'),
    url(r'^user/permission/show/file/(?P<file_id>[0-9]+)/$', views.user_permission_show_file, name='user_permission_show_file'),
    url(r'^user/permission/edit/file/(?P<file_id>[0-9]+)/$', views.user_permission_edit_file, name='user_permission_edit_file'),
    url(r'^user/permission/share/private/file/(?P<file_id>[0-9]+)/$', views.user_permission_share_private_file, name='user_permission_share_private_file'),
    url(r'^user/permission/share/show/file/(?P<file_id>[0-9]+)/$', views.user_permission_share_show_file, name='user_permission_share_show_file'),
    url(r'^user/permission/share/edit/file/(?P<file_id>[0-9]+)/$', views.user_permission_share_edit_file, name='user_permission_share_edit_file'),
    url(r'^user/result_create_file',views.user_result_create_file,name="user_result_create_file"),
    url(r'^user/create_project',views.user_create_project, name="user_create_project"),

]
