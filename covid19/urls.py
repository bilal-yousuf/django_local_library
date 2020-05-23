from django.urls import path
from . import views

urlpatterns = [
	path('quebec-tracker/', views.quebec_tracker, name='quebec-tracker')

]