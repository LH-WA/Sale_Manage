from django.shortcuts import render, redirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import cv2
import pyzbar.pyzbar as pyzbar
from Entity_Info.models import User_Info, Goods_Info, Supplier_Info, Branch_Info, Storage_Info
# Create your views here.

# from django.db import connection
# from django.http import HttpResponse
# from django.template import loader
# from pyecharts.faker import Faker
from pyecharts import options as opts
from pyecharts.charts import Bar

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 30)


def Scan_BarCode():
    x_r = 0
    y_r = 0
    w_r = 0
    h_r = 0
    count_num = 0
    barcodeData_r = 0
    while (True):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        barcodes = pyzbar.decode(gray)

        for barcode in barcodes:
            barcodeData = barcode.data.decode("utf-8")
            (x, y, w, h) = barcode.rect
            if ((x + w / 2) - (x_r + w_r / 2)) ** 2 + ((y + h / 2) - (y_r + h_r / 2)) ** 2 < 5:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                text = "{}".format(barcodeData)
                cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 125), 2)
            x_r = x
            y_r = y
            w_r = w
            h_r = h

            if barcodeData_r == barcodeData:
                count_num = count_num + 1
            else:
                count_num = 0
            barcodeData_r = barcodeData

        cv2.imshow('frame', frame)
        cv2.waitKey(1)
        if count_num > 3:
            break

    cv2.destroyAllWindows()
    return barcodeData_r


def index(request):
    return render(request, 'index.html', {'username': request.session['username']})


def logins(request):
    if request.method == 'POST':
        account = request.POST.get("account")
        password = request.POST.get("password")
        if not User_Info.objects.filter(user_account=account):
            return render(request, 'login.html', {'msg_1': '账号不存在！', 'username': account, 'password': password})
        if not User_Info.objects.filter(user_account=account, user_psw=password):
            return render(request, 'login.html', {'msg_2': '密码错误！', 'username': account, 'password': password})

        request.session['username'] = User_Info.objects.get(user_account=account).user_name
        request.session['branch'] = User_Info.objects.get(user_account=account).user_branch_id
        return redirect('/index/')
    return render(request, 'login.html')


def regist(request):
    Temp = [item for item in Branch_Info.objects.values_list('branch_id', 'branch_district')]
    Account_list = ([item for item in User_Info.objects.values('user_account')])
    Account = max([item['user_account'] for item in Account_list]) + 1

    if request.method == 'POST':
        Name = request.POST.get("Name")
        Tel = request.POST.get("Tel")
        Password = request.POST.get("Password")
        Password_r = request.POST.get("Password_r")
        Branch = request.POST.get("Branch")
        Department = request.POST.get("Department")

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
    # request.session.flush()
    request.session['username'] = ''
    request.session['branch_district'] = ''
    # request.session['password'] = ''
    return redirect('/login/')


class Record(object):
    good_id = 0
    bill = 0
    goods_info_request = 0


