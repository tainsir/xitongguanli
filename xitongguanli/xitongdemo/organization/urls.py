from django.conf.urls import url
from . import views
from . import views as dept_vies

app_name = "organization"
urlpatterns = [
    url(r'^edit_organization$' , views.edit_organization , name = "edit_organization"), #修改组织机构
    url(r'^add_organization$', views.add_organization, name='add_organization'),  # 添加组织机构
 
    url(r'^add/$' , views.add , name = "add"),#添加总公司

    url(r'^delete_origaniza/$' ,  views.delete_origaniza , name = "delete_origaniza"),
    url(r'^show/$', dept_vies.show, name='dept_show'),
    
    url(r'^all_organiza/$', dept_vies.all_organiza , name = "all_organiza"),
    
    ]
