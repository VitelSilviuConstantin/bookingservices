from django.urls import path

from . import views

urlpatterns = [
	path('remind/', views.remind, name='remind'),
	path('statistics/', views.statistics, name='statistics')
]