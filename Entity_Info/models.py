from django.db import models

# Create your models here.
class User_Info(models.Model):
    """用户信息"""
    # 用户(账号/编号)
    user_account = models.AutoField(primary_key=True, unique=True)
    # 用户密码
    user_psw = models.CharField(max_length=8)
    # 用户名
    user_name = models.CharField(max_length=8)
    # 用户电话
    user_tel = models.CharField(max_length=11)
    # 用户所在分店片区
    user_branch = models.ForeignKey('Branch_Info', on_delete=models.PROTECT)
    # 用户所在部门
    user_dep = models.CharField(max_length=5)

class Branch_Info(models.Model):
    """门店信息"""
    # 门店编号
    branch_id = models.PositiveSmallIntegerField(primary_key=True, unique=True)
    # 门店所属片区
    branch_district = models.CharField(max_length=5)
    # 门店地址
    branch_address = models.CharField(max_length=25)

class Goods_Info(models.Model):
    """商品信息"""
    # 商品编号
    goods_id = models.BigIntegerField(primary_key=True, unique=True)
    # 商品名称
    goods_name = models.TextField()
    # 商品类别
    goods_category = models.CharField(max_length=10)
    # 商品单位
    goods_unit = models.CharField(max_length=4)
    # 商品售价
    goods_price = models.DecimalField(max_digits=8, decimal_places=2)

class Supplier_Info(models.Model):
    """供应商信息"""
    # 供应商编号
    supplier_id = models.PositiveSmallIntegerField(primary_key=True, unique=True)
    # 供应商名称
    supplier_name = models.CharField(max_length=15)
    # 供应商邮件
    supplier_mail = models.CharField(max_length=20)
    # 供应商电话
    supplier_tel = models.CharField(max_length=11)
    # 供应商地址
    supplier_address = models.CharField(max_length=25)

class Storage_Info(models.Model):
    """仓库信息"""
    # 仓库编号
    storage_id = models.PositiveSmallIntegerField(primary_key=True, unique=True)
    # 仓库地址
    storage_address = models.CharField(max_length=25)