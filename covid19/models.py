from django.db import models

# Create your models here.

class Data(models.Model):
	date = models.DateField(auto_now_add=True, help_text="Date statistics were collected.")
	confirmed_cases = models.CharField('Confirmed Cases', max_length=20, help_text="Total number of confirmed cases in a given day.",  default=None, blank=True, null=True)
	total_deaths = models.CharField('Total Deaths', max_length=20, help_text="Total number of deaths.", default=None, blank=True, null=True)


	class Meta:
		ordering = ['-date']
		verbose_name_plural = "data"

	def __str__(self):
		return str(self.date)

