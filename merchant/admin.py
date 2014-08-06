from django.contrib import admin
from merchant.models import *

class MerchantAdmin(admin.ModelAdmin):
	list_display = ('id','name','city','address','create_time')

admin.site.register(City)
admin.site.register(Merchant,MerchantAdmin)
admin.site.register(Device)
admin.site.register(Sort)

admin.site.register(Location)

admin.site.register(AppUser)
admin.site.register(WifiUserLog)
admin.site.register(Fans)