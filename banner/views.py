# Create your views here.
from banner.models import *
from django.shortcuts import HttpResponse
import json

def ads(request):
	ads = list()
	try:
		ads = list(Ads.objects.all())
	except Exception,e:
		return HttpResponse(e)
	return HttpResponse(json.dumps(ads,cls=AdsEncoder),content_type="application/json")

class AdsEncoder(json.JSONEncoder):
	def default(self,obj):
		if isinstance(obj,Ads):
			result = dict()
			result.update(id=obj.id,name=obj.name,url=obj.url,redirect_url=obj.redirect_url)
			return result
		return json.JSONEncoder.default(self, obj)

