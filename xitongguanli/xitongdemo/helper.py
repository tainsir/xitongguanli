# from redis import Redis
from django.db import connection
from user.models import * 
from organization.models import *
from django.conf import settings
# from django.core.cache import cache
import json


# rds = Redis(host='127.0.0.1' , port = 6379);


def checkpower(menuid ,username, roleid ):
    powerdata = []
    cursor = connection.cursor()
    sqlStr = "SELECT e.url , e.title , e.key FROM user_role AS a , user_user AS b , user_user_roles AS c ,user_role_operations AS d , user_operation AS e WHERE a.id = c.role_id AND b.id = c.user_id AND a.id = d.role_id AND d.operation_id = e.id AND b.username = '%s' AND e.menu_id ='%s' AND  a.id = '%s'"%(username,menuid,roleid)
    cursor.execute(sqlStr)
    for row in cursor.fetchall():
        data = {
            'key':row[2],
            'url':row[0],
            'title':row[1]
        }
        powerdata.append(data)
  
    cursor.close()
    return powerdata


def menu_data(menu_id):
    #menu_id为可以访问到的目录
    if menu_id == []:#若为空，则不展示任何菜单
        menu_list = Menu.objects.none()  
        return chain(menu_list)
    else:
        all_actor = Menu.objects.none()
        menu_list = []
        for i in menu_id: 
            menu = Menu.objects.get(id = i)
            menu_list.append(menu)
        for  menu in menu_list:
            if menu.parent == None:
                pass
            else:
                if menu.parent.parent == None:
                    menu_list.append(menu.parent)
                else:
                    menu_list.append(menu.parent.parent)
        menu_list = list(set(menu_list))
        return menu_list


# def read(menuid):
#     keystr = "menuid"
#     key = '%s%s'%(keystr , menuid)
#     print(key)
#     value = cache.get(key)
#     print(value)
#     if value == None:
#          data = None
#     else:
#         data = json.loads(value)
#     return data
# ////////////////////////////////////////////////////////////////////  
# //                            _ooOoo_                             //  
# //                           o8888888o                            //      
# //                           88" . "88                            //      
# //                           (| -_- |)                            //      
# //                           O\  =  /O                            //  
# //                        ____/`---'\____                         //                          
# //                      .'  \\|     |//  `.                       //  
# //                     /  \\|||  :  |||//  \                      //      
# //                    /  _||||| -:- |||||-  \                     //  
# //                    |   | \\\  -  /// |   |                     //  
# //                    | \_|  ''\---/''  |   |                     //          
# //                    \  .-\__  `-`  ___/-. /                     //          
# //                  ___`. .'  /--.--\  `. . ___                   //      
# //                ."" '<  `.___\_<|>_/___.'  >'"".                //  
# //              | | :  `- \`.;`\ _ /`;.`/ - ` : | |               //      
# //              \  \ `-.   \_ __\ /__ _/   .-` /  /               //  
# //        ========`-.____`-.___\_____/___.-`____.-'========       //      
# //                             `=---='                            //  
# //        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^      //  
# //         佛祖保佑       永无BUG        永不修改                    //  
# ////////////////////////////////////////////////////////////////////  