def goods_info(request):
    Edit_id = request.GET.get("Edit_id", '')
    Page_id = request.GET.get('page', 1)
    Scan = request.GET.get('Scan')

    if Edit_id:
        Record.good_id = Edit_id
    # 删除
    Delete_id = request.GET.get("Delete_id", '')
    if Delete_id and Goods_Info.objects.filter(goods_id=Delete_id):
        Goods_Info.objects.get(goods_id=Delete_id).delete()

    # 删完再查询
    bill_lists = Goods_Info.objects.order_by('-goods_id')

    if Page_id != 1 or Scan:
        request.POST = Record.goods_info_request
        bill_lists = Record.bill
    else:
        Record.goods_info_request = request.POST
        Record.bill = bill_lists

    bill_lists_len = len(bill_lists)
    paginator = Paginator(bill_lists, 5)
    bill_lists = paginator.page(Page_id)

    # 修改
    Edit_goods_name = request.POST.get("edit_goods_name", '')
    Edit_goods_category = request.POST.get("edit_goods_category", '')
    Edit_goods_unit = request.POST.get("edit_goods_unit", '')
    Edit_goods_price = request.POST.get("edit_goods_price", '')

    if Edit_goods_name:
        Goods_Info.objects.filter(goods_id=Record.good_id).update(
            goods_delivery_send_time=Edit_goods_name)
    if Edit_goods_category:
        Goods_Info.objects.filter(goods_id=Record.good_id).update(
            goods_delivery_receive_time=Edit_goods_category)
    if Edit_goods_unit:
        Goods_Info.objects.filter(goods_id=Record.good_id).update(
            goods_num=Edit_goods_unit)
    if Edit_goods_price:
        Goods_Info.objects.filter(goods_id=Record.good_id).update(
            goods_price=Edit_goods_price)

    # 搜索
    Search_goods_id = request.POST.get("Search_goods_id")
    Search_goods_name = request.POST.get("Search_goods_name")
    Search_goods_category = request.POST.get("Search_goods_category")
    Search_goods_unit = request.POST.get("Search_goods_unit")
    Search_goods_price = request.POST.get("Search_goods_price")

    Search_goods_price_start = '0'
    Search_goods_price_end = '99999'
    Find_Index = str(Search_goods_price).find('-')
    if Search_goods_price and Find_Index == -1:  # xxx
        Search_goods_price_start = Search_goods_price
        Search_goods_price_end = Search_goods_price
    elif Search_goods_price and Find_Index == 0:  # - xxx
        Search_goods_price_end = str(Search_goods_price)[Find_Index + 1:]
    elif Search_goods_price and Find_Index == len(str(Search_goods_price)) - 1:  # xxx -
        Search_goods_price_start = str(Search_goods_price)[:Find_Index]
    elif Search_goods_price:  # xxx-xxx
        Search_goods_price_start = str(Search_goods_price)[:Find_Index]
        Search_goods_price_end = str(Search_goods_price)[Find_Index + 1:]

    Msg = {'msg_1': '', 'msg_2': '', 'msg_3': '', 'msg_4': ''}
    if Search_goods_id and not Goods_Info.objects.filter(goods_id__contains=Search_goods_id):
        Msg['msg_1'] = '单号无此数据'
    if Search_goods_name and not Goods_Info.objects.filter(goods_name__contains=Search_goods_name):
        Msg['msg_2'] = '商品名无此数据'
    if Search_goods_category and not Goods_Info.objects.filter(goods_category__contains=Search_goods_category):
        Msg['msg_3'] = '商品类别无此数据'
    if Search_goods_unit and not Goods_Info.objects.filter(goods_unit__contains=Search_goods_unit):
        Msg['msg_4'] = '商品单位无此数据'
    if Msg['msg_1'] or Msg['msg_2'] or Msg['msg_3'] or Msg['msg_4']:
        return render(request, 'Goods_info.html',
                      {'bill_lists': bill_lists, 'Msg': Msg,
                       'Edit_id': Edit_id, 'All_request': request.POST,
                       'bill_len': bill_lists_len, 'paginator': paginator})

    condition_dict = {}
    if Search_goods_id:
        condition_dict['goods_id__contains'] = Search_goods_id
    if Search_goods_name:
        condition_dict['goods_name__contains'] = Search_goods_name
    if Search_goods_category:
        condition_dict['goods_category__contains'] = Search_goods_category
    if Search_goods_unit:
        condition_dict['goods_unit__contains'] = Search_goods_unit
    if Search_goods_price:
        condition_dict['goods_price__range'] = [Search_goods_price_start, Search_goods_price_end]

    bill_lists = Goods_Info.objects.filter(**condition_dict)

    New_Goods_id = request.POST.get("New_Goods_id")
    New_Goods_name = request.POST.get("New_Goods_name")
    New_Goods_category = request.POST.get("New_Goods_category")
    New_Goods_unit = request.POST.get("New_Goods_unit")
    New_Goods_price = request.POST.get("New_Goods_price")

    if New_Goods_name and New_Goods_category and New_Goods_unit and New_Goods_price:
        Goods_Info.objects.create(goods_id=New_Goods_id, goods_name=New_Goods_name, goods_category=New_Goods_category,
                                  goods_unit=New_Goods_unit,
                                  goods_price=New_Goods_price)

    Good_id_Sort = request.POST.get("Good_id_Sort")
    Good_name_Sort = request.POST.get("Good_name_Sort")
    Good_price_Sort = request.POST.get("Good_price_Sort")
    Multistage_query = request.POST.get("Multistage_query")
    Level_1 = request.POST.get("Level_1")
    Level_2 = request.POST.get("Level_2")
    Level_3 = request.POST.get("Level_3")
    sort_list = []
    if Multistage_query:
        if Level_1:
            sort_list.append(Sort_condition(Level_1))
            if Level_2:
                sort_list.append(Sort_condition(Level_2))
                if Level_3:
                    sort_list.append(Sort_condition(Level_3))
    else:
        if Sort_condition(Good_id_Sort):
            sort_list.append(Sort_condition(Good_id_Sort))
        elif Sort_condition(Good_name_Sort):
            sort_list.append(Sort_condition(Good_name_Sort))
        elif Sort_condition(Good_price_Sort):
            sort_list.append(Sort_condition(Good_price_Sort))

    bill_lists = bill_lists.order_by(*sort_list)

    if Page_id != 1 or Scan:
        request.POST = Record.goods_info_request
        bill_lists = Record.bill
    else:
        Record.goods_info_request = request.POST
        Record.bill = bill_lists

    bill_lists_len = len(bill_lists)
    paginator = Paginator(bill_lists, 5)
    bill_lists = paginator.page(Page_id)

    barcodeData = ''
    if Scan:
        barcodeData = Scan_BarCode()

    # print('POST内容: ', request.POST)
    # print('GET内容: ', request.GET)
    return render(request, 'Goods_info.html',
                  {'bill_lists': bill_lists, 'Edit_id': Edit_id, 'All_request': request.POST,
                   'bill_len': bill_lists_len, 'paginator': paginator, 'barcodeData': barcodeData})


