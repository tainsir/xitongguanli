from django.conf.urls import url
from . import views

app_name = "user"

urlpatterns = [
    # ------------------- 用户登陆url  ----------------------------
    url(r'^login/$', views.login, name='login'),  # 用户登陆
    url(r'^login_out/$', views.login_out, name="login_out"),  # 用户退出

    # ------------------- 系统首页的url  ----------------------------
    url(r"^choice/$", views.choice, name="choice"),  # 选择用户和组织
    url(r'^starter/$', views.starter, name='starter'),  # 系统首页
    #---------------------搜索-------------------------------
    url(r"^search/$" , views.search , name = "search"),

    # ------------------- 用户CRUD的url  ----------------------------
    url(r'^user/$', views.show_all_user, name="show_all_user"),  # 点击用户进入用户界面
    url(r'^(?P<u_id>\d+)/user_details/', views.user_details, name="user_details"),  # 展示用户详情页面
    url(r'^add_user/$', views.add_user, name='add_user'),  # 新增用户
    url(r'^(?P<u_id>\d+)/edit_user/$', views.edit_user, name='edit_user'),  # 修改用户
    url(r'^(?P<u_id>\d+)/delete/$', views.delete, name='delete'),  # 删除用户


    # ------------------- 角色CRUD的url  ----------------------------
    url(r'^role/$', views.show_all_role, name='show_all_role'),  # 显示所有操作项和角色
    url(r'^new_role/$', views.new_role, name='new_role'),  # 新建角色
    url(r'^edit_role/(?P<rid>\d+)/$', views.edit_role, name='edit_role'),  # 编辑角色
    url(r'^del_role/$', views.del_role, name='del_role'),  # 删除(停用)角色

    #---------------------角色权限--------------------------------------
    url(r'^show_opeartion/$' , views.show_opeartion , name = "show_opeartion"),
    url(r'^show_role/$' , views.show_role , name = "show_role"),
]
