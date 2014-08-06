from django.db import models

class City(models.Model):
	id = models.IntegerField(primary_key=True)
	code = models.CharField(max_length=10)
	name = models.CharField(max_length=100)
	
	def __unicode__(self):
		return self.name


class Sort(models.Model):
	name = models.CharField(max_length=100)
	icon_url = models.CharField(max_length=255,null=True)
	def __unicode__(self):
		return self.name

class Merchant(models.Model):
	sort = models.ForeignKey(Sort) 
	city = models.ForeignKey(City)
	email = models.CharField(max_length=50)
	name = models.CharField(max_length=50)
	introduction = models.CharField(max_length=255)
	password = models.CharField(max_length=100)
	address = models.CharField(max_length=255)
	contact = models.CharField(max_length=255)
	image_url = models.CharField(max_length=255,null=True)
	create_time = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.name
	

class Device(models.Model):
	merchant_id = models.IntegerField(default=0)
	mac = models.CharField(max_length=50)
	status = models.IntegerField(default=0)

class Location(models.Model):
	merchant = models.ForeignKey(Merchant)
	latitude = models.CharField(max_length=20)
	longtitude = models.CharField(max_length=20)

	def __unicode__(self):
		return self.merchant.name

class AppUser(models.Model):
	username = models.CharField(max_length=50)
	password = models.CharField(max_length=64)
	description = models.CharField(max_length=200,null=True)
	createtime = models.DateTimeField(auto_now_add=True,null=True)

	def __unicode__(self):
		return self.username

class WifiUserLog(models.Model):
	phonemac = models.CharField(max_length=50,null=True)
	appuser = models.CharField(max_length=50,null=True)
	device = models.CharField(max_length=64,null=True) 
	ip = models.CharField(max_length=64,null=True)
	incoming = models.IntegerField(default=0,null=True)
	outgoing = models.IntegerField(default=0,null=True)
	login_time = models.DateTimeField(null=True)
	online_time = models.IntegerField(default=0,null=True)
	isonline = models.IntegerField(default=0,null=True)

	def __unicode__(self):
		return self.appuser

class Fans(models.Model):
	appuser = models.ForeignKey(AppUser)
	merchant = models.ForeignKey(Merchant)
	createtime = models.DateTimeField(auto_now_add=True,null=True)

	def __unicode__(self):
		return self.appuser.username

