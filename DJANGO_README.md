# Django Project

A Django web application built with Django 6.0.2.

## 🚀 Quick Start

### Installation

Django is already installed. If you need to reinstall:

```bash
pip3 install django
```

### Running the Development Server

Start the Django development server:

```bash
python3 manage.py runserver
```

Then visit:
- **Home Page**: http://127.0.0.1:8000/
- **About Page**: http://127.0.0.1:8000/about/
- **API Endpoint**: http://127.0.0.1:8000/api/hello/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## 📁 Project Structure

```
cursorpython/
├── manage.py              # Django management script
├── myproject/             # Project configuration
│   ├── __init__.py
│   ├── settings.py        # Project settings
│   ├── urls.py           # URL routing
│   ├── asgi.py           # ASGI configuration
│   └── wsgi.py           # WSGI configuration
├── myapp/                 # Your application
│   ├── __init__.py
│   ├── admin.py          # Admin configuration
│   ├── apps.py           # App configuration
│   ├── models.py         # Database models
│   ├── tests.py          # Tests
│   └── views.py          # View functions
└── db.sqlite3            # SQLite database
```

## 📚 What's Included

### Views
- **Home Page** (`/`): Welcome page with project information
- **About Page** (`/about/`): About page
- **API Endpoint** (`/api/hello/`): JSON API example

### Features
- ✅ Django 6.0.2
- ✅ SQLite Database
- ✅ Admin Panel
- ✅ Beautiful Home Page
- ✅ API Endpoints
- ✅ Configured URL Routing

## 🛠️ Common Commands

### Database Management

```bash
# Create migrations
python3 manage.py makemigrations

# Apply migrations
python3 manage.py migrate

# Create superuser (for admin panel)
python3 manage.py createsuperuser
```

### Development

```bash
# Run development server
python3 manage.py runserver

# Run on different port
python3 manage.py runserver 8080

# Run tests
python3 manage.py test
```

### App Management

```bash
# Create a new app
python3 manage.py startapp newapp
```

## 🎯 Next Steps

1. **Create a Superuser**: Run `python3 manage.py createsuperuser` to access the admin panel
2. **Add Models**: Define your data models in `myapp/models.py`
3. **Create Templates**: Add HTML templates for better views
4. **Add Static Files**: Add CSS, JavaScript, and images
5. **Build Your App**: Start adding your own features!

## 📖 Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Tutorial](https://docs.djangoproject.com/en/6.0/intro/tutorial01/)
- [Django REST Framework](https://www.django-rest-framework.org/) (for APIs)

## 🔧 Configuration

The project uses default Django settings with SQLite database. To modify settings, edit `myproject/settings.py`.

## 📝 License

This is a starter project. Add your own license as needed.

---

**Happy Coding!** 🎉

