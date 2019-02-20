import datetime
import json
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core import serializers
from .models import Order, SuperOrder
from .forms import OrderForm
from avangard.museums.models import Schedule, Museum
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from collections import defaultdict
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder


@login_required
def orders_index(request):
    if request.method == 'GET':
        context = {'type': 'current'}
        return render(request, 'orders.html', context)


@login_required
def get_old_orders(request):
    if request.method == 'GET':
        context = {'type': 'old'}
        return render(request, 'orders.html', context)


@login_required
@csrf_exempt
def get_latest_id(request):
    if request.method == 'GET':
        latest_id = Order.objects.latest('pk').pk
        return HttpResponse(latest_id)


@login_required
@csrf_exempt
def get_new_orders(request):
    if request.method == 'GET':
        latest_id = Order.objects.latest('pk').pk
        old_latest_id = int(request.GET["latest_id"])
        new_objects = Order.objects.filter(pk__gt=old_latest_id, pk__lte=latest_id).order_by('pk')
        order_dict = {}
        order_records = []

        for order_object in new_objects:
            pk = order_object.pk
            museum = order_object.museum.name
            seance = str(order_object.seance.start_time) + " - " + str(order_object.seance.end_time)
            date = order_object.seance.date.strftime("%Y-%m-%d")
            full_price = order_object.full_price
            fullticket_count = order_object.fullticket_count
            reduceticket_count = order_object.reduceticket_count
            audioguide = order_object.audioguide
            accompanying_guide = order_object.accompanying_guide
            status = order_object.status
            name = order_object.name
            email = order_object.email
            phone = order_object.phone
            company = order_object.seance.company_id

            record = {"pk": pk, "museum": museum, "seance": seance, "date": date, "full_price": full_price,
                      "fullticket_count": fullticket_count, "reduceticket_count": reduceticket_count,
                      "audioguide": audioguide, "accompanying_guide": accompanying_guide, "status": status,
                      "name": name, "email": email, "phone": phone, "company": company}

            order_records.append(record)

        order_dict["new_orders"] = order_records

        return JsonResponse(order_dict)


def get_timeblock_data(request):
    if request.method == 'GET':
        seances_id_str = request.GET.get('seances_id', [])
        data = dict()
        seances = list()
        summury = defaultdict(int)
        for seance in Schedule.objects.filter(pk__in=set(seances_id_str.split(','))):
            seances.append({"pk": seance.pk, "full_count": seance.full_count, "reduce_count": seance.reduce_count, "full_price": seance.full_price, "reduce_price": seance.reduce_price})
            summury["all_full_сount"] += int(seance.full_count)
            summury["all_reduce_count"] += int(seance.reduce_count)

            if summury["min_full_price"] == 0:
                summury["min_full_price"] = list()
                summury["min_full_price"].append(seance.full_price)
            else:
                summury["min_full_price"].append(seance.full_price)

            if summury["min_reduce_price"] == 0:
                summury["min_reduce_price"] = list()
                summury["min_reduce_price"].append(seance.reduce_price)
            else:
                summury["min_reduce_price"].append(seance.reduce_price)
        summury["min_full_price"] = min(summury["min_full_price"])
        summury["min_reduce_price"] = min(summury["min_reduce_price"])
        summury["max_tickets_count"] = Schedule.objects.get(id=list(seances_id_str.split(','))[0]).museum.max_count
        summury["audioguide_price"] = Schedule.objects.get(id=list(seances_id_str.split(','))[0]).museum.audioguide_price
        summury["accompanying_guide_price"] = Schedule.objects.get(id=list(seances_id_str.split(','))[0]).museum.accompanying_guide_price
        data["summury"] = summury
        data["seances"] = seances
        data["museum"] = Schedule.objects.get(id=list(seances_id_str.split(','))[0]).museum.name
        data["time"] = Schedule.objects.get(pk=list(seances_id_str.split(','))[0]).time_str
        json.dumps(data, sort_keys=True, indent=1, cls=DjangoJSONEncoder)
        return JsonResponse({'timeblock_data': data})


def make_superorder():
    return 0


