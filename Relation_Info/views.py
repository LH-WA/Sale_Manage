from django.shortcuts import render
from Relation_Info.models import Company_Branch_Delivery
# Create your views here.

def company_branch_delivery(request):
    if request.method == 'POST':
        Inquiry = request.POST.get("Inquiry")
        Time_begin = request.POST.get("Time_begin", "2011-05-03")
        Time_end = request.POST.get("Time_end", "2100-12-31 01:01:01")
        print(Time_begin)
        if Inquiry == '单号顺序':
            bill_lists=Company_Branch_Delivery.objects.filter(goods_delivery_send_time__gt = Time_begin, goods_delivery_send_time__lt = Time_end)
            # bill_lists = Company_Branch_Delivery.objects.order_by('goods_delivery_id')[:4]
            return render(request, 'Test.html', {'bill_lists': bill_lists})
        if Inquiry == '单号逆序':
            bill_lists = Company_Branch_Delivery.objects.order_by('-goods_delivery_id')[:4]
            return render(request, 'Test.html', {'bill_lists': bill_lists})

    bill_lists = Company_Branch_Delivery.objects.order_by('goods_delivery_send_time')[:4]
    return render(request, 'Test.html', {'bill_lists': bill_lists})