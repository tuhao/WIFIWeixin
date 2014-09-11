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
        	result.update(latitude=360,longtitude=360)
       		return result
        return json.JSONEncoder.default(self, obj)

EARTH_RADIUS = 6371.0 #
IMAGE_PATH = 'http://61.191.55.81:8080/merchant/Public/'

def merchant_nearest_json(request):
	distance = request.REQUEST.get('distance',None)
	latitude = request.REQUEST.get('latitude',None)
	longtitude = request.REQUEST.get('longtitude',None)
	sort_id = request.REQUEST.get('sort_id',None)
	city_id = request.REQUEST.get('city_id',None)
	merchant_locations = list()
	if distance and latitude and longtitude:
		latitude = float(latitude)
		longtitude = float(longtitude)
		distance = float(distance)
		dlng = 2 * math.asin(math.sin(distance / (2 * EARTH_RADIUS)) / math.cos(latitude))
		dlng = math.degrees(dlng)
		dlat = distance / EARTH_RADIUS
		dlat = math.degrees(dlat)
		latt_start = latitude - dlat
		latt_end = latitude + dlat
		long_start = longtitude - dlng
		long_end = longtitude + dlng
		locations = Location.objects.filter(latitude__gte=latt_start).filter(latitude__lte=latt_end).filter(longtitude__gte=long_start).filter(longtitude__lte=long_end)
		
		for location in locations:
			if sort_id and int(sort_id) > 0 and location.merchant.sort_id != int(sort_id):
				continue
			merchant = Merchant.objects.get(id=location.merchant.id)
			if city_id and int(city_id) > 0 and  merchant.city_id != int(city_id):
				continue
			else:
				merchant_location = MerchantLocation(merchant,location.latitude,location.longtitude)
			merchant_locations.append(merchant_location)
			for item in merchant_locations:
				image_url = str(item.__dict__.get('image_url'))
				if not image_url.startswith('http://'):
					item.__dict__.update(image_url = IMAGE_PATH + image_url)
	elif city_id:
		if sort_id and int(sort_id) > 0:
			merchant_locations = list(Merchant.objects.filter(city_id=city_id).filter(sort_id=int(sort_id))[:50])
		else:
			merchant_locations = list(Merchant.objects.filter(city_id=city_id)[:50])
		for item in merchant_locations:
			image_url = str(item.image_url)
			if not image_url.startswith('http://'):
				item.image_url = IMAGE_PATH + image_url
	return HttpResponse(json.dumps(merchant_locations,cls=MerchantLocationEncoder), content_type="application/json")

def merchant_detail_json(request):
	try:
		merchant_location = None
		merchant_id = request.REQUEST.get('id',None)
		if merchant_id:
			merchant = Merchant.objects.get(id=int(merchant_id))
			location = Location.objects.get(merchant=merchant)
			merchant_location = MerchantLocation(merchant,location.latitude,location.longtitude)
			image_url = str(merchant_location.__dict__.get('image_url'))
			if not image_url.startswith('http://'):
				merchant_location.__dict__.update(image_url = IMAGE_PATH + image_url)
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
			result.update(sort_id=obj.id,name=obj.name,icon_url=obj.icon_url)
			return result
		return json.JSONEncoder.default(self,obj)

def merchant_sort_json(request):
	sorts = list(Sort.objects.order_by('id'))
	return HttpResponse(json.dumps(sorts,cls=MerchantSortEncoder),content_type="application/json")

class CityEncoder(json.JSONEncoder):
	def default(self,obj):
		result = dict()
		if isinstance (obj,City):
			result.update(city_id=obj.id,city_name=obj.name,city_code=obj.code)
			return result
		return json.JSONEncoder.default(self,obj)	
	
def merchant_city_json(request):
	citys = list(City.objects.all())
	return HttpResponse(json.dumps(citys,cls=CityEncoder),content_type="application/json")

def merchant_city_detail_json(request):
	city_code = request.REQUEST.get('city_code',None)
	city = None
	if city_code:
		city = City.objects.get(code = city_code)
	return HttpResponse(json.dumps(city,cls=CityEncoder),content_type="application/json")

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

class FansEncoder(json.JSONEncoder):
	def default(self,obj):
		result = dict()
		if isinstance(obj,Fans):
			result.update(user_id=obj.appuser.id,merchant_id=obj.merchant.id)
			return result
		return json.JSONEncoder.default(self,obj)

def merchant_fans_add(request):
	username = request.REQUEST.get('username',None)
	merchant_id = request.REQUEST.get('merchant_id',None)
	if username and merchant_id:
		try:
			fans = list()
			user = AppUser.objects.get(username=username)
			merchant = Merchant.objects.get(id=merchant_id)
			if user and merchant:
				fans = list(Fans.objects.filter(appuser__id=user.id,merchant__id=merchant_id))
			if len(fans) > 0:
				pass
			else:
				fan = Fans(appuser=user,merchant=merchant,createtime=None)
				fan.save()
				fans.append(fan)
			return HttpResponse(json.dumps(fans[0],cls=FansEncoder),content_type="application/json")
		except Exception, e:
			return HttpResponse(e)
	return HttpResponse('invalidate args')

def merchant_fans_cancel(request):
	username = request.REQUEST.get('username',None)
	merchant_id = request.REQUEST.get('merchant_id',None)
	if username and merchant_id:
		try:
			user = AppUser.objects.get(username=username)
			fans = Fans.objects.filter(appuser__id=user.id,merchant__id=merchant_id)
			if fans and len(fans) > 0:
				fans[0].delete()
				return HttpResponse(json.dumps(fans[0],cls=FansEncoder),content_type="application/json")
			else:
				return HttpResponse('not found')
		except Exception, e:
			return HttpResponse(e)
	return HttpResponse('invalidate args')

def merchant_fans_json(request):
	username = request.REQUEST.get('username',None)
	merchant_id = request.REQUEST.get('merchant_id',None)
	fans = list()
	try:
		if merchant_id:
			fans = Fans.objects.filter(merchant__id=merchant_id)
		elif username:
			user = AppUser.objects.get(username=username)
			fans = Fans.objects.filter(appuser__id=user.id)
	except Exception, e:
		print e
	return HttpResponse(json.dumps(list(fans),cls=FansEncoder),content_type="application/json")

def merchant_mac(request):
	mac = request.REQUEST.get('mac',None)
	try:
		devices = Device.objects.filter(mac=mac)
		if len(devices) > 0:
			return HttpResponse(devices[0].merchant_id,content_type="application/json")
		else:
			return HttpResponse("-1")
	except Exception, e:
		print e
	return HttpResponse('-1')
	

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