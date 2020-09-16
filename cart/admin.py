from django.contrib import admin
from .models import * 

# Register your models here.


class ItemInline(admin.TabularInline):
    model = Item

class OrdersAdmin(admin.ModelAdmin):
#   fieldsets = [
#       ('Покупатель', {'fields': ['name', 'phone', 'email']}),
#   ]  
  inlines = [ItemInline]

admin.site.register(Orders, OrdersAdmin)
admin.site.register(ViewedProduct)
admin.site.register(Promocode)
admin.site.register(Cart)
