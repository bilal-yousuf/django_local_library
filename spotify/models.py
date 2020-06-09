from django.db import models


# Create your models here.
class CurrentAlbum(models.Model):
	"""Model representing top albums I am currently listening to."""
	title = models.CharField(max_length=200, help_text='Album name')
	artist = models.CharField(max_length=200, help_text='Album artist')
	img_url = models.CharField(max_length=200)
	year = models.CharField(max_length=4)
	external_url = models.CharField(max_length=200)

	def __str__(self):
		return self.title
