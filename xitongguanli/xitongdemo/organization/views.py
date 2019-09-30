from django.shortcuts import render, redirect, render_to_response , HttpResponse
from .models import Organization, Employee, TreeNode
from django.http import JsonResponse
from django.shortcuts import render
from user.views import menu_data , checkpower
from user.models import User, Role, Operation, Menu
# Create your views here.
from itertools import chain
from django.core import serializers
from django.db import connection
from helper import *
import json




def add(request):
    name = request.POST.get('name')
    number = request.POST.get('number')
    type = request.POST.get('type')
    repeat_name = Organization.objects.filter(name=request.POST.get('name'))
    if not repeat_name:
        all_data = Organization.objects.create(name=name, number=number,  type=type)
        all_data.save()
        return redirect('organization:dept_show')
    else:
        error = '组织已经存在'
        return render(request, 'organization/show_v2.html', {'err': error,'menu_list': menu_data(request.session['menu_id'])})

# 组织机构
def show_all_organization(request):
    return render_to_response('organization/show_all_organization.html',
                              {'categories_data': Organization.objects.filter(parent__isnull=True),'menu_list': menu_data(request.session['menu_id'])})


# 组织机构添加
def add_organization(request):
    if request.method == 'GET':
        oid = request.GET.get('oid');
       
        data = Organization.objects.filter(id=oid).first()
        return render(request, 'organization/add_organization.html', {'data': data,'menu_list': menu_data(request.session['menu_id'])})
    elif request.method == 'POST':  # 获取前端数据
        oid = request.GET.get('oid');
        name = request.POST.get('name')
        number = request.POST.get('number')
        type = request.POST.get('type')
        repeat_name = Organization.objects.filter(name=request.POST.get('name'))
        if not repeat_name:
            all_data = Organization.objects.create(name=name, number=number, parent_id=oid, type=type)
            all_data.save()
            return redirect('organization:dept_show')
        else:
            error = '组织已经存在'
            return render(request, 'organization/show_v2.html', {'err': error,'menu_list': menu_data(request.session['menu_id'])})

#组织机构删除
def delete_origaniza(request):
    oid = request.GET.get('oid');
    Organization.objects.filter(id=oid).delete()
    return redirect('organization:dept_show')


# 组织机构修改
def edit_organization(request):
    if request.method == 'GET':
        oid = request.GET.get('oid')
        print(oid)
        data = Organization.objects.filter(id=oid).first()
        number = Organization.objects.get(id=oid)
        return render(request, 'organization/edit_organization.html', {'data': data, 'number': number,'menu_list': menu_data(request.session['menu_id'])})
    elif request.method == 'POST':  # 获取前端数据
        oid = request.GET.get('oid')
        print('11111111111111')
        print(oid)
        name = request.POST.get('name')
        print(name)
        number = request.POST.get('number')
        all_data = Organization.objects.get(id=oid)
        if len(name) == 0 and len(number) == 0:
            error = '没有填写数据'
            data = Organization.objects.filter(id=oid).first()
            number = Organization.objects.get(id=oid)
            return render(request, 'organization/show_v2.html',
                          {'data': data, 'number': number, 'error': error,'menu_list': menu_data(request.session['menu_id'])})
        else:
            all_data.name = name
            all_data.number = number
            all_data.save()
        return redirect('organization:dept_show')

def all_organiza(request):
    data = []
    cursor = connection.cursor();
    sqlStr = "select * from organization_organization"
    cursor.execute(sqlStr)
    for row in cursor.fetchall():
        eledata = {
            'id':row[0],
            'name':row[1],
            'number':row[2],
            'type':row[3],
            'parent_id':row[4]
        }
        data.append(eledata)
    cursor.close()
    return HttpResponse(json.dumps( {'data':data}), content_type="application/json")



def show(request):
    menuid = request.GET.get("id")
    action = request.GET.get("action")
    power =  checkpower(menuid , request.session['login'] , request.session['role_id'])
    request.session['powerdata'] = power
    return render(request, "organization/show_v2.html" ,{'menu_list': menu_data(request.session['menu_id']) , 'action':action})






