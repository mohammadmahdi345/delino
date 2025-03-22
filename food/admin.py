from django.contrib import admin

from .models import Restorant, City, Food, Order

admin.site.register(Food)
admin.site.register(City)
admin.site.register(Order)
class ResAdmin(admin.ModelAdmin):

    filter_horizontal = ['meno']

admin.site.register(Restorant,ResAdmin)