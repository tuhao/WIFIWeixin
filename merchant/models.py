from django.db import models

class Sort(models.Model):
	name = models.CharField(max_length=100)
	def __unicode__(self):
		return self.name

class Merchant(models.Model):
	sort = models.ForeignKey(Sort) 
	name = models.CharField(max_length=255)
	introduction = models.CharField(max_length=255)
	password = models.CharField(max_length=100)
	address = models.CharField(max_length=255)
	contact = models.CharField(max_length=255)
	create_time = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.name
	

class Device(models.Model):
	merchant = models.ForeignKey(Merchant)
	mac = models.CharField(max_length=100)
	key = models.CharField(max_length=255)

	def __unicode__(self):
		return self.merchant.name

class Location(models.Model):
	merchant = models.ForeignKey(Merchant)
	latitude = models.CharField(max_length=20)
	longtitude = models.CharField(max_length=20)
	precision = models.CharField(max_length=20)

	def __unicode__(self):
		return self.merchant.name

class AppUser(models.Model):
	username = models.CharField(max_length=20)
	password = models.CharField(max_length=30)
	description = models.CharField(max_length=200,null=True)
	createtime = models.DateTimeField(auto_now_add=True,null=True)

	def __unicode__(self):
		return self.username

class WifiUser(models.Model):
	phonemac = models.CharField(max_length=50)
	online_time = models.IntegerField(default=0)
	appuser = models.ForeignKey(AppUser)
	status = models.IntegerField(default=0)
	isonline = models.IntegerField(default=0)
	broadbandlimit = models.IntegerField(default=0)
	ip = models.CharField(max_length=32)
	device = models.ForeignKey(Device) 

	def __unicode__(self):
		return self.appuser.username

class Fans(models.Model):
	appuser = models.ForeignKey(AppUser)
	merchant = models.ForeignKey(Merchant)
	createtime = models.DateTimeField(auto_now_add=True,null=True)

	def __unicode__(self):
		return self.appuser.username
