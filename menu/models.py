from django.db import models

# Create your models here.

class Button(models.Model):
	name = models.CharField(max_length=16)

	def __unicode__(self):
		return self.name

class Click(models.Model):
	name = models.CharField(max_length=16)
	key = models.CharField(max_length=128)
	default_type = models.CharField(max_length=10,default='click')
	button_id = models.ForeignKey(Button)



class View(models.Model):
	name = models.CharField(max_length=16)
	url = models.CharField(max_length=255)
	default_type = models.CharField(max_length=10,default='view')
	button_id = models.ForeignKey(Button)
