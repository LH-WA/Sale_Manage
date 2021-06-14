from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.charts import Map
from pyecharts.faker import Faker

from Relation_Info.models import Company_Branch_Delivery, Supplier_Goods_Info
from Entity_Info.models import User_Info, Branch_Info, Storage_Info, Goods_Info
from datetime import date


# Create your views here.
class Record(object):
    delivery_id = 0
    bill = 0
    delivery_request = 0
    SKU = 0
    Supplier_Goods_Info_Request = 0
    Supplier_Goods_Info_Goods = 0


def company_branch_delivery(request):
    District_list = [item for item in Branch_Info.objects.values_list('branch_id', 'branch_district')][1:]
    Edit_id = request.GET.get("Edit_id", '')
    Page_id = request.GET.get('page', 1)
    if Edit_id:
        Record.delivery_id = Edit_id

    # 删除
    Delete_id = request.GET.get("Delete_id", '')
    if Delete_id and Company_Branch_Delivery.objects.filter(goods_delivery_id=Delete_id):
        Company_Branch_Delivery.objects.get(goods_delivery_id=Delete_id).delete()

    # 删完再查询
    Max_id = max([item['goods_delivery_id'] for item in Company_Branch_Delivery.objects.values('goods_delivery_id')])
    bill_lists = Company_Branch_Delivery.objects.order_by('-goods_delivery_id')
    if Page_id != 1:
        bill_lists = Record.bill
        request.POST = Record.delivery_request
    else:
        Record.delivery_request = request.POST
        Record.bill = bill_lists

    bill_lists_len = len(bill_lists)
    paginator = Paginator(bill_lists, 3)
    bill_lists = paginator.page(Page_id)

    if request.GET.get('Reset'):
        return render(request, 'Company_Branch_Delivery.html',
                      {'bill_lists': bill_lists, 'Dist': District_list,
                       'New_id': Max_id + 1, 'bill_len': bill_lists_len, 'paginator': paginator})

    # 修改
    Edit_goods_delivery_send_time = request.POST.get("edit_goods_delivery_send_time", '')
    Edit_goods_delivery_receive_time = request.POST.get("edit_goods_delivery_receive_time", '')
    Edit_goods_num = request.POST.get("edit_goods_num", '')
    Edit_delivery_branch_id = request.POST.get("edit_delivery_branch_id", '')
    Edit_delivery_storage_id = request.POST.get("edit_delivery_storage_id", '')
    Edit_delivery_goods_id = request.POST.get("edit_delivery_goods_id", '')
    Edit_goods_delivery_staff_id = request.POST.get("edit_goods_delivery_staff_id", '')

    if Edit_goods_delivery_send_time:
        Company_Branch_Delivery.objects.filter(goods_delivery_id=Record.delivery_id).update(
            goods_delivery_send_time=Edit_goods_delivery_send_time)
    if Edit_goods_delivery_receive_time:
        Company_Branch_Delivery.objects.filter(goods_delivery_id=Record.delivery_id).update(
            goods_delivery_receive_time=Edit_goods_delivery_receive_time)
    if Edit_goods_num:
        Company_Branch_Delivery.objects.filter(goods_delivery_id=Record.delivery_id).update(
            goods_num=Edit_goods_num)
    if Edit_delivery_branch_id:
        Company_Branch_Delivery.objects.filter(goods_delivery_id=Record.delivery_id).update(
            delivery_branch_id_id=Edit_delivery_branch_id)
    if Edit_delivery_storage_id:
        Company_Branch_Delivery.objects.filter(goods_delivery_id=Record.delivery_id).update(
            delivery_storage_id_id=Edit_delivery_storage_id)
    if Edit_delivery_goods_id:
        Company_Branch_Delivery.objects.filter(goods_delivery_id=Record.delivery_id).update(
            delivery_goods_id_id=Edit_delivery_goods_id)
    if Edit_goods_delivery_staff_id:
        Company_Branch_Delivery.objects.filter(goods_delivery_id=Record.delivery_id).update(
            goods_delivery_staff_id_id=Edit_goods_delivery_staff_id)

    Edit_object = ''
    Edit_id_branch_id = ''
    Edit_id_branch_district = ''
    if Edit_id and Company_Branch_Delivery.objects.filter(goods_delivery_id=Edit_id):
        Edit_id_branch_id = Branch_Info.objects.get(
            branch_id=Company_Branch_Delivery.objects.get(goods_delivery_id=Edit_id).delivery_branch_id_id)
        Edit_id_branch_district = Edit_id_branch_id.branch_district
        Edit_object = Company_Branch_Delivery.objects.get(goods_delivery_id=Edit_id)

    # 搜索
    Search_Goods_delivery_id = request.POST.get("Search_Goods_delivery_id")
    Search_Time_begin = request.POST.get("Search_Time_begin")
    Search_Time_end = request.POST.get("Search_Time_end")
    Search_Staff_id = request.POST.get("Search_Staff_id")
    Search_Branch_id = request.POST.get("Search_Branch_id", 'All')
    Msg = {'msg_1': '', 'msg_2': '', 'msg_3': '', 'msg_4': '', 'msg_5': ''}
    if Search_Goods_delivery_id and not Company_Branch_Delivery.objects.filter(
            goods_delivery_id__contains=Search_Goods_delivery_id):
        Msg['msg_1'] = '无此单号'
    if Search_Staff_id and not User_Info.objects.filter(user_account__contains=Search_Staff_id):
        Msg['msg_2'] = '无此员工号'

    if Msg['msg_1'] or Msg['msg_2']:
        return render(request, 'Company_Branch_Delivery.html',
                      {'bill_lists': bill_lists, 'Dist': District_list, 'Msg': Msg,
                       'New_id': Max_id + 1, 'Edit_id': Edit_id, 'All_request': request.POST,
                       'bill_len': bill_lists_len, 'paginator': paginator})

    condition_dict = {}
    show_str_1 = str(Search_Time_begin)
    show_str_2 = str(Search_Time_end)
    if not Search_Time_begin:
        Search_Time_begin = date(2000, 1, 1)
        show_str_1 = '开业'
    if not Search_Time_end:
        Search_Time_end = date(2029, 12, 31)
        show_str_2 = '今'

    if Search_Branch_id != 'All':
        condition_dict['delivery_branch_id__branch_id'] = Search_Branch_id
    if Search_Staff_id:
        condition_dict['goods_delivery_staff_id__user_account__contains'] = Search_Staff_id
    if Search_Goods_delivery_id:
        condition_dict['goods_delivery_id__contains'] = Search_Goods_delivery_id
    condition_dict['goods_delivery_send_time__range'] = [Search_Time_begin, Search_Time_end]
    bill_lists = Company_Branch_Delivery.objects.filter(**condition_dict)

    # 新增
    New_goods_delivery_send_time = request.POST.get("new_goods_delivery_send_time", '')
    New_goods_delivery_receive_time = request.POST.get("new_goods_delivery_receive_time", '')
    New_goods_num = request.POST.get("new_goods_num", '')
    New_delivery_branch_id = request.POST.get("new_delivery_branch_id", '')
    New_delivery_storage_id = request.POST.get("new_delivery_storage_id", '')
    New_delivery_goods_id = request.POST.get("new_delivery_goods_id", '')
    New_goods_delivery_staff_id = request.POST.get("new_goods_delivery_staff_id", '')
    if New_delivery_goods_id and not Goods_Info.objects.filter(goods_id=New_delivery_goods_id):
        Msg['msg_3'] = '商品编号不存在'
    if New_delivery_storage_id and not Storage_Info.objects.filter(storage_id=New_delivery_storage_id):
        Msg['msg_4'] = '仓库编号不存在'
    if New_goods_delivery_staff_id and not User_Info.objects.filter(user_account=New_goods_delivery_staff_id):
        Msg['msg_5'] = '员工不存在'
    elif New_goods_delivery_staff_id and not User_Info.objects.get(
            user_account=New_goods_delivery_staff_id).user_dep == '物流部门':
        Msg['msg_5'] = '此员工不属物流部门'

    if Msg['msg_3'] or Msg['msg_4'] or Msg['msg_5']:
        return render(request, 'Company_Branch_Delivery.html',
                      {'bill_lists': bill_lists, 'Dist': District_list, 'Msg': Msg,
                       'New_id': Max_id + 1, 'Edit_id': Edit_id, 'All_request': request.POST,
                       'bill_len': bill_lists_len, 'paginator': paginator})
    if New_goods_delivery_send_time and New_delivery_branch_id and New_delivery_storage_id and New_delivery_goods_id and New_goods_delivery_staff_id:
        Company_Branch_Delivery.objects.create(goods_delivery_id=Max_id + 1,
                                               goods_delivery_send_time=New_goods_delivery_send_time,
                                               goods_delivery_receive_time=New_goods_delivery_receive_time,
                                               goods_num=New_goods_num,
                                               delivery_branch_id_id=New_delivery_branch_id,
                                               delivery_storage_id_id=New_delivery_storage_id,
                                               delivery_goods_id_id=New_delivery_goods_id,
                                               goods_delivery_staff_id_id=New_goods_delivery_staff_id)

    # 排序
    Delivery_id_Sort = request.POST.get("Delivery_id_Sort")
    Send_time_Sort = request.POST.get("Send_time_Sort")
    Receive_time_Sort = request.POST.get("Receive_time_Sort")
    Goods_num_Sort = request.POST.get("Goods_num_Sort")
    Branch_id_Sort = request.POST.get("Branch_id_Sort")
    Storage_id_Sort = request.POST.get("Storage_id_Sort")
    Good_id_Sort = request.POST.get("Good_id_Sort")
    Staff_id_Sort = request.POST.get("Staff_id_Sort")
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
        if Sort_condition(Delivery_id_Sort):
            sort_list.append(Sort_condition(Delivery_id_Sort))
        elif Sort_condition(Send_time_Sort):
            sort_list.append(Sort_condition(Send_time_Sort))
        elif Sort_condition(Receive_time_Sort):
            sort_list.append(Sort_condition(Receive_time_Sort))
        elif Sort_condition(Goods_num_Sort):
            sort_list.append(Sort_condition(Goods_num_Sort))
        elif Sort_condition(Branch_id_Sort):
            sort_list.append(Sort_condition(Branch_id_Sort))
        elif Sort_condition(Storage_id_Sort):
            sort_list.append(Sort_condition(Storage_id_Sort))
        elif Sort_condition(Good_id_Sort):
            sort_list.append(Sort_condition(Good_id_Sort))
        elif Sort_condition(Staff_id_Sort):
            sort_list.append(Sort_condition(Staff_id_Sort))
    bill_lists = bill_lists.order_by(*sort_list)

    Show_data = ''
    if request.POST.get('Show_state'):
        District_name = [item[1] for item in District_list]
        District_num = len(District_name)
        sum_list = [0] * District_num
        for item in bill_lists:
            for i in range(1, District_num + 1):
                if item.delivery_branch_id_id == i:
                    sum_list[i - 1] = sum_list[i - 1] + item.goods_num

        District_value = [(District_name[i], sum_list[i]) for i in range(0, District_num)]
        c = (
            Map(opts.InitOpts(width='1500px', height='750px'))
                .add(show_str_1 + ' 至 ' + show_str_2, District_value, "上海",
                     is_map_symbol_show=False, is_roam=False)
                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .set_global_opts(title_opts=opts.TitleOpts(title="上海配送图", pos_left='center'),
                                 visualmap_opts=opts.VisualMapOpts(pos_right=20))
        )
        Show_data = c.render_embed()

    # print('POST内容: ', request.POST)
    if Page_id != 1:
        bill_lists = Record.bill
        request.POST = Record.delivery_request
    else:
        Record.delivery_request = request.POST
        Record.bill = bill_lists

    bill_lists_len = len(bill_lists)
    paginator = Paginator(bill_lists, 3)
    bill_lists = paginator.page(Page_id)

    return render(request, 'Company_Branch_Delivery.html',
                  {'bill_lists': bill_lists, 'Dist': District_list, 'New_id': Max_id + 1,
                   'Edit_id': Edit_id, 'All_request': request.POST, 'bill_len': bill_lists_len,
                   'Edit_id_branch_id': Edit_id_branch_id, 'Edit_id_branch_district': Edit_id_branch_district,
                   'Edit_object': Edit_object,  'data': Show_data, 'paginator': paginator})


