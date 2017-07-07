import django_tables2 as tables
from .models import Museum
from django_tables2.utils import A


class MuseumTable(tables.Table):
    name = tables.LinkColumn('museum_schedule', args=[A('pk')] , attrs={
            "td": {"style": "width:15%"}
        })
    operations = tables.TemplateColumn(template_name='operations_column.html', verbose_name=(' '), attrs={
            "td": {"align": "right", "style": "width:25%"}
        })

    class Meta:
        model = Museum
        fields = ('name', 'fullticket_price', 'reduceticket_price', 'audioguide_price', 'accompanying_guide_price', 'operations')
