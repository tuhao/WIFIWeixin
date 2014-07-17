#coding=utf-8
# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render_to_response
from signature.models import *
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from weixin import settings
from weixin import common_exception
import sha
import time
import xml.etree.ElementTree as ET
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

CONTENT_SWITCH = {
    '帮助':lambda req,param:reply_help(req,param),
	'help':lambda req,param:reply_help(req,param),
	}

EVENT_SWITCH = {
	'subscribe':lambda req,param:reply_welcome(req,param),
	'CLICK':None,
	'VIEW':None,
}

MSG_TYPE_SWITCH = {
	'text':CONTENT_SWITCH,
	'event':EVENT_SWITCH,
}

def enum(**enums):
	return type('Enum',(),enums)


@csrf_exempt
def check_signature(request):
	signature = request.REQUEST.get('signature',None)
	timestamp = request.REQUEST.get('timestamp',None)
	nonce = request.REQUEST.get('nonce',None)
	#echostr = request.REQUEST.get('echostr',None)    #connect
	if signature and timestamp and nonce:
		tmp_arr = list((settings.TOKEN,timestamp,nonce))
		tmp_arr = sorted(tmp_arr)
		tmp_str = ''
		for item in tmp_arr:
			tmp_str += item
		tmp_str =sha.new(tmp_str).hexdigest()
		if tmp_str == signature:
			#return HttpResponse(echostr)   #connect
			return reply(request)
		else:
			return HttpResponse('signature not correct')
	else:
		return HttpResponse('invalid request')


def reply(request):
	parse_result = parse_xml(request)
	if parse_result[1] is None:
		param = parse_result[0]
		msg_type_value = param['msg_type']   		# msg_type_value can be event or text.
		value = param.get(msg_type_value,None)		# get event value or text value
		if value:
			value = param[msg_type].encode('utf-8')
			processor_switch = MSG_TYPE_SWITCH.get(msg_type_value,None)
			if processor_switch:
				func = processor_switch.get(value.lower(),None)
				if func:
					return func(request,param)
				else:
					#if key[:2].lower() == 'ss':
					#	key = key[2:]
					#return reply_search(request, param, key)
					pass
			else:
				return HttpResponse(common_exception.UNSUPPORT_EVENT_TYPE)
		else:
			return HttpResponse(common_exception.UNSUPPORT_EVENT_TYPE)
	else:
		return HttpResponse(parse_result[1])

def parse_xml(request):
	try:
		doc = ET.parse(request)
	except Exception, e:
		return None,e
	else:
		to_user_name = doc.find('ToUserName')
		from_user_name = doc.find('FromUserName')
		msg_type = doc.find('MsgType')
		if msg_type is not None and to_user_name is not None and from_user_name is not None:
			param = dict(to_user_name=to_user_name.text,from_user_name=from_user_name.text,msg_type=msg_type.text)
			content = doc.find('Content')
			if content:
				param.update(text=content.text)
			event = doc.find('Event')
			if event:
				param.update(event=event.text)
			event_key = doc.find('EventKey')
			if event_key:
				param.update(event_key=event_key.text)
			return param,None
		else:
			return None,common_exception.MISSING_PARAMS



IMAGEURL = re.compile(r'h(?!.*http://).*\.jpg$')
def reply_gen_news(request,param,merchants):
	news_id = 1
	articles = list()
	for merchant in merchants:
		pic = None
		for image_url in IMAGEURL.findall(merchant.introduction):
			pic = image_url
			break
		#if pic is None:
		#	continue
		show = merchant.introduction[:25].encode('utf-8')
		title = show
		description = show
		url = "http://" + request.META.get('HTTP_HOST') + reverse('signature.views.merchant_detail',args=(msg.id,))
		article = Article(title=title,description=description,pic=pic,url=url)
		articles.append(article)
	from_user_name,to_user_name = param['to_user_name'],param['from_user_name']
	create_timestamp = int(time.time())
	return render_to_response('reply_news.xml',locals(),content_type='application/xml')

def merchant_detail(request,msg_id):
	try:
		merchant = Message.objects.get(id=msg_id)
	except Exception, e:
		return HttpResponse(e)
	else:
		
		return render_to_response('merchant_detail.html',locals())


#def reply_search(request,param,query):
#	if query is not None:
#		try:
#			r = Merchant.search.query(query)
#			results = list(r)[:6]
#		except Exception, e:
#                        print e
#			return HttpResponse(e)
#		else:
#			return reply_gen_news(request, param, results)
#	else:
#		return HttpResponse('unknown query string')

def reply_welcome(request,param):
	words = ""
	try:
		welcome = Welcome.objects.order_by('-id')[0]
		words += welcome.content
		help = Help.objects.order_by('-id')[0]
		words += help.content
	except Exception, e:
		raise e
	else:
		return reply_leave_message(request,param,words)

def reply_leave_message(request,param,words):
	content = words
	from_user_name,to_user_name = param['to_user_name'],param['from_user_name']
	create_timestamp = int(time.time())
	return render_to_response('reply_message.xml',locals(),content_type='application/xml')

def reply_help(request,param):
	try:
		help = Help.objects.order_by('-id')[0]
	except Exception, e:
		return HttpResponse(e)
	else:
		return reply_leave_message(request, param, help.content)