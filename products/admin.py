from django.contrib import admin
from .models import *

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "obiem", "bool_status")
    search_fields = ("name", )

    def bool_status(self, obj):
        if obj.pr_status.status_id == 1:
            return True
        else:
            return False
    bool_status.boolean = True

admin.site.register(Product, ProductAdmin)
admin.site.register(Series)
admin.site.register(Category)
admin.site.register(Destination)
admin.site.register(Prtype)
admin.site.register(Hairtype)
admin.site.register(Brand)
admin.site.register(Status)
