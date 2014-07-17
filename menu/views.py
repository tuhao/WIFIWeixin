#coding=utf-8
# Create your views here.

from menu.models import *
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from weixin import settings
from weixin import common_exception
import requests
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

@csrf_exempt
def create_menu(request):
	result = generate_menu()
	if type(result) is dict:
		post_data = json.dumps(result)
		url = settings.CREATE_MENU_URL
		headers = {'content-type':'application/json'}
		response = requests.post(url,data=post_data,headers=headers)
		result = response.text
	return render_to_response('menu_result.html',locals())

def delete_menu(request):
	url = settings.DELETE_MENU_URL
	response = requests.get(url)
	result = response.text
	return render_to_response('menu_result.html',locals())

def generate_menu():
	buttons = Button.objects.order_by('id')
	if len(buttons) > 3:
		result = common_exception.BUTTON_TOO_MANY
		return render_to_response('menu_result.html',locals())
	result = {'button':list()}
	for button in buttons:
		clicks = Click.objects.filter(button_id=button.id)
		views = View.objects.filter(button_id=button.id)
		button_count = len(clicks) + len(views)
		if(button_count == 0):
			result = common_exception.EMPTY_BUTTON
			break
		if(button_count > 3):
			result = common_exception.SUB_BUTTON_TOO_MANY
			break
		if button_count == 1:
			data_list = list()
			data_list.extend(generate_data(views=views, clicks=clicks))
			result.get('button').append(data_list[0])
		else:
			data = {'name':button.name,'sub_button':list()}
			data.get('sub_button').extend(generate_data(views=views, clicks=clicks))
			result.get('button').append(data)
	return result

def generate_data(views,clicks):
	data = list()
	for view in views:
		data.append({'type':view.default_type,'name':view.name,'url':view.url})
	for click in clicks:
		data.append({'type':click.default_type,'name':click.name,'key':click.key})
	return data