def create_orders(data):
    if data['audioguide'] > 0:
        audioguide = True
    else:
        audioguide = False
    if data['accompanying_guide'] > 0:
        accompanying_guide = True
    else:
        accompanying_guide = False
    museum = Museum.objects.get(pk=data['museum'])
    so = SuperOrder(audioguide=audioguide, accompanying_guide=accompanying_guide, name=data["name"], museum=museum,
                    email=data["email"], phone=data["phone"], fullticket_count=data["fullticketCount"], reduceticket_count=data["reduceticketCount"], totalPrice=data["totalPrice"])
    so.save()
    for i in data['ticketsData']:
        seance = Schedule.objects.get(pk=i)
        order = Order(seance=seance, museum=museum, fullticket_count=data['ticketsData'][i].get("full_count", 0),
                      reduceticket_count=data['ticketsData'][i].get("reduce_count", 0), audioguide=audioguide, accompanying_guide=accompanying_guide,
                      name=data['name'], phone=data['phone'], email=data['email'], superorder=so)

        order.save()
        so.date = seance.date
        so.start_time = seance.start_time
        so.end_time = seance.end_time
        so.save()
    print(so.id)
    return so.id


def create_sorder(request):
    if request.method == 'POST':
        data = json.loads(request.POST['data'])
        super_order_id = create_orders(data)
        return JsonResponse({'SuperOrderId': super_order_id})


def created_sorder(request):
    if request.method == 'POST':
        print(request.POST)
        sorder_id = request.POST['sorderId']
        sorder = SuperOrder.objects.get(pk=sorder_id)
        orders = []
        for i in sorder.orders:
            order = Order.objects.get(pk=i)
            order2 = model_to_dict(order)
            order2['full_price'] = order.full_price
            orders.append(order2)
        context = {"data": orders, "sorder": sorder}
        # sorder_id = request.POST
        return render(request, 'payment.html', context)


# @login_required
# def create_order(data):
#     museum_id = request.GET.get('museum_id', 4)
#     museum = Museum.objects.get(pk=museum_id)
#     order_formset = OrderForm(initial={'museum': museum}, data=request.POST or None)
#     if request.method == 'GET':
#         return render(request, 'create_order.html', {'type': 'create', "form": order_formset, "museum": museum})
#     elif request.method == 'POST':
#         if order_formset.is_valid():
#             if order_formset.data.get("audioguide", "no") == "on":
#                 audioguide = True
#             else:
#                 audioguide = False
#             if order_formset.data.get("accompanying_guide", "no") == "on":
#                 accompanying_guide = True
#             else:
#                 accompanying_guide = False
#             o = order_formset.save(commit=False)
#             so = SuperOrder(audioguide=audioguide, accompanying_guide=accompanying_guide, name=order_formset.data["name"],
#                             email=order_formset.data["email"], phone=order_formset.data["phone"])
#             so.save()
#             o.superorder = so
#             o.save()
#             so.save()
#             return redirect('orders_index')
#         else:
#             return render(request, 'create_order.html', {'type': 'create', "form": order_formset, "museum": museum,
#                                                          "date": order_formset.cleaned_data["seance"].date})


# @login_required
@csrf_exempt
def get_seances_for_date(request):
    date = datetime.datetime.strptime(request.GET["date"], "%d-%m-%Y").date()
    museum = Museum.objects.get(pk=request.GET["museum_id"])
    seances = Schedule.objects.filter(museum=museum, date=date)
    data = [{'value': seance.id, 'text': str(seance)} for seance in seances]
    return JsonResponse({'seances': data})


def aggregate_seances(queryset):
    aggregated_data = list()
    groups = defaultdict(list)
    for obj in queryset:
        groups[obj.time_str].append(obj)
    new_list = groups.values()
    timeblock = dict()
    for obj_time in new_list:
        for item in obj_time:
            timeblock.setdefault("seances", []).append(item.pk)
            timeblock["time_str"] = item.time_str
            timeblock.setdefault("full_count", []).append(item.full_count)
            timeblock.setdefault("reduce_count", []).append(item.reduce_count)
            timeblock.setdefault("full_price", []).append(item.full_price)
            timeblock.setdefault("reduce_price", []).append(item.reduce_price)
        aggregated_data.append(timeblock)
        timeblock = dict()
    newlist = sorted(aggregated_data, key=lambda k: k['time_str'])
    return json.dumps(newlist, sort_keys=True, indent=1, cls=DjangoJSONEncoder)


# @login_required
@csrf_exempt
def get_aggregated_seances(request):
    date = datetime.datetime.strptime(request.GET["date"], "%d-%m-%Y").date()
    museum = Museum.objects.get(pk=request.GET["museum_id"])
    seances = Schedule.objects.filter(museum=museum, date=date)
    data = aggregate_seances(seances)
    return JsonResponse({'aggregated_seances': data})


