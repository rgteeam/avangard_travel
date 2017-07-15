from django.contrib import admin
from .models import Order

# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('added', 'updated', 'full_price')

admin.site.register(Order, OrderAdmin)
