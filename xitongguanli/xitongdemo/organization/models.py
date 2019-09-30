from django.db import models

# Create your models here.


class Organization(models.Model):
    """
    组织机构表
    """
    name = models.CharField(max_length=30, verbose_name='组织机构名称')
    number = models.CharField(max_length=10, unique=True, default=1001, verbose_name='机构代码')
    parent = models.ForeignKey('self', related_name='categories',  null=True)  # 上级
    type = models.IntegerField(verbose_name='公司/分公司/部门/职务')

    def __str__(self):
        return self.name


class Employee(models.Model):
    """
    人员表
    """
    name = models.CharField(max_length=30, verbose_name='员工姓名')
    number = models.CharField(max_length=30, unique=True, default=100101, verbose_name='员工工号')
    phone = models.CharField(max_length=11, blank=True, null=True, verbose_name='电话')
    email = models.CharField(max_length=30, blank=True, null=True, verbose_name='邮箱')
    city = models.CharField(max_length=10, blank=True, null=True, verbose_name='城市')
    address = models.CharField(max_length=30, blank=True, null=True, verbose_name='地址')
    postalcode = models.CharField(max_length=10, blank=True, null=True, verbose_name='邮政编码')
    state = models.SmallIntegerField(default=1, verbose_name='状态')
    headimage = models.ImageField(blank=True, null=True, verbose_name='头像')
    addex = models.FileField(max_length=30, blank=True, null=True, verbose_name='附件')
    birthday = models.DateField(blank=True, null=True, verbose_name='出生日期')
    startdate = models.DateField(blank=True, null=True, verbose_name='聘用日期')
    enddate = models.DateField(blank=True, verbose_name='终止日期')
    title = models.CharField(max_length=30, blank=True, null=True, verbose_name='头衔')
    job = models.ForeignKey(Organization, verbose_name='职务名称')
    department = models.CharField(max_length=30, verbose_name='部门')
    is_management = models.SmallIntegerField(default=0, verbose_name='是否是主管人')
    # group = models.ForeignKey(blank=True, null=True)
    # def __str__(self):
    #     return self.name


#  python json数据转dict
class TreeNode():
    def __init__(self):
        self.id = 0
        self.text = "Node 1"
        self.href = None
        self.selectable = True
        self.backColor = "#2894FF"
        self.color = "#ffffff"
        self.state = {
                             'checked': True,
                             'disabled': True,
                             'expanded': True,
                             'selected': True,
                         },
        self.tags = ['available'],
        self.nodes = []
        # self.enableLinks = None

    def to_dict(self):
        icon = (len(self.nodes) > 0) and 'glyphicon glyphicon-list-alt' or 'glyphicon glyphicon-user'
        return {
                'id': self.id,
                'text': self.text,
                'icon': icon,
                'href': self.href,
                'tags': ['点击操作'],
                'nodes': self.nodes,
                'backColor': self.backColor,
                'color': self.color,
                # 'enableLinks': self.enableLinks,
            }
