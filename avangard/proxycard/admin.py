from django.contrib import admin
from .models import PcOrder


class PcOrderAdmin(admin.ModelAdmin):
    readonly_fields = ('added',)


admin.site.register(PcOrder, PcOrderAdmin)
