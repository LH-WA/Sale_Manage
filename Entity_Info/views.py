from django.shortcuts import render, redirect, HttpResponse
from django.forms import Form, fields, widgets
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

from Entity_Info.models import User_Info, Goods_Info, Supplier_Info, Branch_Info, Storage_Info

# from django.db import connection
# from django.http import HttpResponse
# from django.template import loader
# from pyecharts.faker import Faker
from pyecharts import options as opts
from pyecharts.charts import Bar


class TestForm(Form):
    inp1 = fields.CharField(min_length=4, max_length=8)
    inp2 = fields.EmailField()
    inp3 = fields.IntegerField(min_value=10, max_value=100)


def index(request):
    return render(request, 'index.html')


def logins(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        if not User_Info.objects.filter(user_account=username):
            return render(request, 'login.html', {'msg_1': '账号不存在！', 'username': username, 'password': password})
        if not User_Info.objects.filter(user_account=username, user_psw=password):
            return render(request, 'login.html', {'msg_2': '密码错误！', 'username': username, 'password': password})
        request.session['is_login'] = True
        request.session['username'] = username
        request.session['password'] = password
        return render(request, 'index.html', {'username': username})
    return render(request, 'login.html')


def regist(request):
    Temp = [item for item in Branch_Info.objects.values_list('branch_id', 'branch_district')]
    Account_list = ([item for item in User_Info.objects.values('user_account')])
    Account = max([item['user_account'] for item in Account_list]) + 1

    if request.method == 'POST':
        # Account = request.POST.get("Account")
        Name = request.POST.get("Name")
        Tel = request.POST.get("Tel")
        Password = request.POST.get("Password")
        Password_r = request.POST.get("Password_r")
        Branch = request.POST.get("Branch")
        Department = request.POST.get("Department")
        # if len(Account) != 8:
        #     msg_1 = '账号长度应为8位'
        #     return render(request, 'regist.html', {'Dist': Temp})
        # elif Account.isdigit() == False :
        #     msg_1 = '账号应只含数字'
        #     return render(request, 'regist.html', {'Dist': Temp})
        # elif Account.count(' ') != 0:
        #     msg_1 = '账号应不含空格'
        #     return render(request, 'regist.html', {'Dist': Temp})
        # elif User_Info.objects.filter(user_account=Account):
        #     msg_1 = '账号重复'
        #     return render(request, 'regist.html', {'Dist': Temp})

        if len(Name) >= 8:
            msg_2 = '员工名字大于8位'
            return render(request, 'regist.html', {'Dist': Temp, 'Account': Account})

        if len(Tel) > 11:
            msg_3 = '电话号码大于11位'
            return render(request, 'regist.html', {'Dist': Temp, 'Account': Account})
        elif len(Tel) < 7:
            msg_3 = '电话号码小于7位'
            return render(request, 'regist.html', {'Dist': Temp, 'Account': Account})

        if len(Password) < 5 or len(Password) > 8:
            msg_4 = '密码长度应为6-8位字符'
            return render(request, 'regist.html', {'Dist': Temp, 'Account': Account})
        elif Password != Password_r:
            msg_4 = '两次输入密码不一样！'
            return render(request, 'regist.html', {'Dist': Temp, 'Account': Account})

        if Branch == '00':
            msg_5 = '请选择所属分店'
            return render(request, 'regist.html', {'Dist': Temp, 'Account': Account})
        if Department == '00':
            msg_6 = '请选择所属部门'
            return render(request, 'regist.html', {'Dist': Temp, 'Account': Account})
        User_Info.objects.create(user_account=Account, user_psw=Password, user_name=Name, user_tel=Tel,
                                 user_branch_id=Branch, user_dep=Department)

        return redirect('/login/')

    return render(request, 'regist.html', {'Dist': Temp, 'Account': Account})


def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')

    request.session.flush()
    return redirect('/regist/')


def goods_info_input(request):
    if request.method == 'POST':
        Id = request.POST.get("Goods_id")
        Name = request.POST.get("Goods_name")
        Category = request.POST.get("Goods_category")
        Unit = request.POST.get("Goods_unit")
        Price = request.POST.get("Goods_price")

        if Goods_Info.objects.filter(goods_id=Id):
            msg_1 = '商品信息已存在'
            return render(request, 'goods_input.html', locals())

        Goods_Info.objects.create(goods_id=Id, goods_name=Name, goods_category=Category, goods_unit=Unit,
                                  goods_price=Price)

    return render(request, 'goods_input.html')


def supplier_info_input(request):
    if request.method == 'POST':
        Id = request.POST.get("Supplier_id")
        Name = request.POST.get("Supplier_name")
        Mail = request.POST.get("Supplier_mail")
        Tel = request.POST.get("Supplier_tel")
        Address = request.POST.get("Supplier_address")

        if Supplier_Info.objects.filter(supplier_id=Id):
            msg_1 = '供应商信息已存在'
            return render(request, 'goods_new_input.html', locals())

        Supplier_Info.objects.create(supplier_id=Id, supplier_name=Name, supplier_mail=Mail, supplier_tel=Tel,
                                     supplier_address=Address)

    return render(request, 'goods_new_input.html')


def branch_info_input(request):
    if request.method == 'POST':
        Id = request.POST.get("Branch_id")
        District = request.POST.get("Branch_district")
        Address = request.POST.get("Branch_address")

        if Branch_Info.objects.filter(supplier_id=Id):
            msg_1 = '分店信息已存在'
            return render(request, 'goods_new_input.html', locals())

        Supplier_Info.objects.create(branch_id=Id, branch_district=District, branch_address=Address)

    return render(request, 'goods_new_input.html')


def storage_info_input(request):
    if request.method == 'POST':
        Id = request.POST.get("Storage_id")
        Address = request.POST.get("Storage_address")

        if Branch_Info.objects.filter(supplier_id=Id):
            msg_1 = '仓库信息已存在'
            return render(request, 'goods_new_input.html', locals())

        Storage_Info.objects.create(storage_id=Id, storage_address=Address)

    return render(request, 'goods_new_input.html')



def test(request):
    if request.method == 'GET':
        obj = TestForm()
        # return render(request, 'test.html', {'obj': obj})
    else:
        obj = TestForm(request.POST)
        if obj.is_valid():
            return HttpResponse('提交成功')
    return render(request, 'test.html', {'obj': obj})