# @login_required
@csrf_exempt
def seance_selected(request):
    seance = Schedule.objects.get(pk=request.POST["seance_id"])
    return JsonResponse({'seance': {'full_price': seance.full_price, 'reduce_price': seance.reduce_price}})


@login_required
@csrf_exempt
def update_order_status(request, order_id):
    new_status = request.POST["new_status"]
    order = get_object_or_404(Order, pk=order_id)
    order.status = new_status
    order.save()
    return HttpResponse(status=200)


@login_required
@csrf_exempt
def check_new_orders(request):
    latest_id = Order.objects.latest('pk').pk
    old_latest_id = request.POST["latest_id"]
    if latest_id != int(old_latest_id):
        return HttpResponse("true")
    else:
        return HttpResponse("false")


@login_required
def edit_order(request, order_id):
    instance = get_object_or_404(Order, id=order_id)
    order_formset = OrderForm(request.POST or None, instance=instance)
    if request.method == 'GET':
        return render(request, 'create_order.html',
                      {'type': 'edit', 'museum': instance.museum, "form": order_formset, "date": instance.seance.date, "fullticket_store": instance.fullticket_store, "reduceticket_store": instance.reduceticket_store, "order": instance})
    elif request.method == 'POST':
        if order_formset.is_valid():
            order_formset.save()
            return redirect('orders_index')
        else:
            return render(request, 'create_order.html',
                          {'type': 'edit', 'museum': instance.museum, "form": order_formset, "date": instance.seance.date, "fullticket_store": instance.fullticket_store, "reduceticket_store": instance.reduceticket_store, "order": instance})


@login_required
def info_sorder(request, sorder_id=None):
    if sorder_id is None:
        sorder_id = request.POST['sorder_id']
    try:
        currnt_sorder = SuperOrder.objects.get(id=int(sorder_id))

        pk = currnt_sorder.pk
        museum = currnt_sorder.museum.name
        seances = []
        for i in currnt_sorder.orders:
            instance = model_to_dict(Order.objects.get(pk=i))
            instance['company'] = Order.objects.get(pk=i).seance.company.name
            seances.append(instance)
            print(instance)
        date = currnt_sorder.date.strftime("%d-%m-%Y")
        full_price = currnt_sorder.totalPrice
        fullticket_count = currnt_sorder.fullticket_count
        reduceticket_count = currnt_sorder.reduceticket_count
        if currnt_sorder.audioguide is True:
            audioguide = "Да"
        else:
            audioguide = "Нет"
        if currnt_sorder.accompanying_guide is True:
            accompanying_guide = "Да"
        else:
            accompanying_guide = "Нет"
        if currnt_sorder.status == 1:
            status = "Новый"
        elif currnt_sorder.status == 2:
            status = "Одобрен"
        elif currnt_sorder.status == 3:
            status = "Оплачен"
        elif currnt_sorder.status == 4:
            status = "Собран"
        elif currnt_sorder.status == 5:
            status = "Передан"
        elif currnt_sorder.status == 6:
            status = "Отсканирован"
        elif currnt_sorder.status == 7:
            status = "Отказан"
        name = currnt_sorder.name
        email = currnt_sorder.email
        phone = currnt_sorder.phone
        time = str(currnt_sorder.start_time.strftime("%H:%M")) + " - " + str(currnt_sorder.end_time.strftime("%H:%M"))
        # company = currnt_order.seance.company_id
        qr_code = currnt_sorder.qr_code
        voucher_path = currnt_sorder.voucher_path
        record = {"pk": pk, "museum": museum, "seances": seances, "date": date, "full_price": full_price,
                  "fullticket_count": fullticket_count, "reduceticket_count": reduceticket_count,
                  "audioguide": audioguide, "accompanying_guide": accompanying_guide, "status": status,
                  "name": name, "email": email, "phone": phone, "qr_code": qr_code, "voucher_path": voucher_path, "time": time}

        context = {"sorder": record}
    except ValueError:
        context = {"sorder": "NaN"}
    except Order.DoesNotExist:
        context = {"sorder": "None"}

    return render(request, 'sorder_info.html', context)


@csrf_exempt
@login_required
def delete_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    order.delete()
    return JsonResponse({'latest_id': Order.objects.latest('pk').pk})


@csrf_exempt
@login_required
def delete_sorder(request, sorder_id):
    sorder = SuperOrder.objects.get(pk=sorder_id)
    sorder.delete()
    return JsonResponse({'latest_id': SuperOrder.objects.latest('pk').pk})


def ticket_receipt(request):
    context = {}
    return render(request, 'ticket_receipt.html', context)