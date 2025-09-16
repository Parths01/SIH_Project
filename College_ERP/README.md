# College ERP System

A comprehensive Enterprise Resource Planning (ERP) system for educational institutions4. **Environment is pre-configured**
```bash
# The .env file is already set up for development
# Database: college_erp (PostgreSQL)
# User: postgres / Password: postgres
# Institution: Sample College of Engineering
```

5. **Initialize database**
```bash
python manage.py migrate
python manage.py init_system  # Creates superuser and initial data
``` Django and PostgreSQL. This system unifies admissions, fee collection, hostel allocation, examination records, and administrative dashboards into a single, cohesive platform.

## 🎯 Problem Statement

Educational institutions face fragmentation across critical operations:
- **Admissions, fee collection, hostel allocation, and examination records maintained in separate ledgers**
- **Students queue at multiple counters; staff re-enter identical data**
- **Administrators lack real-time institutional overview**

Traditional ERP solutions are expensive and complex. This system provides similar functionality using modern web technologies at a fraction of the cost.

## ✨ Key Features

### 🎓 **Admissions Management**
- Online application forms with document upload
- Application review workflow with status tracking
- Interview scheduling and evaluation
- Automated acceptance/rejection notifications
- Seamless conversion to student records

### 💰 **Finance & Fee Management**
- Flexible fee structure configuration by program/category
- Automated invoice generation
- Multiple payment methods (Online, Cash, Cheque, UPI, etc.)
- Instant digital receipt generation with QR codes
- Payment reconciliation and ledger management
- Outstanding fees tracking and reminders

### 🏠 **Hostel Management**
- Room allocation with capacity management
- Real-time occupancy tracking
- Mess plan subscriptions
- Attendance monitoring
- Damage assessment and security deposits

### 📚 **Examination System**
- Course enrollment and management
- Assessment configuration (internals, externals, practicals)
- Grade calculation with SGPA/CGPA computation
- Result publishing and transcript generation
- Hall ticket generation with barcodes

### 📊 **Dashboards & Analytics**
- Role-based dashboards for different user types
- Real-time KPI monitoring
- Financial collection tracking
- Occupancy and capacity analytics
- Alert system for critical metrics
- Export capabilities (CSV, Excel, PDF)

### 🔐 **Security & Audit**
- Role-based access control
- Comprehensive audit logging
- Data encryption for sensitive information
- Secure file storage with access controls
- Rate limiting and security middleware

## 🏗️ System Architecture

### **Technology Stack**
- **Backend**: Django 5.1, Django REST Framework
- **Database**: PostgreSQL 15+ with Redis for caching
- **Task Queue**: Celery with Redis broker
- **File Storage**: Local filesystem or S3-compatible storage
- **PDF Generation**: WeasyPrint for reports and receipts
- **Frontend**: Django Admin (expandable to React/Vue.js)

### **Application Structure**
```
College_ERP/
├── common/          # Shared utilities, base models, audit logging
├── app/             # Core models (Student, Department, Program)
├── admissions/      # Application management and workflow
├── finance/         # Fee management, payments, receipts
├── hostel/          # Room allocation and mess management
├── exams/           # Course enrollment and result management
└── dashboards/      # Analytics, widgets, and reporting
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 15+
- Redis 6+
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/college-erp.git
cd college-erp
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your database and other configuration
```

5. **Initialize database**
```bash
python manage.py migrate
python manage.py init  # Creates superuser and initial data
```

6. **Start development server**
```bash
python manage.py runserver
```

7. **Access the system**
- Admin Panel: http://localhost:8000/admin/
- Default login: `admin` / `admin123`

## 🐳 Docker Deployment

### Development with Docker Compose
```bash
# Start all services
docker-compose up -d

# Initialize the system
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py init

# View logs
docker-compose logs -f web
```

### Production Deployment
```bash
# Use production compose file
docker-compose -f docker-compose.prod.yml up -d

# Set up SSL certificates
docker-compose exec nginx certbot --nginx
```

