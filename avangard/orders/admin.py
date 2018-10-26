from django.contrib import admin
from .models import Order, SuperOrder

# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('added', 'updated', 'full_price')


class SuperOrderAdmin(admin.ModelAdmin):
    readonly_fields = ('added', 'updated')


admin.site.register(Order, OrderAdmin)
admin.site.register(SuperOrder, SuperOrderAdmin)

