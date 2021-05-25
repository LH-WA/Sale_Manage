from django.shortcuts import render,redirect
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
# Create your views here.

from Entity_Info.models import User_Info,Goods_Info

# from pyecharts.globals import CurrentConfig
from django.shortcuts import render
# from django.db import connection
# from django.http import HttpResponse
# from django.template import loader
# from pyecharts.faker import Faker
from pyecharts import options as opts
from pyecharts.charts import Bar

def index(request):

    return render(request, 'index.html')

def logins(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        if not User_Info.objects.filter(user_account=username):
            msg_1 = '账号不存在！'
            return render(request, 'login.html', locals())
        if not User_Info.objects.filter(user_account=username,user_psw=password):
            msg_2 = '密码错误！'
            return render(request, 'login.html', locals())
        request.session['is_login'] = True
        request.session['username'] = username
        request.session['password'] = password
        return render(request, 'index.html', {'username': username})
    return render(request, 'login.html')


def regist(request):
    if request.method == 'POST':
        Account = request.POST.get("Account")
        Name = request.POST.get("Name")
        Tel = request.POST.get("Tel")
        Password = request.POST.get("Password")
        Password_r = request.POST.get("Password_r")
        Branch = request.POST.get("Branch")
        Section = request.POST.get("Section")
        if len(Account) != 8:
            msg_1 = '账号长度应为8位'
            return render(request, 'regist.html', locals())
        elif Account.isdigit() == False :
            msg_1 = '账号应只含数字'
            return render(request, 'regist.html', locals())
        elif Account.count(' ') != 0:
            msg_1 = '账号应不含空格'
            return render(request, 'regist.html', locals())
        elif User_Info.objects.filter(user_account=Account):
            msg_1 = '账号重复'
            return render(request, 'regist.html', locals())

        if len(Name) >= 8:
            msg_2 = '员工名字大于8位'
            return render(request, 'regist.html', locals())

        if len(Tel) >= 11:
            msg_3 = '电话号码大于11位'
            return render(request, 'regist.html', locals())
        elif len(Tel) <= 7:
            msg_3 = '电话号码小于7位'
            return render(request, 'regist.html', locals())

        if len(Password) < 5 or len(Password) > 8:
            msg_4 = '密码长度应为6-8位字符'
            return render(request, 'regist.html', locals())
        elif Password != Password_r:
            msg_4 = '两次输入密码不一样！'
            return render(request, 'regist.html', locals())

        if Branch=='00':
            msg_5 = '请选择所属分店'
            return render(request, 'regist.html', locals())
        if Section=='00':
            msg_6 = '请选择所属部门'
            return render(request, 'regist.html', locals())
        User_Info.objects.create(user_account=Account,user_psw=Password,user_branch=Branch,user_dep=Section)

        return redirect('/login/')
    return render(request, 'regist.html')


def logout(request):
    if not request.session.get('is_login',None):
        return redirect('/login/')

    request.session.flush()
    return redirect('/regist/')


def goods_info_new_input(request):
    if request.method == 'POST':
        Id = request.POST.get("Goods_id")
        Name = request.POST.get("Goods_name")
        Category = request.POST.get("Goods_category")
        Unit = request.POST.get("Goods_unit")
        Price = request.POST.get("Goods_price")

        if Goods_Info.objects.filter(goods_id=Id):
            msg_1 = '商品信息已存在'
            return render(request, 'goods_new_input.html', locals())

        Goods_Info.objects.create(goods_id=Id, goods_name=Name, goods_category=Category, goods_unit=Unit, goods_price=Price)

    return render(request, 'goods_new_input.html')


def show_chart(request):
    Goods = ['河马', '蟒蛇', '老虎', '大象', '兔子', '熊猫', '狮子']
    Value1 = [135, 37, 72, 150, 21, 98, 51]
    Value2 = [15, 56, 42, 10, 21, 98, 51]

    bar = (
        Bar()
            .add_xaxis(Goods)
            .add_yaxis("商家A", Value1)
            .add_yaxis("商家B", Value2)
            # .reversal_axis()
            # .set_series_opts(label_opts=opts.LabelOpts(position="right"))
            .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例", subtitle="我是副标题"))
    )
    data = {'data': bar.render_embed()}
    return render(request, 'Pyechart.html', data)