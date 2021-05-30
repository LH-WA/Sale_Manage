from django.shortcuts import render
from django.db.models import Q
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.charts import Map
from pyecharts.faker import Faker

from Relation_Info.models import Company_Branch_Delivery
from Entity_Info.models import User_Info, Branch_Info, Storage_Info, Goods_Info
from datetime import date


# Create your views here.
class Record(object):
    count = 0  # Record.count是静态变量


def company_branch_delivery(request):
    Temp = [item for item in Branch_Info.objects.values_list('branch_id', 'branch_district')][1:]
    Edit_id = request.GET.get("Edit_id", '')
    # print('GET内容: ', request.GET)
    State = 0
    if Edit_id:
        State = 1
        Record.count = Edit_id
    # 删除
    Delete_id = request.GET.get("Delete_id", '')
    if Delete_id:
        Company_Branch_Delivery.objects.get(goods_delivery_id=Delete_id).delete()

    # 删完再查询
    Max_id = max([item['goods_delivery_id'] for item in Company_Branch_Delivery.objects.values('goods_delivery_id')])
    bill_lists = Company_Branch_Delivery.objects.order_by('-goods_delivery_id')[:5]
    if request.method == 'POST':
        # 修改
        Edit_goods_delivery_send_time = request.POST.get("edit_goods_delivery_send_time", '')
        Edit_goods_delivery_receive_time = request.POST.get("edit_goods_delivery_receive_time")
        Edit_goods_num = request.POST.get("edit_goods_num")
        Edit_delivery_branch_id = request.POST.get("edit_delivery_branch_id")
        Edit_delivery_storage_id = request.POST.get("edit_delivery_storage_id")
        Edit_delivery_goods_id = request.POST.get("edit_delivery_goods_id")
        Edit_goods_delivery_staff_id = request.POST.get("edit_goods_delivery_staff_id")

        if Edit_goods_delivery_send_time:
            Company_Branch_Delivery.objects.filter(goods_delivery_id=Record.count).update(
                goods_delivery_send_time=Edit_goods_delivery_send_time)
        if Edit_goods_delivery_receive_time:
            Company_Branch_Delivery.objects.filter(goods_delivery_id=Record.count).update(
                goods_delivery_receive_time=Edit_goods_delivery_receive_time)
        if Edit_goods_num:
            Company_Branch_Delivery.objects.filter(goods_delivery_id=Record.count).update(
                goods_num=Edit_goods_num)
        if Edit_delivery_branch_id:
            Company_Branch_Delivery.objects.filter(goods_delivery_id=Record.count).update(
                delivery_branch_id_id=Edit_delivery_branch_id)
        if Edit_delivery_storage_id:
            Company_Branch_Delivery.objects.filter(goods_delivery_id=Record.count).update(
                delivery_storage_id_id=Edit_delivery_storage_id)
        if Edit_delivery_goods_id:
            Company_Branch_Delivery.objects.filter(goods_delivery_id=Record.count).update(
                delivery_goods_id_id=Edit_delivery_goods_id)
        if Edit_goods_delivery_staff_id:
            Company_Branch_Delivery.objects.filter(goods_delivery_id=Record.count).update(
                goods_delivery_staff_id_id=Edit_goods_delivery_staff_id)

        # 搜索
        Search_Goods_delivery_id = request.POST.get("Search_Goods_delivery_id")
        Search_Time_begin = request.POST.get("Search_Time_begin")
        Search_Time_end = request.POST.get("Search_Time_end")
        Search_Staff_id = request.POST.get("Search_Staff_id")
        Search_Branch_id = request.POST.get("Search_Branch_id")
        if not Search_Time_begin:
            Search_Time_begin = date(2000, 1, 1)
        if not Search_Time_end:
            Search_Time_end = date(2029, 12, 31)
        Msg = {'msg_1': '', 'msg_2': '', 'msg_3': '', 'msg_4': '', 'msg_5': ''}
        if Search_Staff_id and not User_Info.objects.filter(user_account__contains=Search_Staff_id):
            Msg['msg_1'] = '员工号无此字段'
        if Search_Goods_delivery_id and not Company_Branch_Delivery.objects.filter(
                goods_delivery_id__contains=Search_Goods_delivery_id):
            Msg['msg_2'] = '单号无此字段'
        if Msg['msg_1'] or Msg['msg_2']:
            return render(request, 'Company_Branch_Delivery.html',
                          {'bill_lists': bill_lists, 'Dist': Temp, 'Msg': Msg, 'State': State,
                           'New_id': Max_id + 1, 'Edit_id': Edit_id, 'All_request': request.POST,
                           'bill_len': len(bill_lists)})

        condition_dict = {}
        if Search_Branch_id:
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
        if New_delivery_storage_id and not Storage_Info.objects.filter(storage_id=New_delivery_storage_id):
            Msg['msg_3'] = '仓库不存在'
        if New_delivery_goods_id and not Goods_Info.objects.filter(goods_id=New_delivery_goods_id):
            Msg['msg_4'] = '商品不存在'
        if New_goods_delivery_staff_id and not User_Info.objects.filter(user_account=New_goods_delivery_staff_id):
            Msg['msg_5'] = '员工不存在'

        if Msg['msg_3'] or Msg['msg_4'] or Msg['msg_5']:
            return render(request, 'Company_Branch_Delivery.html',
                          {'bill_lists': bill_lists, 'Dist': Temp, 'Msg': Msg, 'State': State,
                           'New_id': Max_id + 1, 'Edit_id': Edit_id, 'All_request': request.POST,
                           'bill_len': len(bill_lists)})
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

        # print('POST内容: ', request.POST)
        return render(request, 'Company_Branch_Delivery.html',
                      {'bill_lists': bill_lists, 'Dist': Temp, 'State': State, 'New_id': Max_id + 1,
                       'Edit_id': Edit_id, 'All_request': request.POST, 'bill_len': len(bill_lists)})

    Edit_id_branch_id = ''
    Edit_id_branch_district = ''
    if Edit_id:
        Edit_id_branch_id = Branch_Info.objects.get(
            branch_id=Company_Branch_Delivery.objects.get(goods_delivery_id=Edit_id).delivery_branch_id_id)
        Edit_id_branch_district = Edit_id_branch_id.branch_district
    return render(request, 'Company_Branch_Delivery.html',
                  {'bill_lists': bill_lists, 'Dist': Temp, 'State': State, 'New_id': Max_id + 1, 'Edit_id': Edit_id,
                   'Edit_id_branch_id': Edit_id_branch_id, 'Edit_id_branch_district': Edit_id_branch_district,
                   'All_request': request.POST, 'bill_len': len(bill_lists)})


