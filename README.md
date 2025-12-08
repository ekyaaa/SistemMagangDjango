# MagangHub - Internship Management System

A clean and modern internship management system built with Django in just 2 days. This system allows companies to manage their internship programs efficiently with a beautiful admin dashboard and a user-friendly application interface.

## 🚀 Features

### For Public Users
- **Easy Application Process**: Apply for internship positions by filling out a simple form
- **One-Time Application**: Each NIK (National ID) can only apply once per department to prevent duplicate applications
- **File Upload**: Upload CV documents during application
- **Search Functionality**: Search available positions by title or department

### For Administrators
- **Secure Authentication**: Built-in Django authentication system for admin access
- **Beautiful Dashboard**: Clean and intuitive admin dashboard with statistics and charts
- **Complete CRUD Operations**:
  - Manage Departments
  - Manage Internship Positions (Lowongan)
  - Review and manage applicants
- **Application Management**: 
  - Approve or reject applicant submissions
  - View detailed applicant information
  - Track application status (Pending, Approved, Rejected)
- **Real-time Statistics**: Dashboard showing key metrics and recent applicants

## 🛠️ Tech Stack

- **Backend**: Django 6.0
- **Database**: PostgreSQL
- **Frontend**: HTML, CSS, JavaScript (Clean and modern UI)
- **Authentication**: Django's built-in authentication system

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL
- pip (Python package manager)

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ekyaaa/SistemMagangDjango.git
   cd SistemMagangDjango
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Database**
   
   Update your database settings in `config/settings/local.py` or `config/settings/production.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'your_database_name',
           'USER': 'your_database_user',
           'PASSWORD': 'your_database_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser (Admin)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Public Interface: `http://localhost:8000/`
   - Admin Login: `http://localhost:8000/admin/`
   - Admin Dashboard: `http://localhost:8000/dashboard/`

## 📁 Project Structure

```
SistemMagangDjango/
├── admin_dashboard/          # Admin dashboard app
│   ├── templates/           # Admin templates
│   ├── views.py            # Admin views
│   ├── service.py          # Business logic
│   └── auth_views.py       # Authentication views
├── magang/                  # Main internship app
│   ├── models.py           # Database models
│   ├── views.py            # Public views
│   ├── services/           # Service layer
│   └── templates/          # Public templates
├── config/                  # Project configuration
│   ├── settings/           # Settings modules
│   │   ├── base.py        # Base settings
│   │   ├── local.py       # Development settings
│   │   └── production.py  # Production settings
│   └── urls.py            # URL routing
├── storage/                # Media files storage
│   └── cv/                # Uploaded CV files
├── manage.py
└── requirements.txt
```

## 🗃️ Database Models

### Departement
Manages company departments where internships are available.

### Lowongan (Internship Position)
- Position title
- Description
- Start and end dates
- Associated department

### Pendaftar (Applicant)
- Personal information (NIK, name, gender, date of birth)
- Contact details (address, phone)
- Academic information (university, major, GPA)
- CV upload
- Unique constraint on NIK to prevent duplicate applications

### TransaksiPendaftaran (Application Transaction)
Tracks the relationship between applicants and positions with status management.

## 🎨 Features in Detail

### Public Interface
- Clean and modern landing page
- List of available internship positions
- Search and filter functionality
- Easy-to-use application form
- Automatic validation for duplicate NIK

### Admin Dashboard
- Overview statistics (total positions, applicants, pending applications)
- Recent applicants table
- Department management (Create, Read, Update, Delete)
- Position management (Create, Read, Update, Delete)
- Applicant review system
- Application status management (Approve/Reject)

## 🔒 Security Features

- Django's built-in authentication system
- CSRF protection
- Staff-only access to admin dashboard
- Secure file upload handling
- SQL injection protection through Django ORM

## 🚀 Future Enhancements

- Email notifications for applicants
- Advanced filtering and sorting options
- Export data to Excel/PDF
- Multi-language support
- Applicant tracking system
- Interview scheduling

## 👨‍💻 Development

This project was developed in **2 days** as a rapid prototype for an internship management system. It demonstrates:
- Clean code architecture
- Service layer pattern
- Separation of concerns
- Modern UI/UX principles
- Django best practices

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/ekyaaa/SistemMagangDjango/issues).

## 📧 Contact

For any questions or suggestions, please open an issue or contact the repository owner.

---

**Note**: Remember to change the `SECRET_KEY` in production and never commit sensitive information to the repository.
