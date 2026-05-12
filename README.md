# FinDish / FlavorMap

FinDish is a Django-based restaurant discovery and review platform for the CSE 220 Web Programming project. Users can browse restaurants, search and filter listings, read and write reviews, add favorites, and manage their own submitted restaurants after admin verification.

## Project Links

- GitHub repository: https://github.com/basarhaktanyaman/Findish
- Local development URL: http://127.0.0.1:8000/
- Admin panel: http://127.0.0.1:8000/admin/

## Tech Stack

- Python 3.12+
- Django 6.x
- SQLite
- Bootstrap 5
- Pillow for image uploads

## Setup Instructions

1. Clone the repository:

```bash
git clone https://github.com/basarhaktanyaman/Findish.git
cd Findish
```

2. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Apply database migrations:

```bash
python manage.py migrate
```

5. Create an admin user:

```bash
python manage.py createsuperuser
```

6. Run the development server:

```bash
python manage.py runserver
```

7. Open the app:

```text
http://127.0.0.1:8000/
```

## Main Features

- Restaurant list and detail pages
- Category, city, price, search, and sorting filters
- User registration, login, logout, and profile page
- Restaurant submission with admin verification
- Restaurant create, edit, and delete for owners/admins
- Review and rating system with one review per user per restaurant
- Review replies
- Favorites list
- Menu item management
- Opening hours management
- Restaurant image upload
- Admin panel customizations for restaurant verification and quick delete

## Report Template

The final report template is available at:

```text
docs/REPORT.md
```

Screenshot placeholders are listed in:

```text
docs/screenshots/README.md
```

Add screenshots to `docs/screenshots/` and reference them from `docs/REPORT.md`.
