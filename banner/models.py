from django.db import models
# Create your models here.

class Sort(models.Model):
	name = models.CharField(max_length=256)

	def __unicode__(self):
		return self.name

class Ads(models.Model):
	name = models.CharField(max_length=256)
	url = models.CharField(max_length=500)
	createtime = models.DateTimeField(auto_now_add=True,null=True)
	sort = models.ForeignKey(Sort)

	def __unicode__(self):
		return self.name

