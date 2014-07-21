from django.contrib import admin
from merchant.models import *

class MerchantAdmin(admin.ModelAdmin):
	list_display = ('id','name','address','create_time')

admin.site.register(Merchant,MerchantAdmin)
admin.site.register(Device)
admin.site.register(Sort)

admin.site.register(Location)