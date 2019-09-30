from django.shortcuts import render, redirect ,reverse
from .models import User, Role, Operation, Menu
from organization.models import Organization
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render_to_response 
from django.db import connection
from django.core import serializers
import json
from itertools import chain
import split
from helper import *
from django.views.decorators.cache import cache_page
# ------------------------首页------------------




# 首页
def starter(request):

    return render(request, 'user/starter.html', {'menu_list': menu_data(request.session['menu_id'])})


# ------------------------用户------------------

# 用户登陆
def login(request):
    if request.method == "GET":
        return render(request, "user/login.html")
    elif request.method == "POST":
        # 获取用户数据
        username = request.POST["username"]
        password = request.POST["password"]
        # 从数据库中查询数据是否存在
        user_obj = User.objects.filter(username=username, password=password).first()
        # print(user_obj)


        # 判断账户名密码是否正确
        if not user_obj:
            return render(request, "user/login.html", {"error": '用户名或密码错误'})
        else:
            
            # 登陆成功跳转到选择角色的页面
            request.session["login"] = user_obj

            return redirect('user:choice')



# 选择角色和组织

def choice(request):
    if request.method == "GET":
        # 从数据库中查询角色和组织机构信息， 展示到前端,供登录用户选择。
        # 获取用户
        user = request.session.get('login')
        role_list = user.roles.all()
        # request.session["allrole"] = role_list
        # organization_list = Organization.objects.filter(parent=user.organization)
        return render(request, "user/choice.html", {"role_list": role_list})
    elif request.method == "POST":
        # 获取登录客户选择的数据，从数据库中读取需要展示的数据
        role_id = request.POST['role_id'] # 根据用户选择的角色，可以决定用户拥有的操作权限
        role = Role.objects.get(id=role_id) # 获取选择的角色
        request.session["role_id"] = role_id
        request.session['role'] = role
        # organization_id = request.POST['organization_id']  # 根据用户选择的部门，可以展示该分公司下的数据信息
        # organization = Organization.objects.get(id=organization_id)
        # request.session["organization"] = organization
        # 角色和部门都已经确定，由此可以确定首页展示的数据
        userdata = []
        keydata = []
        cursor = connection.cursor()
    #从角色，用户及其中间表中取他们相对应的关系
        cursor.execute("SELECT * FROM user_role AS a , user_user AS b , user_user_roles AS c ,user_role_operations AS d , user_operation AS e WHERE a.id = c.role_id AND b.id = c.user_id AND a.id = d.role_id AND d.operation_id = e.id AND b.username = '%s' AND a.id ='%s' "%( request.session["login"],request.session["role_id"]))
        for row in cursor.fetchall():
            usertable = {
                'menu_id':row[22],
                'key':row[21],
                'url':row[24 ]
            }
            
            userdata.append(usertable)   
        cursor.close()
        request.session['menu'] = userdata
        menudata = []
        for i in userdata:
            menudata.append(i['menu_id'])
        print(menudata)
        request.session['menu_id'] = menudata
        return redirect('user:starter')

# 用户退出
def login_out(request):
    #     清除session缓存
    request.session.flush()
    #     跳转至登录页面
    return redirect('/user/login/')

#查看角色
def show_role(request):
    # print(request.body)
    user_id = request.GET.get('user_id')
    # print(user_id)
    roledata = []
    cursor = connection.cursor()
    #从角色，用户及其中间表中取他们相对应的关系
    cursor.execute("SELECT * FROM user_role AS a , user_user AS b , user_user_roles AS c  WHERE a.id = c.role_id AND b.id = c.user_id AND b.id = '%s' "%user_id)
    for row in cursor.fetchall():
        roletable = {
            'role_name':row[1]
        }
        roledata.append(roletable)   
    cursor.close()
    # print(roledata)
    return HttpResponse(json.dumps({"status":"ok" , "data":roledata}) , content_type="application/json");





# 用户
def show_all_user(request):
    # 查询所有用户
    if request.method == "GET":
        action = request.GET.get("action")
        menuid = request.GET.get("id")
        
    power =  checkpower(menuid , request.session['login'] , request.session['role_id'])
    request.session['powerdata'] = power
    # a = read(menuid)
    # print(a)
    # 实例化结果集, 每页15条， 少于2条合并到上一页
    # a = test(menuid , request.session['role_id'] , request.session['login'])
   

    alluser =[]
    cursor = connection.cursor()
  
    cursor.execute('SELECT * FROM  user_user ')
     
    for row in cursor.fetchall():
        usertable = {
            'id':row[0],
            'username':row[1],
            'created_at':str(row[4]),
            'is_active':row[3],
        }
        alluser.append(usertable)
    # print(sb)    
    cursor.close()
    paginator = Paginator(alluser, 10)
    # 网页中的page值
    page = request.GET.get("page")
    # print(sb)
    try:
        # 传递HTML当前页对象
        alluser = paginator.page(page)
    except PageNotAnInteger:
        alluser = paginator.page(1)
    except EmptyPage:
        alluser = paginator.page(paginator.num_pages)
    
    
    return render(request, "user/show_all_user.html", {'alluser':alluser, 'menu_list': menu_data(request.session['menu_id']) , 'action':action , 'id':menuid})


