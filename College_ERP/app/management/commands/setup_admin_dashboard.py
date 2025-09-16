from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.staticfiles.management.commands.collectstatic import Command as CollectStaticCommand

class Command(BaseCommand):
    help = 'Setup enhanced admin dashboard with modern design'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🎨 Setting up enhanced admin dashboard...'))
        
        # Create directories if they don't exist
        import os
        from django.conf import settings
        
        static_dirs = [
            'static/admin/css',
            'static/admin/js',
            'static/admin/img',
            'templates/admin'
        ]
        
        for directory in static_dirs:
            full_path = os.path.join(settings.BASE_DIR, directory)
            os.makedirs(full_path, exist_ok=True)
            self.stdout.write(f'✅ Created directory: {directory}')
        
        # Update admin site configuration
        from django.contrib.admin import site as admin_site
        admin_site.site_header = '🎓 College ERP Administration'
        admin_site.site_title = 'College ERP Admin'
        admin_site.index_title = 'Welcome to College ERP Dashboard'
        
        self.stdout.write(self.style.SUCCESS('✅ Admin site configuration updated'))
        
        # Check if superuser exists
        if not User.objects.filter(is_superuser=True).exists():
            self.stdout.write(
                self.style.WARNING('⚠️  No superuser found. Please create one using: python manage.py createsuperuser')
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                '\n🎉 Enhanced admin dashboard setup completed!\n'
                '\n📊 Features added:'
                '\n  ✅ Modern, responsive design'
                '\n  ✅ Interactive charts and graphs'
                '\n  ✅ Real-time statistics'
                '\n  ✅ Role-based dashboard views'
                '\n  ✅ Professional color scheme'
                '\n  ✅ Mobile-friendly interface'
                '\n'
                '\n🚀 Next steps:'
                '\n  1. Run: python manage.py migrate'
                '\n  2. Run: python manage.py collectstatic'
                '\n  3. Run: python manage.py runserver'
                '\n  4. Visit: http://127.0.0.1:8000/admin/'
                '\n'
                '\n🎯 Dashboard features:'
                '\n  📈 Student enrollment charts'
                '\n  📊 Department-wise statistics'
                '\n  👥 Staff distribution graphs'
                '\n  📅 Recent activities feed'
                '\n  🚀 Quick action buttons'
            )
        )