def Sort_condition(mode):
    if mode == 'delivery_id_incr':
        return 'goods_delivery_id'
    elif mode == 'delivery_id_desc':
        return '-goods_delivery_id'
    elif mode == 'delivery_send_time_incr':
        return 'goods_delivery_send_time'
    elif mode == 'delivery_send_time_desc':
        return '-goods_delivery_send_time'
    elif mode == 'delivery_receive_time_incr':
        return 'goods_delivery_receive_time'
    elif mode == 'delivery_receive_time_desc':
        return '-goods_delivery_receive_time'
    elif mode == 'goods_num_incr':
        return 'goods_num'
    elif mode == 'goods_num_desc':
        return '-goods_num'
    elif mode == 'branch_id_incr':
        return 'delivery_branch_id'
    elif mode == 'branch_id_desc':
        return '-delivery_branch_id'
    elif mode == 'storage_id_incr':
        return 'delivery_storage_id'
    elif mode == 'storage_id_desc':
        return '-delivery_storage_id'
    elif mode == 'goods_id_incr':
        return 'delivery_goods_id'
    elif mode == 'goods_id_desc':
        return '-delivery_goods_id'
    elif mode == 'staff_id_incr':
        return 'goods_delivery_staff_id'
    elif mode == 'staff_id_desc':
        return '-goods_delivery_staff_id'
    elif mode == 'SKU_incr':
        return 'SKU'
    elif mode == 'SKU_desc':
        return '-SKU'
    elif mode == 'order_price_incr':
        return 'order_price'
    elif mode == 'order_price_desc':
        return '-order_price'
    else:
        return 0


