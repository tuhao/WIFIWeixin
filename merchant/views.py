from merchant.models import *
from django.shortcuts import render_to_response
from django.http import HttpResponse
import math

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
	print latitude,longtitude
	if latitude and longtitude:
		latitude = float(latitude)
		longtitude = float(longtitude)
		latt_start = latitude - 0.1
		latt_end = latitude + 0.1
		long_start = longtitude - 0.1
		long_end = longtitude + 0.1
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
		locations = Location.objects.order_by('id')
	return render_to_response('merchant_list.html',locals())

def merchant_location(request,merchant_id):
	try:
		location = Location.objects.get(id=merchant_id)
	except Exception, e:
		return HttpResponse(e)
	else:
		return render_to_response('merchant_location.html',locals())

import math

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