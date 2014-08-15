from upgrade.models import *
from django.shortcuts import render_to_response
from django.http import HttpResponse
import json


def apk_version(request):
	try:
		apks = Apk.objects.order_by('-version_code')[:1]
		if apks and len(apks) > 0:
			apk = apks[0]
		return HttpResponse(json.dumps(apk,cls=ApkEncoder),content_type="application/json")
	except Exception, e:
		return HttpResponse(e)
	
class ApkEncoder(json.JSONEncoder):
	
	def default(self,obj):
		result = dict()
		if isinstance(obj,Apk):
			result.update(name=obj.name,version_code=obj.version_code)
			result.update(version_name=obj.version_name,create_time=str(obj.create_time))
			result.update(url=obj.apk.url)
			return result
		return json.JSONEncoder.default(self,obj)