# def Scan_BarCode():
#     x_r = 0
#     y_r = 0
#     w_r = 0
#     h_r = 0
#     count_num = 0
#     barcodeData_r = 0
#     while (True):
#         ret, frame = cap.read()
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         barcodes = pyzbar.decode(gray)
#
#         for barcode in barcodes:
#             barcodeData = barcode.data.decode("utf-8")
#             (x, y, w, h) = barcode.rect
#             if ((x + w / 2) - (x_r + w_r / 2)) ** 2 + ((y + h / 2) - (y_r + h_r / 2)) ** 2 < 5:
#                 cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
#                 text = "{}".format(barcodeData)
#                 cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 125), 2)
#             x_r = x
#             y_r = y
#             w_r = w
#             h_r = h
#
#             if barcodeData_r == barcodeData:
#                 count_num = count_num + 1
#             else:
#                 count_num = 0
#             barcodeData_r = barcodeData
#
#         cv2.imshow('frame', frame)
#         cv2.waitKey(1)
#         if count_num > 3:
#             break
#
#     cv2.destroyAllWindows()
#     return barcodeData_r


def Sort_condition(mode):
    if mode == 'good_id_incr':
        return 'goods_id'
    elif mode == 'good_id_desc':
        return '-goods_id'
    elif mode == 'good_name_incr':
        return 'goods_name'
    elif mode == 'good_name_desc':
        return '-goods_name'
    elif mode == 'good_price_incr':
        return 'goods_price'
    elif mode == 'good_price_desc':
        return '-goods_price'
    elif mode == 'good_category_incr':
        return 'goods_category'
    elif mode == 'good_category_desc':
        return '-goods_category'
    elif mode == 'good_unit_incr':
        return 'goods_unit'
    elif mode == 'good_unit_desc':
        return '-goods_unit'
    else:
        return 0


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
