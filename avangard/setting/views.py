from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from avangard.setting.models import OrderSettings
from avangard.museums.models import Company
from avangard.orders.models import Order


@login_required
def settings_index(request):
    if request.method == 'GET':
        current_prebuy_time_value = OrderSettings.objects.latest('pk').prebuy_time
        current_companies = Company.objects.all()
        current_companies_str = ", ".join(i.name for i in current_companies)
        context = {'prebuy_time': current_prebuy_time_value, 'current_companies': current_companies_str, }
        return render(request, 'settings.html', context)
    elif request.method == 'POST':
        exist_item = OrderSettings.objects.latest('pk')
        exist_item.prebuy_time = int(request.POST.get("prebuy_time_input"))
        exist_item.save()
        current_value = OrderSettings.objects.latest('pk').prebuy_time
        new_companies = str(request.POST.get("companies_input"))
        for i in new_companies.split(', '):
            try:
                Company.objects.get(name=i)
            except Company.DoesNotExist:
                new_company = Company(name=i)
                new_company.save()
        current_companies = Company.objects.all()
        current_companies_str = ", ".join(i.name for i in current_companies)
        context = {'prebuy_time': current_value, 'current_companies': current_companies_str, 'type': 'updated'}
        return render(request, 'settings.html', context)
