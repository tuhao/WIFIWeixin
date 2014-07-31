from merchant.models import *
from django.shortcuts import render_to_response
from django.http import HttpResponse
import math
import json

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

def merchant_distance(request):
	latitude = request.REQUEST.get('latitude',None)
	longtitude = request.REQUEST.get('longtitude',None)
	if latitude and longtitude:
		latitude = float(latitude)
		longtitude = float(longtitude)
		latt_start = latitude - 0.2
		latt_end = latitude + 0.2
		long_start = longtitude - 0.2
		long_end = longtitude + 0.2
		locations = Location.objects.filter(latitude__gte=latt_start).filter(latitude__lte=latt_end).filter(longtitude__gte=long_start).filter(longtitude__lte=long_end)
		user_location_dms = (deg_to_dms(latitude),deg_to_dms(longtitude))
		merchants = list()
		for location in locations:
			merchant = Merchant.objects.get(id=location.merchant.id)
			merchant_location_dms = (deg_to_dms(float(location.latitude)),deg_to_dms(float(location.longtitude)))
			merchant.distance = int(points2distance(user_location_dms,merchant_location_dms) * 1000)
			merchants.append(merchant)
		merchants.sort(cmp=lambda x,y:cmp(x.distance,y.distance), reverse=False)
	else:
		merchants = Merchant.objects.order_by('id')
	return render_to_response('merchant_list.html',locals())

class MerchantLocation(Merchant):

	latitude = 0
	longtitude = 0

	def __init__(self,merchant,latitude,longtitude):
		self.__dict__ = merchant.__dict__.copy()
		self.longtitude = longtitude
		self.latitude = latitude


class MerchantLocationEncoder(json.JSONEncoder):  
    def default(self, obj):  
    	result = dict()
    	result.update(id=obj.id,sort_id=obj.sort.id,name=obj.name,address=obj.address)
        result.update(introduction=obj.introduction,contact=obj.contact,image_url=obj.image_url)
        if isinstance(obj, MerchantLocation):  
        	result.update(latitude=float(obj.latitude),longtitude=float(obj.longtitude))
        	return result
        if isinstance(obj, Merchant):
        	result.update(latitude=None,longtitude=None)
       		return result
        return json.JSONEncoder.default(self, obj)

def merchant_nearest_json(request):
	scale = request.REQUEST.get('scale',None)
	latitude = request.REQUEST.get('latitude',None)
	longtitude = request.REQUEST.get('longtitude',None)
	sort_id = request.REQUEST.get('sort_id',None)
	if scale and latitude and longtitude:
		scale = float(scale)
		latitude = float(latitude)
		longtitude = float(longtitude)
		latt_start = latitude - scale
		latt_end = latitude + scale
		long_start = longtitude - scale
		long_end = longtitude + scale
		if sort_id and int(sort_id) > 0:
			locations = Location.objects.filter(latitude__gte=latt_start).filter(latitude__lte=latt_end).filter(longtitude__gte=long_start).filter(longtitude__lte=long_end).filter(merchant__sort=sort_id)
		else:
			locations = Location.objects.filter(latitude__gte=latt_start).filter(latitude__lte=latt_end).filter(longtitude__gte=long_start).filter(longtitude__lte=long_end)
		merchant_locations = list()
		for location in locations:
			merchant = Merchant.objects.get(id=location.merchant.id)
			merchant_location = MerchantLocation(merchant,location.latitude,location.longtitude)
			merchant_locations.append(merchant_location)
	else:
		merchant_locations = list(Merchant.objects.order_by('-id')[:20])
	return HttpResponse(json.dumps(merchant_locations,cls=MerchantLocationEncoder), content_type="application/json")

def merchant_detail_json(request):
	try:
		merchant_location = None
		merchant_id = request.REQUEST.get('id',None)
		if merchant_id:
			merchant = Merchant.objects.get(id=int(merchant_id))
			location = Location.objects.get(merchant=merchant)
			merchant_location = MerchantLocation(merchant,location.latitude,location.longtitude)
		else:
			return HttpResponse('merchant_id not validate')
	except Exception, e:
		return HttpResponse(e)
	else:
		return HttpResponse(json.dumps(merchant_location,cls=MerchantLocationEncoder),content_type="application/json")

class MerchantSortEncoder(json.JSONEncoder):
	def default(self,obj):
		result = dict()
		if isinstance (obj,Sort):
			result.update(sort_id=obj.id,name=obj.name)
			return result
		return json.JSONEncoder.default(self,obj)

def merchant_sort_json(request):
	sorts = list(Sort.objects.order_by('id'))
	return HttpResponse(json.dumps(sorts,cls=MerchantSortEncoder),content_type="application/json")
	

def merchant_amap_location(request,merchant_id):
	try:
		location = Location.objects.get(id=merchant_id)
	except Exception, e:
		return HttpResponse(e)
	else:
		return render_to_response('merchant_amap_location.html',locals())

def merchant_baidu_location(request,merchant_id):
	try:
		location = Location.objects.get(id=merchant_id)
	except Exception, e:
		return HttpResponse(e)
	else:
		return render_to_response('merchant_baidu_location.html',locals())



def recalculate_coordinate(val,  _as=None):
  deg,  min,  sec = val
  # pass outstanding values from right to left
  min = (min or 0) + int(sec) / 60
  sec = sec % 60
  deg = (deg or 0) + int(min) / 60
  min = min % 60
  # pass decimal part from left to right
  dfrac,  dint = math.modf(deg)
  min = min + dfrac * 60
  deg = dint
  mfrac,  mint = math.modf(min)
  sec = sec + mfrac * 60
  min = mint
  if _as:
    sec = sec + min * 60 + deg * 3600
    if _as == 'sec': return sec
    if _as == 'min': return sec / 60
    if _as == 'deg': return sec / 3600
  return deg,  min,  sec
      

def points2distance(start,  end):
  start_long = math.radians(recalculate_coordinate(start[0],  'deg'))
  start_latt = math.radians(recalculate_coordinate(start[1],  'deg'))
  end_long = math.radians(recalculate_coordinate(end[0],  'deg'))
  end_latt = math.radians(recalculate_coordinate(end[1],  'deg'))
  d_latt = end_latt - start_latt
  d_long = end_long - start_long
  a = math.sin(d_latt/2)**2 + math.cos(start_latt) * math.cos(end_latt) * math.sin(d_long/2)**2
  c = 2 * math.asin(math.sqrt(a))
  return 6371 * c

def deg_to_dms(deg):
    d = int(deg)
    md = abs(deg - d) * 60
    m = int(md)
    sd = (md - m) * 60
    return (d, m, sd)