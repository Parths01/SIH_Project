from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='website_index'),
    path('about/', views.about, name='website_about'),
    path('features/', views.features, name='website_features'),
    path('contact/', views.contact, name='website_contact'),
]