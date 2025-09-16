# College ERP - Quick Setup Guide

## 🚨 Database Fixed - Now Using SQLite

The system is now configured to use SQLite database for development (no PostgreSQL setup required).

## Setup Steps

### 1. Clean Installation (Recommended)

**Step A: Remove conflicting packages**
```bash
pip uninstall -y django-cachalot django-rq rq django-tenant-schemas
```

**Step B: Install stable packages**
```bash
pip install -r requirements-stable.txt
```

**Step C: Install additional packages individually (optional)**
```bash
# Only install these if you need the features
pip install redis==5.0.1
pip install reportlab==4.0.9
pip install qrcode==7.4.2
pip install requests==2.31.0
```

### 2. Database Setup (SQLite - No Setup Required!)

The system now uses SQLite database which requires no installation or configuration. The database file will be created automatically.

### 3. Run Migrations
```bash
# Create migrations for all apps
python manage.py makemigrations common
python manage.py makemigrations app
python manage.py makemigrations admissions
python manage.py makemigrations finance
python manage.py makemigrations hostel
python manage.py makemigrations exams
python manage.py makemigrations dashboards
python manage.py makemigrations students

# Apply migrations
python manage.py migrate
```

### 4. Create Superuser
```bash
python manage.py createsuperuser
# Username: admin
# Email: admin@college.edu
# Password: admin123
```

### 5. Start Server
```bash
python manage.py runserver
```

**Access:** http://localhost:8000/admin/  
**Login:** admin / admin123

## Configuration Options

### Option A: SQLite (Current - Recommended for Development)
- ✅ No database server required
- ✅ Works out of the box
- ✅ Perfect for development and testing
- ✅ Database file: `db.sqlite3`

### Option B: PostgreSQL (For Production)
If you need PostgreSQL later, uncomment the PostgreSQL section in `settings.py` and:

```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE DATABASE college_erp;
CREATE USER college_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE college_erp TO college_user;
\q

# Update .env file
USE_SQLITE=False
DB_PASSWORD=your_password
```

## Current Configuration
Your `.env` file includes:
- SQLite database (no setup required)
- Development settings (DEBUG=True, console email backend)
- Institution: Sample College of Engineering
- All core modules enabled

## Troubleshooting

**If you still get database errors:**
```bash
# Delete any existing database files
rm -f db.sqlite3

# Clear migrations and start fresh
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
python manage.py makemigrations
python manage.py migrate
```

**Package Installation Issues:**
```bash
# Upgrade pip first
pip install --upgrade pip

# Install packages one by one if bulk install fails
pip install Django==4.2.16
pip install djangorestframework==3.14.0
# ... etc
```

The system should now work immediately with SQLite!