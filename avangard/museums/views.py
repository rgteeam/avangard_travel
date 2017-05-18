
# Create your views here.

from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from avangard.museums.models import Museum, Schedule

from avangard.museums.forms import MuseumForm
from avangard.museums.tables import MuseumTable
from django_tables2 import RequestConfig
from django.views.decorators.csrf import csrf_exempt
import datetime


# Удаление записи расписания

@csrf_exempt
@login_required
def schedule_delete(request, schedule_id):
    schedule = Schedule.objects.get(pk=schedule_id)
    schedule.delete()
    return HttpResponse(status=200)


# Обновление записи расписания

@csrf_exempt
@login_required
def schedule_update(request, schedule_id):
    if request.method == 'POST':
        schedule = Schedule.objects.get(pk=schedule_id)
        s = parse_schedule_from_post(request.POST)
        schedule.start_time = s.start_time
        schedule.end_time = s.end_time
        schedule.max_count = s.max_count
        schedule.save()
        return HttpResponse(status=200)


# Создание записи расписания

@csrf_exempt
@login_required
def schedule_create(request):
    if request.method == 'POST':
        s = parse_schedule_from_post(request.POST)
        s.save()
        return HttpResponse(s.id)


# Получение расписания

@csrf_exempt
@login_required
def museum_schedule(request, museum_id):
    museum = Museum.objects.get(pk=museum_id)

    if request.method == 'GET':
        schedule = Schedule.objects.filter(museum=museum, date=datetime.date.today())
        context = {'museum': museum, 'schedule': schedule}
        return render(request, 'schedule.html', context)
    elif request.method == 'POST':

        # Обработка AJAX-запроса при выборе даты в календаре

        date = datetime.datetime.strptime(request.POST["date"], "%m/%d/%Y").date()
        schedule = Schedule.objects.filter(museum=museum, date=date)
        context = {'museum': museum, 'schedule': schedule}
        return HttpResponse(render(request, 'schedule_table.html', context))


# Список музеев

@login_required
def index(request):
    table = MuseumTable(Museum.objects.all())
    RequestConfig(request, paginate={"per_page": 25}).configure(table)
    return render(request, 'museums.html', {'table': table, 'dynamic_fields': False})


# Форма создания музея

@login_required
def create_museum_view(request):
    if request.method == 'GET':
        return render(request, 'create.html')
    elif request.method == 'POST':
        museum_formset = MuseumForm(request.POST)
        museum_formset.save()
        return redirect('index')


def parse_schedule_from_post(dict):
    start_time = datetime.datetime.strptime(dict['start_time'], '%H:%M').time()

    try:
        end_time = datetime.datetime.strptime(dict['end_time'], '%H:%M').time()
    except ValueError as e:
        end_time = None

    date = datetime.datetime.strptime(dict['date'], "%d.%m.%Y").date()
    max_count = dict['max_count']
    museum_id = dict['museum_id']
    print(museum_id)
    s = Schedule(start_time=start_time, end_time=end_time, date=date, max_count=max_count)
    s.museum_id = museum_id
    return s
