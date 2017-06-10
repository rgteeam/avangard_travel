from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order
from .forms import OrderForm
from avangard.museums.models import Schedule, Museum
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import datetime


@login_required
def orders_index(request):
    orders = Order.objects.all()

    if request.method == 'GET':
        context = {'orders': orders}
        return render(request, 'orders.html', context)


@login_required
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
def edit_order(request, order_id):
    instance = get_object_or_404(Order, id=order_id)
    order_formset = OrderForm(request.POST or None, instance=instance)
    if request.method == 'GET':
        return render(request, 'create_order.html', {'type':'edit', 'museum':instance.museum, "form": order_formset, "date": instance.seance.date})
    elif request.method == 'POST':
        if order_formset.is_valid():
            order_formset.save()
            return redirect('orders_index')
        else:
            return render(request, 'create_order.html', {'type':'edit', 'museum':instance.museum, "form": order_formset})


@csrf_exempt
@login_required
def delete_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    order.delete()
    return HttpResponse(status=200)
