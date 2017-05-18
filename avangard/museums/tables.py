import django_tables2 as tables
from .models import Museum, Schedule
from django_tables2.utils import A


class MuseumTable(tables.Table):
    name = tables.LinkColumn('museum_schedule', args=[A('pk')])

    class Meta:
        model = Museum