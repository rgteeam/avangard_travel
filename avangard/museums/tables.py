import django_tables2 as tables
from .models import Museum, Schedule
from django_tables2.utils import A


class MuseumTable(tables.Table):
    name = tables.LinkColumn('museum_schedule', args=[A('pk')])
    operations = tables.TemplateColumn(template_name='operations_column.html', verbose_name=(' '), attrs={
            "td": {"align": "right"}
        })

    class Meta:
        model = Museum
        fields = ('name', 'fullticket_price', 'full_coefficient', 'reduceticket_price', 'reduce_coefficient', 'audioguide_price', 'accompanying_guide_price', 'operations')