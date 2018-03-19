from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from avangard.museums.models import Museum
from avangard.orders.models import Order
from datetime import datetime


def export_to_csv(museum, date):
    date = datetime.strptime(date, "%d-%m-%Y").date()
    seances = Order.objects.filter(museum=museum, seance__date=date)
    print(seances)
    return 0


@login_required
def export(request):
    if request.method == 'GET':
        current_museums = Museum.objects.all()
        current_museums_list = {i.pk: i.name for i in current_museums}
        context = {'museums': current_museums_list}
        return render(request, 'export.html', context)
    elif request.method == 'POST':
        museum = str(request.POST.get("museum"))
        date = str(request.POST.get("date_input"))
        email = str(request.POST.get("email_input"))
        export_file_url = export_to_csv(museum, date)
        context = {"date": date, "museum": museum, "export_file_url": export_file_url}
        return render(request, 'download.html', context)
