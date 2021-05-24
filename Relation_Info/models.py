from django.db import models

# Create your models here.
class Branch_Client_Sale(models.Model):
    """门店_顾客：销售联系"""
    # 销售单号
    branch_sale_id = models.IntegerField(primary_key=True, unique=True)
    # 销售数量
    branch_sale_num = models.IntegerField()
    # 售价
    branch_sale_price = models.DecimalField(max_digits=5, decimal_places=2)
    # 销售时间
    branch_sale_time = models.DateTimeField()
    # 门店号
    branch_id = models.ForeignKey('Entity_Info.Branch_Info', on_delete=models.DO_NOTHING)
    # 商品码
    goods_id = models.ForeignKey('Entity_Info.Goods_Info', on_delete=models.DO_NOTHING)

class Goods_Brench_Storage(models.Model):
    """商品_门店：库存联系"""
    # 库存代码
    goods_storage_id = models.IntegerField(primary_key=True, unique=True)
    # 商品数量
    goods_storage_num = models.IntegerField()


class Company_Branch_Delivery(models.Model):
    """公司_门店：配送联系"""
    # 配送单号
    goods_delivery_id = models.IntegerField(primary_key=True, unique=True)
    # 发货时间
    goods_delivery_send_time = models.DateTimeField()
    # 收货时间
    branch_sale_receive_time = models.DateTimeField()
    # 销售数量
    goods_num = models.IntegerField()
    # 门店号
    branch_id = models.ForeignKey('Entity_Info.Branch_Info', on_delete=models.DO_NOTHING)
    # 仓库号
    storage_id = models.ForeignKey('Entity_Info.Storage_Info', on_delete=models.DO_NOTHING)
    # 商品码
    goods_id = models.ForeignKey('Entity_Info.Goods_Info', on_delete=models.DO_NOTHING)
    # 物流员工
    user_account = models.ForeignKey('Entity_Info.User_Info', on_delete=models.DO_NOTHING)

class Supplier_Branch_Purchase(models.Model):
    """供应商_公司：采购联系"""
    # 采购单号
    goods_purchase_id = models.IntegerField(primary_key=True, unique=True)
    # 采购时间
    goods_purchase_time = models.DateTimeField()
    # 供应时间
    goods_supply_time = models.DateTimeField()
    # 采购数量
    goods_purchase_num = models.IntegerField()
    # 门店号
    branch_id = models.IntegerField()
    # 购入价格
    goods_purchase_price = models.DecimalField(max_digits=5, decimal_places=2)
    # 仓库号
    storage_id = models.ForeignKey('Entity_Info.Storage_Info', on_delete=models.DO_NOTHING)
    # 相关员工
    user_account = models.ForeignKey('Entity_Info.User_Info', on_delete=models.DO_NOTHING)

class Brench_User_Info(models.Model):
    """门店_员工：信息联系"""
    # 员工编号
    user_id = models.ForeignKey('Entity_Info.User_Info', on_delete=models.DO_NOTHING)
    # 商品数量
    branch_id = models.ForeignKey('Entity_Info.Branch_Info', on_delete=models.DO_NOTHING)
    # 是否为负责人
    is_dir = models.BooleanField()