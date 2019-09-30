from django.db import models


# 新建一个行为表，用来定义点击菜单路由后出现的数据类型
# 如果为列表，则规定只显示新建和搜索按钮


class Menu(models.Model):
    """
    菜单表
    """
    title = models.CharField(max_length=10, verbose_name='菜单名称')
    order = models.IntegerField(blank=True, default=1, verbose_name='排序')
    is_active = models.SmallIntegerField(default=1, verbose_name='是否激活')
    created_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='最后更新时间', auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, verbose_name='父级菜单')
    url = models.URLField( verbose_name='路由')

    # 定义菜单间的自引用关系
    # 权限url 在 菜单下；菜单可以有父级菜单；还要支持用户创建菜单，因此需要定义parent字段（parent_id）
    # blank=True 意味着在后台管理中填写可以为空，根菜单没有父级菜单

    def __str__(self):
        # 显示层级菜单
        title_list = [self.title]
        p = self.parent
        while p:
            title_list.insert(0, p.title)
            p = p.parent
        return '-'.join(title_list)
    # join()中的sequence元素必须都为字符串，将其按照一定的连接符连接起来


class Operation(models.Model):
    """
    操作表
    """
    title = models.CharField(max_length=10, verbose_name='操作名称')
    url = models.URLField(blank=True, null=True, verbose_name='排序')
    is_active = models.SmallIntegerField(default=1, verbose_name='是否激活')
    created_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    menu = models.ForeignKey(Menu, null=True, blank=True)
    key = models.CharField(max_length=10,verbose_name='关键词')

    def __str__(self):
        # 显示带菜单前缀的权限
        return '{menu}---{permission}'.format(menu=self.menu, permission=self.title)


class Role(models.Model):
    """
    角色表
    """
    name = models.CharField(max_length=30, verbose_name='角色名称')
    is_select = models.SmallIntegerField(default=1, verbose_name='是否被选用')
    created_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='最后更新时间', auto_now_add=True)
    operations = models.ManyToManyField(Operation, verbose_name='操作')

    # 定义角色和权限的多对多关系

    def __str__(self):
        return self.name


class User(models.Model):
    """
    用户表
    """
    username = models.CharField(max_length=32, verbose_name='用户名称')
    password = models.CharField(max_length=64, verbose_name='密码')
    is_active = models.SmallIntegerField(default=1, verbose_name='是否激活')
    created_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='最后更新时间', auto_now_add=True)
    organization = models.ForeignKey('organization.Organization', blank=True, null=True, verbose_name='绑定员工')
    roles = models.ManyToManyField(Role, verbose_name='绑定角色')

    # 定义用户和角色的多对多关系

    def __str__(self):
        return self.username
