from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
import json
from avangard.museums.models import Museum
from rest_framework import generics, viewsets, status
from rest_framework.decorators import api_view
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.views import APIView
from avangard.museums.serializers import MuseumSerializer
from avangard.museums.forms import MuseumForm
from avangard.museums.tables import MuseumTable
from django_tables2 import RequestConfig

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'museums': reverse('museum-list', request=request),
    })

class MuseumViewSet(viewsets.ModelViewSet):
    queryset = Museum.objects.all()
    serializer_class = MuseumSerializer


@login_required
def museum_schedule(request, museum_id):
    museum = Museum.objects.get(pk=museum_id)
    context = {'museum': museum}
    return render(request,'schedule.html', context)


@login_required
def index(request):
    table = MuseumTable(Museum.objects.all())
    RequestConfig(request, paginate={"per_page": 25}).configure(table)
    return render(request, 'museums.html', {'table': table})

@login_required
def create_museum_view(request):
    if request.method == 'GET':
        return render(request, 'create.html')
    elif request.method == 'POST':
        museum_formset = MuseumForm(request.POST)
        museum_formset.save()
        return redirect('index')