def Sort_condition(Mode):
    if Mode == 'delivery_id_incr':
        return 'goods_delivery_id'
    elif Mode == 'delivery_id_desc':
        return '-goods_delivery_id'
    elif Mode == 'delivery_send_time_incr':
        return 'goods_delivery_send_time'
    elif Mode == 'delivery_send_time_desc':
        return '-goods_delivery_send_time'
    elif Mode == 'delivery_receive_time_incr':
        return 'goods_delivery_receive_time'
    elif Mode == 'delivery_receive_time_desc':
        return '-goods_delivery_receive_time'
    elif Mode == 'goods_num_incr':
        return 'goods_num'
    elif Mode == 'goods_num_desc':
        return '-goods_num'
    elif Mode == 'branch_id_incr':
        return 'delivery_branch_id'
    elif Mode == 'branch_id_desc':
        return '-delivery_branch_id'
    elif Mode == 'storage_id_incr':
        return 'delivery_storage_id'
    elif Mode == 'storage_id_desc':
        return '-delivery_storage_id'
    elif Mode == 'goods_id_incr':
        return 'delivery_goods_id'
    elif Mode == 'goods_id_desc':
        return '-delivery_goods_id'
    elif Mode == 'staff_id_incr':
        return 'goods_delivery_staff_id'
    elif Mode == 'staff_id_desc':
        return '-goods_delivery_staff_id'
    else:
        return 0

# def company_branch_delivery_show(request):
#     Temp = [item for item in Branch_Info.objects.values_list('branch_id', 'branch_district')]
#     if request.method == 'POST':
#         Time_begin = request.POST.get("Time_begin")
#         Time_end = request.POST.get("Time_end")
#         Staff_id = request.POST.get("Staff_id")
#         Branch_id = request.POST.get("Branch_id")
#         Goods_delivery_id = request.POST.get("Goods_delivery_id")
#         if not Time_begin:
#             Time_begin = date(2000, 1, 1)
#         if not Time_end:
#             Time_end = date(2029, 12, 31)
#
#         if Staff_id and not User_Info.objects.filter(user_account=Staff_id):
#             msg_1 = '无此员工'
#             return render(request, 'Company_Branch_Delivery.html', locals())
#
#         if Branch_id and not Branch_Info.objects.filter(branch_id=Branch_id):
#             msg_2 = '无此门店'
#             return render(request, 'Company_Branch_Delivery.html', locals())
#
#         if Goods_delivery_id and not Company_Branch_Delivery.objects.filter(goods_delivery_id=Goods_delivery_id):
#             msg_3 = '无此单号'
#             return render(request, 'Company_Branch_Delivery.html', locals())
#
#         condition_dict = {}
#         if Branch_id:
#             condition_dict['delivery_branch_id'] = Branch_id
#         if Staff_id:
#             condition_dict['goods_delivery_staff_id'] = Staff_id
#         if Goods_delivery_id:
#             condition_dict['goods_delivery_id'] = Goods_delivery_id
#         bill_lists = Company_Branch_Delivery.objects.filter(
#             **condition_dict, goods_delivery_send_time__range=[Time_begin, Time_end]
#         )
#
#         # District_num= [item.delivery_branch_id_id for item in bill_lists]
#         District_list = [item['branch_district'] for item in Branch_Info.objects.values('branch_district')]
#         District_num = len(District_list)
#         sum_list = [0] * District_num
#         for item in bill_lists:
#             for i in range(1, District_num + 1):
#                 if item.delivery_branch_id_id == i:
#                     sum_list[i - 1] = sum_list[i - 1] + item.goods_num
#
#         District_value = [(District_list[i], sum_list[i]) for i in range(0, District_num)]
#
#         c = (
#             Map()
#                 .add("", District_value, "上海",
#                      is_map_symbol_show=False, )
#                 .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
#                 .set_global_opts(title_opts=opts.TitleOpts(title="Map-基本示例"),
#                                  visualmap_opts=opts.VisualMapOpts(max_=max(sum_list), split_number=5,
#                                                                    is_piecewise=True))
#         )
#         return render(request, 'Testshow.html', {'Dist': Temp, 'data': c.render_embed()})
#     # bill_lists = Company_Branch_Delivery.objects.order_by('-goods_delivery_id')[:4]
#     return render(request, 'Testshow.html', {'Dist': Temp})
