from django.db import models

# Create your models here.

class Welcome(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField(u'welcome',max_length=1000,blank=False)

	def __unicode__(self):
		return self.title

class Help(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField(u'help',max_length=1000,blank=False)

	def __unicode__(self):
		return self.title

class Sort(models.Model):
	sid = models.IntegerField(default=0)
	name = models.CharField(max_length=100)
	def __unicode__(self):
		return self.name

class Merchant(models.Model):
	mid = models.CharField(max_length=100)
	sort = models.ForeignKey(Sort) 
	name = models.CharField(max_length=255)
	introduction = models.CharField(max_length=255)
	password = models.CharField(max_length=100)
	address = models.CharField(max_length=255)
	contact = models.CharField(max_length=255)
	create_time = models.DateTimeField(auto_now_add=True)
	

class MerchantWIFI(models.Model):
	wid = models.CharField(max_length=100)
	mid = models.ForeignKey(Merchant)
	mac = models.CharField(max_length=100)
	key = models.CharField(max_length=255)

	def __unicode__(self):
		return self.wid

class Article(models.Model):
	news = models.ForeignKey(News)
	title = models.CharField(max_length = 100)
	description = models.CharField(max_length=255,blank=True)
	pic = models.CharField(max_length=255,blank=False)
	url = models.CharField(max_length=255,blank=True)

	def __unicode__(self):
		return self.title