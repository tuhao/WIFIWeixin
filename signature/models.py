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


class Article(models.Model):
	title = models.CharField(max_length = 100)
	description = models.CharField(max_length=255,blank=True)
	pic = models.CharField(max_length=255,blank=False)
	url = models.CharField(max_length=255,blank=True)

	def __unicode__(self):
		return self.title