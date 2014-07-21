from merchant.models import *
from django.shortcuts import render_to_response
from django.http import HttpResponse

def merchant_detail(request,merchant_id):
	try:
		merchant = Merchant.objects.get(id=merchant_id)
	except Exception, e:
		return HttpResponse(e)
	else:
		return render_to_response('merchant_detail.html',locals())

def merchant_list(request):
	merchants = Merchant.objects.order_by('id')
	return render_to_response('merchant_list.html',locals())

def merchant_location(request,merchant_id):
	try:
		location = Location.objects.get(id=merchant_id)
	except Exception, e:
		return HttpResponse(e)
	else:
		return render_to_response('merchant_location.html',locals())