from django.contrib import admin
from signature.models import *


admin.site.register(Help)
admin.site.register(Welcome)

class MerchantAdmin(admin.ModelAdmin):
	list_display = ('id','name','create_time')

admin.site.register(Merchant,MerchantAdmin)
admin.site.register(MerchantWIFI)
admin.site.register(Sort)