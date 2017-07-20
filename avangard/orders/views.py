from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core import serializers
from .models import Order
from .forms import OrderForm
from avangard.museums.models import Schedule, Museum
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import datetime


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
        new_objects = Order.objects.filter(pk__gt=old_latest_id, pk__lte=latest_id)

        order_dict = {}
        order_records = []

        for order_object in new_objects:
            pk = order_object.pk
            museum = order_object.museum.name
            seance = order_object.seance.__str__()
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

            record = {"pk": pk, "museum": museum, "seance": seance, "date": date, "full_price": full_price,
                      "fullticket_count": fullticket_count, "reduceticket_count": reduceticket_count,
                      "audioguide": audioguide, "accompanying_guide": accompanying_guide, "status": status,
                      "name": name,
                      "email": email, "phone": phone}

            order_records.append(record)

        order_dict["new_orders"] = order_records

        return JsonResponse(order_dict)


# @login_required
def create_order(request):
    museum_id = request.GET.get('museum_id', 1)
    museum = Museum.objects.get(pk=museum_id)
    order_formset = OrderForm(initial={'museum': museum}, data=request.POST or None)
    if request.method == 'GET':
        return render(request, 'create_order.html', {'type': 'create', "form": order_formset, "museum": museum})
    elif request.method == 'POST':
        if order_formset.is_valid():
            order_formset.save()
            return redirect('orders_index')
        else:
            return render(request, 'create_order.html', {'type': 'create', "form": order_formset, "museum": museum})


@login_required
@csrf_exempt
def get_seances_for_date(request):
    date = datetime.datetime.strptime(request.GET["date"], "%d-%m-%Y").date()
    museum = Museum.objects.get(pk=request.GET["museum_id"])
    seances = Schedule.objects.filter(museum=museum, date=date)
    data = [{'value': seance.id, 'text': str(seance)} for seance in seances]
    return JsonResponse({'seances': data})


@login_required
@csrf_exempt
def update_order_status(request, order_id):
    new_status = request.POST["new_status"]
    order = get_object_or_404(Order, pk=order_id)
    order.status = new_status
    order.save(update_fields=["status"])
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
                      {'type': 'edit', 'museum': instance.museum, "form": order_formset, "date": instance.seance.date})
    elif request.method == 'POST':
        if order_formset.is_valid():
            order_formset.save()
            return redirect('orders_index')
        else:
            return render(request, 'create_order.html',
                          {'type': 'edit', 'museum': instance.museum, "form": order_formset})


@csrf_exempt
@login_required
def delete_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    order.delete()
    return JsonResponse({'latest_id': Order.objects.latest('pk').pk})