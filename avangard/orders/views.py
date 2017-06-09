from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order
from .forms import OrderForm
from avangard.museums.models import Schedule, Museum
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import datetime


def orders_index(request):
    return HttpResponse("orders page")


def create_order(request):
    museum_id = request.GET.get('museum_id', 1)
    museum = Museum.objects.get(pk=museum_id)
    order_formset = OrderForm(initial={'museum': museum}, data=request.POST or None)
    order_formset.fields["seance"].queryset = Schedule.objects.filter(museum=museum, date=datetime.date.today())
    if request.method == 'GET':
        return render(request, 'create_order.html', {'type': 'create', "form": order_formset, "museum": museum})
    elif request.method == 'POST':
        seance = request.POST.get('seance')
        order_formset.fields['seance'].choices = [(seance, seance)]
        if order_formset.is_valid():
            order_formset.save()
            return HttpResponse("Order created")
        else:
            print(order_formset.errors.as_data())
            return HttpResponse(order_formset.errors.as_data())


@csrf_exempt
def get_seances_for_date(request):
    date = datetime.datetime.strptime(request.GET["date"], "%d-%m-%Y").date()
    museum = Museum.objects.get(pk=request.GET["museum_id"])
    seances = Schedule.objects.filter(museum=museum, date=date)
    data = [{'value': seance.id, 'text': str(seance)} for seance in seances]
    return JsonResponse({'seances': data})


def edit_order(request):
    return HttpResponse("orders page")


def delete_order(request):
    return HttpResponse("orders page")
