from django.db import models

# Create your models here.
class User_Info(models.Model):
    """用户信息"""
    # 用户账号
    user_account = models.CharField(max_length=10, primary_key=True, unique=True)
    # 用户密码
    user_psw = models.CharField(max_length=10)
    # 用户名
    user_name = models.CharField(max_length=10)
    # 用户所在部门
    user_dep = models.CharField(max_length=10)
    # 用户电话
    user_tel = models.CharField(max_length=11)
    # 用户所在分店
    # user_branch = models.CharField(max_length=10)

class Goods_Info(models.Model):
    """商品信息"""
    # 商品编号
    goods_id = models.IntegerField(primary_key=True, unique=True)
    # 商品名称
    goods_name = models.CharField(max_length=10)
    # 商品类别
    goods_category = models.CharField(max_length=10)
    # 商品单位
    goods_unit = models.CharField(max_length=2)
    # 商品售价
    goods_price = models.DecimalField(max_digits=5, decimal_places=2)

class Supplier_Info(models.Model):
    """供应商信息"""
    # 供应商编号
    supplier_id = models.IntegerField(max_length=6, primary_key=True, unique=True)
    # 供应商名称
    supplier_name = models.CharField(max_length=10)
    # 供应商邮件
    supplier_mail = models.CharField(max_length=12)
    # 供应商电话
    supplier_tel = models.CharField(max_length=11)
    # 供应商地址
    supplier_address = models.CharField(max_length=11)

class Branch_Info(models.Model):
    """门店信息"""
    # 门店编号
    branch_id = models.IntegerField(primary_key=True, unique=True)
    # 门店名称
    branch_name = models.CharField(max_length=10)
    # 门店地址
    branch_address = models.CharField(max_length=15)
    # 门店管理人---
    # branch_manager = models.BigIntegerField(max_length=11)

class Storage_Info(models.Model):
    """仓库信息"""
    # 仓库编号
    storage_id = models.IntegerField(primary_key=True, unique=True)
    # 仓库地址
    storage_address = models.CharField(max_length=15)