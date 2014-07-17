from django.contrib import admin
from menu.models import *




class ClickAdmin(admin.ModelAdmin):
	list_display = ('id','name','key','default_type','button_id')

admin.site.register(Click,ClickAdmin)

class ViewAdmin(admin.ModelAdmin):
	list_display = ('id','name','url','default_type','button_id')

admin.site.register(View,ViewAdmin)

admin.site.register(Button)