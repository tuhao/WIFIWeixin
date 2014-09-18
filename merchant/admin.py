from django.contrib import admin
from merchant.models import *

class MerchantAdmin(admin.ModelAdmin):
	list_display = ('id','name','city','address','create_time')

#admin.site.register(City)
admin.site.register(Merchant,MerchantAdmin)
admin.site.register(Device)
admin.site.register(Sort)

admin.site.register(Location)

admin.site.register(AppUser)

class WifiUserLogAdmin(admin.ModelAdmin):
	list_display = ('id','ip','device','appuser')

admin.site.register(WifiUserLog,WifiUserLogAdmin)

admin.site.register(Fans)

admin.site.register(AuthType)

admin.site.register(UserClient)