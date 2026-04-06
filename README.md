# College Alumni Connect & Management System

A comprehensive, production-grade Django web application designed to foster meaningful connections between college alumni and current students.

## Quick Start

### 1. Requirements
- Python 3.8+
- Django 4.0+

### 2. Setup
```bash
# Install dependencies
pip install django django-crispy-forms crispy-bootstrap5 openpyxl reportlab

# Apply migrations
python manage.py migrate

# Create Superuser (Admin)
python manage.py createsuperuser

# Start server
python manage.py runserver
```

### 3. Usage
1. **Access Admin**: Go to `http://127.0.0.1:8000/admin/` and log in with your superuser.
2. **Setup Data**: Create Announcements and verify user registrations.
3. **Approve Users**: New registrations appear in the `Approvals` table. Approve them to allow login.

### 3. Management Commands
- **Seed Data**: `python manage.py seed_data`
- **Auto-Conversion**: `python manage.py convert_graduates` (Converts students past their grad year to Alumni)

## Project Structure
- `users/`: Authentication, Roles, and Approvals.
- `profiles/`: Student/Alumni data and AI Matching Service.
- `mentorship/`: Connections, Chat, and Resume Review.
- `events/`: Webinar and Workshop management.
- `core/`: Announcements, Audit Logs, and Dashboards.
- `analytics/`: Export services and chart data.

## UI Aesthetic
Inspired by **SRIT (Srit.ac.in)**, featuring:
- Navy Blue & Ivory White theme.
- Traditional academic header/footer.
- Professional, non-SaaS clean typography.
