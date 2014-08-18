from django.db import models

# Create your models here.
class Apk(models.Model):
	name = models.CharField(max_length=100)
	version_code = models.IntegerField(null=False)
	version_name = models.CharField(max_length=20)
	apk = models.FileField(upload_to='apk')
	detail = models.CharField(max_length=100)
	create_time = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.name