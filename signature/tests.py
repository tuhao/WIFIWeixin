#coding=utf-8
import re
import sys
from math import sin, asin, cos, radians, fabs, sqrt  

reload(sys)
sys.setdefaultencode='utf-8'

#DATA_REGEX = re.compile(r'"code":"(\d+)","city":"(\W+)",')
#with open('d:/amapcitycode.txt','r') as f:
#	line = f.read()
#	count = 1
#	for item in DATA_REGEX.findall(line):
#		print "insert into `merchant_city` values(" + str(count) + ",'" + item[0] + "','" + item[1] + "');"
#		count = count + 1

EARTH_RADIUS=6371.0

distance = 100
lat = 31.0
dlng = 2 * asin(sin(distance / (2 * EARTH_RADIUS)) / cos(lat))
#dlng = degrees(dlng)        # 弧度转换成角度 
dlat = distance / EARTH_RADIUS
#dlat = degrees(dlat)     # 弧度转换成角度 
print dlat,dlng

if 1 is not 2 :
	print 'not'