# def company_branch_delivery_show(request):
#     if request.POST.get('Show_state'):
#         District_name = [item[1] for item in District_list]
#         District_num = len(District_name)
#         sum_list = [0] * District_num
#         for item in bill_lists:
#             for i in range(1, District_num + 1):
#                 if item.delivery_branch_id_id == i:
#                     sum_list[i - 1] = sum_list[i - 1] + item.goods_num
#
#         District_value = [(District_name[i], sum_list[i]) for i in range(0, District_num)]
#         c = (
#             Map()
#                 .add("", District_value, "上海",
#                      is_map_symbol_show=False, )
#                 .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
#                 .set_global_opts(title_opts=opts.TitleOpts(title="上海配送图"),
#                                  visualmap_opts=opts.VisualMapOpts(max_=max(sum_list), split_number=5,
#                                                                    is_piecewise=True))
#         )
#         return render(request, 'Company_Branch_Delivery.html',
#                       {'bill_lists': bill_lists, 'Dist': District_list, 'New_id': Max_id + 1,
#                        'Edit_id': Edit_id, 'data': c.render_embed(),
#                        'All_request': request.POST, 'bill_len': bill_lists_len})

def supplier_goods_info(request):
    Edit_id = request.GET.get("Edit_id", '')
    Page_id = request.GET.get('page', 1)
    if Edit_id:
        Record.count = Edit_id

    # 删除
    Delete_id = request.GET.get("Delete_id", '')
    if Delete_id and Supplier_Goods_Info.objects.filter(SKU=Delete_id):
        Supplier_Goods_Info.objects.get(SKU=Delete_id).delete()

    # 删完再查询
    goods_lists = Supplier_Goods_Info.objects.order_by('-SKU')
    if Page_id != 1:
        goods_lists = Record.Supplier_Goods_Info_Goods
        request.POST = Record.Supplier_Goods_Info_Request
    else:
        Record.Supplier_Goods_Info_Request = request.POST
        Record.Supplier_Goods_Info_Goods = goods_lists
    goods_len = len(goods_lists)
    paginator = Paginator(goods_lists, 10)
    goods_lists = paginator.page(Page_id)
    if request.GET.get('Reset'):
        return render(request, 'Supplier_Goods_Info.html',
                      {'goods_lists': goods_lists, 'goods_len': goods_len, 'paginator': paginator})

    # 修改
    Edit_SKU = request.POST.get("edit_SKU", '')
    Edit_order_price = request.POST.get("edit_order_price", '')
    if Edit_SKU:
        Supplier_Goods_Info.objects.filter(SKU=Record.SKU).update(
            SKU=Edit_SKU)
    if Edit_order_price:
        Supplier_Goods_Info.objects.filter(SKU=Record.SKU).update(
            order_price=Edit_order_price)
    Edit_object = ''
    if Edit_id and Supplier_Goods_Info.objects.filter(SKU=Edit_id):
        Edit_object = Supplier_Goods_Info.objects.get(SKU=Edit_id)
    # 查询
    Search_SKU = request.POST.get("Search_SKU")
    Search_price = request.POST.get("Search_price")
    condition_dict = {}
    Search_price_low_bound = '0'
    Search_price_up_bound = '99999'
    Find_Index = str(Search_price).find('-')
    if Search_price and Find_Index == -1:
        Search_price_low_bound = Search_price
        Search_price_up_bound = Search_price
    elif Search_price and Find_Index == 0:
        Search_price_up_bound = str(Search_price)[Find_Index + 1:]
    elif Search_price and Find_Index == len(Search_price) - 1:
        Search_price_low_bound = str(Search_price)[:Find_Index]
    elif Search_price:
        Search_price_low_bound = str(Search_price)[:Find_Index]
        Search_price_up_bound = str(Search_price)[Find_Index + 1:]
    if Search_SKU:
        condition_dict['SKU__contains'] = Search_SKU
    Msg = {'msg_1': '', 'msg_2': ''}
    if Search_SKU and not Supplier_Goods_Info.objects.filter(SKU__contains=Search_SKU):
        Msg['msg_1'] = '店内码无此数据项'
    if Msg['msg_1']:
        return render(request, 'Supplier_Goods_Info.html',
                      {'goods_lists': goods_lists, 'Msg': Msg,
                       'Edit_id': Edit_id, 'All_request': request.POST,
                       'goods_len': goods_len, 'paginator': paginator})
    condition_dict['order_price__range'] = [Search_price_low_bound, Search_price_up_bound]
    goods_lists = Supplier_Goods_Info.objects.filter(**condition_dict)

    # 新增
    New_SKU = request.POST.get("new_SKU", '')
    New_order_price = request.POST.get("new_order_price", '')
    goods_len = len(paginator.page(Page_id))
    if New_SKU and New_order_price:
        if Supplier_Goods_Info.objects.filter(SKU__contains=New_SKU):
            Msg['msg_2'] = '该店内码已存在'
            return render(request, 'Supplier_Goods_Info.html',
                          {'goods_lists': goods_lists, 'Msg': Msg,
                           'Edit_id': Edit_id, 'All_request': request.POST,
                           'goods_len': goods_len, 'paginator': paginator})
        else:
            Supplier_Goods_Info.objects.create(SKU=New_SKU, order_price=New_order_price)
    # 排序
    SKU_Sort = request.POST.get("SKU_Sort")
    order_price_Sort = request.POST.get("order_price_Sort")
    Multistage_query = request.POST.get("Multistage_query")
    Level_1 = request.POST.get("Level_1")
    Level_2 = request.POST.get("Level_2")

    sort_list = []
    if Multistage_query:
        if Level_1:
            sort_list.append(Sort_condition(Level_1))
            if Level_2:
                sort_list.append(Sort_condition(Level_2))
    else:
        if Sort_condition(SKU_Sort):
            sort_list.append(Sort_condition(SKU_Sort))
        elif Sort_condition(order_price_Sort):
            sort_list.append(Sort_condition(order_price_Sort))
    goods_lists = goods_lists.order_by(*sort_list)
    if Page_id != 1:
        goods_lists = Record.Supplier_Goods_Info_Goods
        request.POST = Record.Supplier_Goods_Info_Request
    else:
        Record.Supplier_Goods_Info_Request = request.POST
        Record.Supplier_Goods_Info_Goods = goods_lists
    goods_len = len(goods_lists)
    # print('POST内容: ', request.POST)
    paginator = Paginator(goods_lists, 10)
    goods_lists = paginator.page(Page_id)
    return render(request, 'Supplier_Goods_Info.html',
                  {'goods_lists': goods_lists, 'Edit_id': Edit_id, 'All_request': request.POST,
                   'goods_len': goods_len, 'Edit_object': Edit_object, 'paginator': paginator})
