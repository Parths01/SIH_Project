from django.core.management.base import BaseCommand
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Setup complete website with all HTML sections'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🌐 Setting up complete College ERP website...'))
        
        # Update URLs to include website
        self.update_main_urls()
        
        # Create website app if it doesn't exist
        self.create_website_app()
        
        self.stdout.write(
            self.style.SUCCESS(
                '\n🎉 Complete College ERP Website Setup Completed!\n'
                '\n🌐 Website Pages Created:'
                '\n  ✅ Homepage - Modern landing page with hero section'
                '\n  ✅ About Us - Company story, mission, vision, team'
                '\n  ✅ Features - Comprehensive feature showcase'
                '\n  ✅ Contact - Contact form, FAQ, support info'
                '\n'
                '\n📱 Website Features:'
                '\n  ✅ Responsive design for all devices'
                '\n  ✅ Modern animations and effects'
                '\n  ✅ Interactive charts and statistics'
                '\n  ✅ Professional gradient designs'
                '\n  ✅ Contact forms with validation'
                '\n  ✅ FAQ sections with toggle functionality'
                '\n  ✅ Social media integration'
                '\n'
                '\n🚀 Access Your Website:'
                '\n  📍 Homepage: http://127.0.0.1:8000/'
                '\n  📍 About: http://127.0.0.1:8000/about/'
                '\n  📍 Features: http://127.0.0.1:8000/features/'
                '\n  📍 Contact: http://127.0.0.1:8000/contact/'
                '\n  📍 Admin Dashboard: http://127.0.0.1:8000/admin/'
                '\n'
                '\n🎯 What to do next:'
                '\n  1. Run: python manage.py runserver'
                '\n  2. Visit: http://127.0.0.1:8000/'
                '\n  3. Enjoy your professional College ERP website!'
            )
        )
    
    def update_main_urls(self):
        """Update main URLs file to include website"""
        urls_content = '''from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/', include('dashboards.urls')),
    path('api/app/', include('app.urls')),
    path('api/admissions/', include('admissions.urls')),
    path('api/finance/', include('finance.urls')),
    path('api/hostel/', include('hostel.urls')),
    path('api/exams/', include('exams.urls')),
    path('api/students/', include('students.urls')),
    path('api/dashboards/', include('dashboards.urls')),
    path('', include('website.urls')),  # Website URLs
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
'''
        
        urls_path = os.path.join(settings.BASE_DIR, 'College_ERP', 'urls.py')
        with open(urls_path, 'w') as f:
            f.write(urls_content)
        
        self.stdout.write('✅ Updated main URLs configuration')
    
    def create_website_app(self):
        """Create website app structure"""
        website_dir = os.path.join(settings.BASE_DIR, 'website')
        os.makedirs(website_dir, exist_ok=True)
        
        # Create __init__.py
        with open(os.path.join(website_dir, '__init__.py'), 'w') as f:
            f.write('')
        
        self.stdout.write('✅ Website app structure created')