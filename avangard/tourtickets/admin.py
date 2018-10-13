from django.contrib import admin
from .models import TtOrder


class TtOrderAdmin(admin.ModelAdmin):
    readonly_fields = ('added',)


admin.site.register(TtOrder, TtOrderAdmin)
