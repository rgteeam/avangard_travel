from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from avangard.setting.models import OrderSettings


@login_required
def settings_index(request):
    if request.method == 'GET':
        current_value = OrderSettings.objects.latest('pk').prebuy_time
        context = {'prebuy_time': current_value}
        return render(request, 'settings.html', context)
    elif request.method == 'POST':
        exist_item = OrderSettings.objects.latest('pk')
        exist_item.prebuy_time = int(request.POST.get("prebuy_time_input"))
        exist_item.save()
        current_value = OrderSettings.objects.latest('pk').prebuy_time
        context = {'prebuy_time': current_value, 'type': 'updated'}
        return render(request, 'settings.html', context)
        print("post request")
