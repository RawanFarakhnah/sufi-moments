# Sufi Moments 🌿

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Django](https://img.shields.io/badge/Django-4.0%2B-green)
![MySQL](https://img.shields.io/badge/MySQL-8.0%2B-orange)
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)

A Django-based platform for sharing Sufi Cafe memories, supporting photo/video uploads, events

---

## ✨ Features
- **📸 Memory Sharing:** Submit memories with admin moderation.
- **🗓️ Event Management:** Create and RSVP to events.
- **👍 Social Features:** Like and comment on memories.
- **🔒 Authentication:** Google OAuth and traditional login.
- **📱 Responsive Design:** Mobile-first approach.
- **🔄 AJAX Integration:** Dynamic content loading.
- **🗂️ Database:** MySQL with Django ORM.
- **🌐 REST API:** JSON endpoints for integration.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MySQL 8.0+
- Git

### Installation
```bash
# Clone repository
git clone https://github.com/yourusername/sufi-moments.git
cd sufi-moments

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt
```

### Database Setup
1. Create MySQL database:
```sql
CREATE DATABASE sufi_moments_database;
```
2. Update `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sufi_moments_database',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}
```

### Run Application
```bash
# Apply migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Run development server
python manage.py runserver
```
Visit [http://localhost:8000](http://localhost:8000) in your browser.

---

## 📂 Project Structure
```
sufi_cafe/
├── accounts/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
├── events/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
├── landing/
│   ├── models.py
│   ├── views.py
├── locale/
│   ├── ar/
│   │   ├── LC_MESSAGES/
│   │   │   ├── django.po
│   ├── en/
│   │   ├── LC_MESSAGES/
│   │   │   ├── django.po
├── memories/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
├── sufi_moments/
│   ├── settings/
│   ├── urls.py
│   └── wsgi.py
├── static/
│   ├── css/
│   ├── js/
│   └── img/
├── templates/
│   ├── landing/
│   │   ├── about.html
│   │   ├── home.html
│   ├── accounts/
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── profile.html
│   ├── events/
│   │   ├── list.html
│   │   ├── detail.html
│   │   ├── create.html
│   ├── memories/
│   │   ├── list.html
│   │   ├── create.html
│   ├── base.html
└── manage.py
├── requirements.txt
├── README.md
```

---

## 🌐 API Endpoints
| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/api/memories/` | GET | List public memories | No |
| `/api/memories/` | POST | Create new memory | Yes |
| `/api/events/` | GET | List upcoming events | No |
| `/api/events/<id>/rsvp/` | POST | RSVP to event | Yes |

---

## 🔒 Security Features
- ✅ CSRF protection
- ✅ SQL injection prevention
- ✅ XSS protection
- ✅ Password hashing (PBKDF2)
- ✅ Content moderation system
- ✅ Rate limiting (API endpoints)

---

## 🛠️ Tech Stack
- **Backend:** Django 4.0+
- **Database:** MySQL 8.0
- **Frontend:** HTML5, CSS3, JavaScript
- **Authentication:** Django Allauth

---

## 🤝 Contributing
1. Fork the repository.
2. Create your feature branch: `git checkout -b feature/AmazingFeature`.
3. Commit your changes: `git commit -m 'Add some AmazingFeature'`.
4. Push to the branch: `git push origin feature/AmazingFeature`.
5. Open a Pull Request.

---