## 📋 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Enable debug mode | `False` |
| `SECRET_KEY` | Django secret key | Required |
| `DATABASE_URL` | PostgreSQL connection string | Required |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379/0` |
| `INSTITUTION_NAME` | Your institution name | `Sample College` |
| `INSTITUTION_CODE` | Short code for numbering | `SC` |
| `EMAIL_HOST` | SMTP server for emails | Required for notifications |
| `USE_S3` | Enable S3 file storage | `False` |

### Initial Setup

After installation, configure:

1. **Institution Settings**: Update institution name, code, and contact details
2. **Academic Structure**: Add departments, programs, and courses
3. **Fee Structure**: Configure fee heads and plans for different programs
4. **Hostel Setup**: Add hostels, rooms, and mess plans
5. **User Roles**: Create staff accounts with appropriate permissions

## 📊 API Documentation

The system provides RESTful APIs for integration:

- **Students API**: `/api/students/` - Student CRUD operations
- **Admissions API**: `/api/admissions/` - Application management
- **Finance API**: `/api/finance/` - Fee and payment operations
- **Hostel API**: `/api/hostel/` - Room allocation and management
- **Exams API**: `/api/exams/` - Academic and result management
- **Dashboards API**: `/api/dashboards/` - Analytics and reporting

API documentation available at: `/api/docs/`

## 🔧 Key Workflows

### 1. Admission to Enrollment
```
Application Submission → Document Verification → Interview (if required) 
→ Selection → Fee Payment → Student Record Creation → Course Enrollment
```

### 2. Fee Collection
```
Fee Plan Creation → Invoice Generation → Payment Processing 
→ Receipt Generation → Ledger Posting → Reconciliation
```

### 3. Hostel Allocation
```
Application → Eligibility Check → Room Assignment 
→ Fee Collection → Check-in → Attendance Tracking
```

### 4. Examination Process
```
Course Registration → Assessment Configuration → Exam Scheduling 
→ Hall Ticket Generation → Result Entry → Grade Calculation → Publication
```

## 🎯 Business Benefits

### **For Students**
- ✅ Single portal for all academic needs
- ✅ Real-time status tracking
- ✅ Digital receipts and certificates
- ✅ Mobile-friendly interface

### **For Staff**
- ✅ Eliminate data re-entry across systems
- ✅ Automated workflow processing
- ✅ Role-based access to relevant data
- ✅ Comprehensive reporting tools

### **For Administrators**
- ✅ Real-time institutional overview
- ✅ Financial tracking and analytics
- ✅ Capacity planning insights
- ✅ Compliance and audit trails

### **For Institution**
- ✅ Significant cost savings over commercial ERP
- ✅ Customizable to specific requirements
- ✅ Scalable architecture
- ✅ Open-source flexibility

## 🛡️ Security Features

- **Authentication**: Multi-factor authentication support
- **Authorization**: Granular permission system
- **Data Protection**: Encryption at rest and in transit
- **Audit Trail**: Comprehensive logging of all actions
- **Rate Limiting**: Protection against abuse
- **Input Validation**: Prevents injection attacks
- **File Security**: Secure upload and access controls

## 📈 Scalability & Performance

- **Database Optimization**: Indexed queries and connection pooling
- **Caching Strategy**: Redis for frequently accessed data
- **Background Tasks**: Asynchronous processing with Celery
- **File Storage**: S3-compatible storage for assets
- **Load Balancing**: Ready for horizontal scaling
- **Monitoring**: Built-in health checks and metrics

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python manage.py test

# Code formatting
black .
isort .

# Linting
flake8 .
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

- **Documentation**: See SETUP.md for quick start
- **Issues**: [GitHub Issues](https://github.com/yourusername/college-erp/issues)
- **Email**: support@yourorganization.com

## 🏆 Acknowledgments

Built for educational institutions seeking modern, affordable ERP solutions. This project demonstrates how thoughtful architecture and open-source technologies can deliver enterprise-grade functionality without enterprise-grade costs.

---

**Note**: This system is designed for educational institutions and can be customized for specific requirements. For commercial deployment, please ensure compliance with local data protection regulations.