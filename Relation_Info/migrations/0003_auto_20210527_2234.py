# Generated by Django 3.2.3 on 2021-05-27 14:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Entity_Info', '0003_alter_user_info_user_branch'),
        ('Relation_Info', '0002_auto_20210527_2225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch_client_sale',
            name='sale_branch_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Entity_Info.branch_info'),
        ),
        migrations.AlterField(
            model_name='branch_client_sale',
            name='sale_goods_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Entity_Info.goods_info'),
        ),
        migrations.AlterField(
            model_name='company_branch_delivery',
            name='delivery_branch_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Entity_Info.branch_info'),
        ),
        migrations.AlterField(
            model_name='company_branch_delivery',
            name='delivery_goods_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Entity_Info.goods_info'),
        ),
        migrations.AlterField(
            model_name='company_branch_delivery',
            name='delivery_storage_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Entity_Info.storage_info'),
        ),
        migrations.AlterField(
            model_name='company_branch_delivery',
            name='goods_delivery_staff',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Entity_Info.user_info'),
        ),
        migrations.AlterField(
            model_name='supplier_company_purchase',
            name='Purchase_user_account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Entity_Info.user_info'),
        ),
        migrations.AlterField(
            model_name='supplier_company_purchase',
            name='purchase_storage_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Entity_Info.storage_info'),
        ),
    ]
