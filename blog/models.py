from django.db import models
from django.urls import reverse
from datetime import date
from ckeditor.fields import RichTextField

# Create your models here.
class Post(models.Model):
	"""Model representing a blog post."""
	title = models.CharField(max_length=200)

	body = RichTextField(help_text="What is the body of your blog post?")

	pub_date = models.DateField(auto_now_add=True)
	pub_time = models.TimeField(auto_now_add=True)

	POST_STATUS = (
		('b', 'Blog post'),
		('n', 'Note'),
		)
	status = models.CharField(
		max_length=1,
		choices=POST_STATUS,
		blank=True,
		default='n',
		help_text="Blog post or note?"
		)

	def get_absolute_url(self):
		return reverse('blog-detail', args=[str(self.id)])


	def __str__(self):
		return self.title

	class Meta:
		ordering = ['-pub_date', '-pub_time']