# 展示用户详情
def user_details(request, u_id):
    # 查询用户信息
    user = User.objects.filter(id=u_id).first()
    # 查询组织机构信息
    organization = Organization.objects.all()
    # 查询组织机构表中的父ID
    organization_id = Organization.objects.filter(id=user.organization_id).first()
    print(organization_id)
    if organization_id.parent_id == None:
        role_obj = User.objects.filter(id=u_id).first()
        role_list = role_obj.roles.all()
        return render(request, "user/user_details.html",
                      {"user": user, "role_list": role_list, 'menu_list': menu_data(request.session['menu_id']), \
                                                         'organization': organization})
    else:
        parent_id = organization_id.parent.id
        # print(organization_id.type)
        # print("父id：%s" % parent_id)
        if organization_id.type > 2:
            # 遍历所有的组织
            for x in organization:
                # 判断父id属于哪个组织
                if parent_id == x.id and x.parent_id != None:
                    organizations = x.name
                
                    for u in organization:
                        # 判断上层父ID属于哪个组织
                        if x.parent_id == u.id:
                            or_id = u.name

            # 查询用户对应角色的信息
            # 多对多表查询
            role_obj = User.objects.filter(id=u_id).first()
            role_list = role_obj.roles.all()
            return render(request, "user/user_details.html", {"user": user, "role_list": role_list, 'menu_list': menu_data(request.session['menu_id']), \
                                                              'or_id': or_id, 'organizations': organizations})
        else:
            role_obj = User.objects.filter(id=u_id).first()
            role_list = role_obj.roles.all()
            return render(request, "user/user_details.html", {"user": user, "role_list": role_list, 'menu_list': menu_data(request.session['menu_id'])})



# 新增用户
def add_user(request):
    if request.method == "GET":
        # 查找角色所有数据
        role_list = Role.objects.all()
        return render(request, "user/add_user.html", {"role_list": role_list, 'menu_list': menu_data(request.session['menu_id'])})
    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        role = request.POST.getlist("role_id")
        # 创建并保存到数据库
        user = User.objects.filter(username=username)
        if user:
            error = '账户已存在'
            return render(request, "user/add_user.html", {'error': error})
        else:
            user = User.objects.create(username=username, password=password)
            user.save()
            user.roles.add(*role)
            return render(request, 'user/add_user.html', {'msg': '添加成功' , 'menu_list':menu_data(request.session['menu_id'])})


# 修改用户
def edit_user(request, u_id):
    if request.method == "GET":
        user = User.objects.get(id=u_id)
        # 查询所有用户
        user_list = User.objects.all()
        # 查找角色所有数据
        role_list = Role.objects.all()
        user_id = u_id
        cursor = connection.cursor()
        cursor.execute("SELECT is_active FROM user_user  WHERE id = '%s'"%user_id)
        is_active= cursor.fetchall()
         
        cursor.close()
        # print(is_active[0][0])
        return render(request, "user/edit_user.html", {'pression':is_active[0][0] ,"role_list": role_list, 'user': user, "user_list": user_list, "menu_list": menu_data(request.session['menu_id'])})
    elif request.method == "POST":
        # 通过ID找到到要修改的数据
        print(request.POST)
        user = User.objects.filter(id=u_id).first()
        # 修改数据
        user.username = request.POST["username"]
        user.password = request.POST["password"]
        user.is_active = request.POST["is_active"]
        # 获取修改的角色
        role = request.POST.getlist("role_id")
        # 清楚原来的信息
        user.roles.clear()
        # 更新数据
        user.save()
        # 增加关联的角色
        user.roles.add(*role)
        return redirect('user:show_all_user')



# 删除用户
def delete(request, u_id):
    # 从数据库中查询要删除的用户
    user = User.objects.filter(id=u_id).first()
    # 改变用户状态为不活动
    user.is_active = 0
    # 更新到数据库
    user.save()
    # alluser =[]
    # cursor = connection.cursor()
  
    # cursor.execute('SELECT * FROM user_role AS a , user_user AS b , user_user_roles AS c  WHERE a.id = c.role_id AND b.id = c.user_id')
     
    # for row in cursor.fetchall():
    #     usertable = {
    #         'id':row[5],
    #         'username':row[6],
    #         'is_select':row[2],
    #         'name':row[1],
    #         'created_at':str(row[3]),
    #         'is_active':row[8],
    #     }
    #     alluser.append(usertable)
    # # print(sb)    
    # cursor.close()
    # paginator = Paginator(alluser, 10)
    # # 网页中的page值
    # page = request.GET.get("page")
    # # print(sb)
    # try:
    #     # 传递HTML当前页对象
    #     alluser = paginator.page(page)
    # except PageNotAnInteger:
    #     alluser = paginator.page(1)
    # except EmptyPage:
    #     alluser = paginator.page(paginator.num_pages)
    # return render(request, "user/show_all_user.html", {'alluser':alluser, 'menu_list': menu_data() })
    return redirect('user:show_all_user')



