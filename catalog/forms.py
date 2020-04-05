import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from catalog.models import BookInstance

class RenewBookModelForm(forms.ModelForm):
	
	def clean_renewal_date(self):
		data = self.cleaned_data['due_back']
        
    	# Check if a date is not in the past. 
		if data < datetime.date.today():
			raise ValidationError(_('Invalid date - renewal in past'))

        # Check if a date is in the allowed range (+4 weeks from today).
		if data > datetime.date.today() + datetime.timedelta(weeks=4):
			raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
		return data

	class Meta:
		model = BookInstance
		fields = ['due_back']
		labels = {'due_back': _('Renewal date')}
		help_texts = {'due_back': _('Enter a date between now and 4 weeks (default 3).')} 

class RequestBookCheckoutForm(forms.ModelForm):

	def clean_borrow_date(self):
		data = self.cleaned_data['borrowed_on']

		# ensure data is not in past
		if data < datetime.date.today():
			raise ValidationError(_('Invalid date - date cannot be in past'))

		if data > datetime.date.today() + datetime.timedelta(weeks=1):
			raise ValidationError(_('Invalid date - cannot request pickup more than 1 week ahead'))

		return data

	def clean_return_date(self):
		data = self.cleaned_data['due_back']

		# ensure data is not in past
		if data < datetime.date.today():
			raise ValidationError(_('Invalid date - date cannot be in past'))

		if data > datetime.date.today() + datetime.timedelta(weeks=4):
			raise ValidationError(_('Invalid date - cannot request return more than 4 weeks ahead'))

		return data

	class Meta:
		model = BookInstance
		fields = ['borrowed_on', 'due_back']
		labels = {'borrowed_on': _('Pickup date'),
			'due_back': _('Return date')
		}
		help_texts = {'borrowed_on': _('Enter a date within the next week'),
			'due_back': _('Enter a date between now and 4 weeks (default 3).')
		} 
	


