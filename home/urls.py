from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index1'),
	path('cv', views.cv, name='resume'),

]