# 查看用户信息
def check_all_user(request):
    user_list = User.objects.all()
    # print(user_list)
    return render(request, "user/show_all_user.html", {"user_list": user_list, "menu_list": menu_data(request.session['menu_id'])})


# 搜索用户  还没有前端网页
def search(request):
    data = str(request.body , encoding = "utf-8")
    keydata = data.split("=")
    if keydata[0] == 'table_user':
        key = request.POST["table_user"]
        userdata = User.objects.filter(username = key)
        return render(request ,'user/show_all_user.html' , {"alluser":userdata , "menu_list":menu_data(request.session['menu_id'])} )
    if keydata[0] == 'table_role':   
        key = request.POST["table_role"]
        print(key)
        userdata = Role.objects.filter(name = key)
        return render(request ,'user/show_all_role.html' , {"all_role":userdata , "menu_list":menu_data(request.session['menu_id'])} ) 

# 导出excel
def derive_excel(request, u_id):
    pass


# ------------------------角色------------------

# 展示所有角色
def show_all_role(request):
    if request.method == "GET":
        action = request.GET.get("action")
        menuid = request.GET.get("id")
    power =  checkpower(menuid , request.session['login'] , request.session['role_id'])
    request.session['powerdata'] = power
   
    # roledata = []
    # cursor = connection.cursor()
  
    # cursor.execute('SELECT * FROM user_role AS a , user_role_operations AS b , user_operation AS c WHERE a.id = b.role_id AND c.id = b.operation_id ')
     
    # for row in cursor.fetchall():
    #     roletable = {
    #         'name':row[2],
    #         'operation_id':row[7]
    #     }
    #     roledata.append(roletable)
    # # print(sb)    
    # cursor.close()
    all_role = Role.objects.all()

    paginator = Paginator(all_role, 10)
    # 网页中的page值
    page = request.GET.get("page")
    try:
        # 传递HTML当前页对象
        all_role = paginator.page(page)
    except PageNotAnInteger:
        all_role = paginator.page(1)
    except EmptyPage:
        all_role = paginator.page(paginator.num_pages)
    
    # associated = user_roles.all()
    return render(request, 'user/show_all_role.html', {'all_role': all_role, "menu_list": menu_data(request.session['menu_id']) , "action":action ,"id":id})


# 新建角色
def new_role(request):
    if request.method == 'GET':
        operation_data = Operation.objects.all()
        return render(request, 'user/new_role.html', {'operation_data': operation_data, "menu_list": menu_data(request.session['menu_id'])})
    elif request.method == 'POST':  # 获取前端数据
        username = request.POST.get('username')
        is_select = request.POST.get('is_select')
        operation_id = request.POST.getlist('operation_id')
        repeat_username = Role.objects.filter(name=username)
        if not repeat_username:  
            all_data = Role.objects.create(name=username, is_select=is_select)
            all_data.operations.add(*operation_id)
            return redirect('user:show_all_role')    
        else:
            error = '角色已经存在'
            return render(request, 'uesr/new_role.html', {'err': error})


# 编辑角色信息
def edit_role(request, rid):
    if request.method == "GET":
        role_id = rid
        role = Role.objects.filter(id=rid).first()
        operation_list = Operation.objects.all()
        cursor = connection.cursor()
        cursor.execute("SELECT is_select FROM user_role  WHERE id = '%s'"%role_id)
        is_select= cursor.fetchall()#取出此角色是否被启用
        cursor.close()
      
        return render(request, 'user/edit_role.html', {'pression':is_select[0],'role': role, 'operation_list': operation_list, "menu_list": menu_data(request.session['menu_id'])})
    elif request.method == "POST":
        username = request.POST.get('name')
        is_select = request.POST.get('is_select')
        operation_id = request.POST.getlist('operation_id')
        all_data = Role.objects.get(id=rid)
        all_data.name = username
        all_data.is_select = is_select
        all_data.save()
        all_data.operations.clear()
        all_data.operations.add(*operation_id)
        return redirect('user:show_all_role')


# 停用角色
def del_role(request):
    role_id = request.GET.get('nid')
    Role.objects.filter(id=role_id).delete()
    return redirect('user:show_all_role')
#查询权限
def show_opeartion(request):
    role_id = request.GET.get('role_id')
    roledata = []
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_role AS a , user_role_operations AS b , user_operation AS c ,user_menu AS d WHERE  d.id =c.menu_id AND  a.id = b.role_id AND c.id = b.operation_id AND a.id = '%s' "%role_id)
    for row in cursor.fetchall():
        roletable = {
            'operation_id':row[7],
            'title':row[9],
            'menu':row[16],
        }
        roledata.append(roletable)   
    cursor.close()
    # print(roledata)
    return HttpResponse(json.dumps({"status":"ok" , "data":roledata}) , content_type="application/json");