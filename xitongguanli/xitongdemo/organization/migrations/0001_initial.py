# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-04-03 09:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='员工姓名')),
                ('number', models.CharField(default=100101, max_length=30, unique=True, verbose_name='员工工号')),
                ('phone', models.CharField(blank=True, max_length=11, null=True, verbose_name='电话')),
                ('email', models.CharField(blank=True, max_length=30, null=True, verbose_name='邮箱')),
                ('city', models.CharField(blank=True, max_length=10, null=True, verbose_name='城市')),
                ('address', models.CharField(blank=True, max_length=30, null=True, verbose_name='地址')),
                ('postalcode', models.CharField(blank=True, max_length=10, null=True, verbose_name='邮政编码')),
                ('state', models.SmallIntegerField(default=1, verbose_name='状态')),
                ('headimage', models.ImageField(blank=True, null=True, upload_to='', verbose_name='头像')),
                ('addex', models.FileField(blank=True, max_length=30, null=True, upload_to='', verbose_name='附件')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='出生日期')),
                ('startdate', models.DateField(blank=True, null=True, verbose_name='聘用日期')),
                ('enddate', models.DateField(blank=True, verbose_name='终止日期')),
                ('title', models.CharField(blank=True, max_length=30, null=True, verbose_name='头衔')),
                ('department', models.CharField(max_length=30, verbose_name='部门')),
                ('is_management', models.SmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='组织机构名称')),
                ('number', models.CharField(default=1001, max_length=10, unique=True, verbose_name='机构代码')),
                ('type', models.IntegerField(verbose_name='公司/分公司/部门/职务')),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='organization.Organization')),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.Organization', verbose_name='职务名称'),
        ),
    ]