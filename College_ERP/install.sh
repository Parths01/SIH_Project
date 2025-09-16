#!/bin/bash

# College ERP System Installation Script

echo "🏫 College ERP System Installation Started..."

# Check if virtual environment is active
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ Virtual environment is active: $VIRTUAL_ENV"
else
    echo "❌ Please activate your virtual environment first:"
    echo "   python -m venv venv"
    echo "   source venv/bin/activate  # On Linux/Mac"
    echo "   venv\\Scripts\\activate     # On Windows"
    exit 1
fi

# Install core dependencies first
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Create directories if they don't exist
echo "📁 Creating necessary directories..."
mkdir -p logs
mkdir -p static
mkdir -p media/students/photos
mkdir -p media/students/documents
mkdir -p media/admissions/documents
mkdir -p media/receipts
mkdir -p media/hall_tickets
mkdir -p media/transcripts
mkdir -p media/attachments

# Create environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "⚙️  Creating environment configuration..."
    echo "   For basic development setup, keeping minimal .env"
    echo "   For advanced features, copy from .env.example:"
    echo "   cp .env.example .env"
else
    echo "✅ Environment file (.env) already exists"
fi

echo "🗄️  Setting up database (make sure PostgreSQL is running)..."

# Run initial migrations
echo "🔄 Creating migrations..."
python manage.py makemigrations common
python manage.py makemigrations app
python manage.py makemigrations admissions  
python manage.py makemigrations finance
python manage.py makemigrations hostel
python manage.py makemigrations exams
python manage.py makemigrations dashboards
python manage.py makemigrations students

echo "🔄 Applying migrations..."
python manage.py migrate

echo "👤 Creating superuser and initial data..."
python manage.py init_system

echo "📊 Collecting static files..."
python manage.py collectstatic --noinput

echo "✅ Installation completed successfully!"
echo ""
echo "🚀 To start the development server:"
echo "   python manage.py runserver"
echo ""
echo "🌐 Access the admin panel at:"
echo "   http://localhost:8000/admin/"
echo ""
echo "🔑 Default login credentials:"
echo "   Username: admin"
echo "   Password: admin123"
echo ""
echo "⚠️  IMPORTANT: Change the default password after first login!"
echo ""
echo "📚 Next steps:"
echo "   1. Configure your institution settings in admin panel"
echo "   2. Add departments and programs"
echo "   3. Set up fee structures"
echo "   4. Configure hostel and room details"
echo "   5. Create user accounts for staff"
echo ""