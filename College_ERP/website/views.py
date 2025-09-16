from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    """Homepage view"""
    return render(request, 'website/index.html')

def about(request):
    """About page view"""
    return render(request, 'website/about.html')

def features(request):
    """Features page view"""
    return render(request, 'website/features.html')

def contact(request):
    """Contact page view"""
    return render(request, 'website/contact.html')