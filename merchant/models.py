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