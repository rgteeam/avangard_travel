from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def settings_index(request):
    if request.method == 'GET':
        context = {'type': 'current'}
        return render(request, 'settings.html', context)
