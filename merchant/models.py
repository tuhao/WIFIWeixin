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

class InnerSort(models.Model):
	sort = models.ForeignKey(Sort)
	name = models.CharField(max_length=100)
	icon_url = models.CharField(max_length=256,null=True)
	def __unicode__(self):
		return self.name

class Merchant(models.Model):
	sort = models.ForeignKey(Sort)
	city = models.ForeignKey(City)
	inner_sort = models.ForeignKey(InnerSort)
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

	def __unicode__(self):
		return self.mac

class Location(models.Model):
	merchant = models.ForeignKey(Merchant)
	latitude = models.CharField(max_length=20)
	longtitude = models.CharField(max_length=20)

	def __unicode__(self):
		return self.merchant.name

class AuthType(models.Model):
	name = models.CharField(max_length=50)
	auth_value = models.IntegerField()

	def __unicode__(self):
		return self.name

class AppUser(models.Model):
	auth_value = models.IntegerField()
	username = models.CharField(max_length=200)
	email = models.CharField(max_length=100,null=True)
	password = models.CharField(max_length=64,null=True)
	gender = models.CharField(max_length=10,null=True)
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

class UserClient(models.Model):
	appuser = models.ForeignKey(AppUser)
	client_id = models.CharField(max_length=100)
	createtime = models.DateTimeField(auto_now_add=True,null = True)

	def __unicode__(self):
		return self.appuser.username

class Fans(models.Model):
	appuser = models.ForeignKey(AppUser)
	merchant = models.ForeignKey(Merchant)
	createtime = models.DateTimeField(auto_now_add=True,null=True)

	def __unicode__(self):
		return self.appuser.username

class Send(models.Model):
	merchant = models.ForeignKey(Merchant)
	task_id = models.CharField(max_length=100)
	title = models.CharField(max_length=40)
	content = models.CharField(max_length=600)
	tags = models.CharField(max_length=1000,null=True)
	payload = models.CharField(max_length=2048,null=True)
	createtime = models.DateTimeField(auto_now_add=True,null=True)

	def __unicode__(self):
		return self.title


class Good(models.Model):
	merchant = models.ForeignKey(Merchant)
	image_url = models.CharField(max_length=500,null=True)
	title = models.CharField(max_length=100)
	name = models.CharField(max_length=500)
	description = models.CharField(max_length=2000)
	origin_price = models.CharField(max_length=10)
	on_promotion = models.CharField(max_length=10)
	promotion_price = models.CharField(max_length=10,null=True)
	promotion_deadline = models.DateTimeField(null=True)
	createtime = models.DateTimeField(auto_now_add=True,null=True)

	def __unicode__(self):
		return self.title

class Comment(models.Model):
	merchant = models.ForeignKey(Merchant)
	image_url = models.CharField(max_length=500,null=True)
	appuser = models.ForeignKey(AppUser)
	content = models.CharField(max_length=500)
	star = models.CharField(max_length=10)
	createtime = models.DateTimeField(auto_now_add=True,null=True)

	def __unicode__(self):
		return self.content

class GoodsComment(models.Model):
	good = models.ForeignKey(Good)
	image_url = models.CharField(max_length=500,null=True)
	appuser = models.ForeignKey(AppUser)
	content = models.CharField(max_length=500)
	star = models.CharField(max_length=10)
	createtime = models.DateTimeField(auto_now_add=True,null=True)

	def __unicode__(self):
		return self.content