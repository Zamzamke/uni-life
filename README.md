# Maisha Uni Backend

A Student Success Platform backend built with Django REST Framework that enables university students and institutions to engage, communicate, and manage opportunities.

##  Features

- **JWT Authentication** - Secure user authentication
- **User Management** - Student and Admin roles
- **Announcements** - Post and manage institutional announcements
- **Opportunities** - Job, internship, and scholarship listings
- **RESTful API** - Clean, well-documented API endpoints
- **API Documentation** - Interactive Swagger/OpenAPI documentation

##  Tech Stack

- **Backend**: Django 4.2 + Django REST Framework
- **Database**: PostgreSQL (Production), SQLite (Development)
- **Authentication**: JWT (djangorestframework-simplejwt)
- **API Docs**: drf-spectacular
- **Deployment**: Render

##  API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/refresh/` - Token refresh

### Profile
- `GET /api/auth/profile/` - Get user profile
- `PUT /api/auth/profile/` - Update profile

### Announcements
- `GET /api/announcements/` - List all announcements
- `POST /api/announcements/` - Create announcement (Admin only)
- `GET /api/announcements/{id}/` - Get specific announcement

### Opportunities
- `GET /api/opportunities/` - List all opportunities
- `POST /api/opportunities/` - Create opportunity (Admin only)
- `GET /api/opportunities/{id}/` - Get specific opportunity

##  Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL (for production)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Zamzamke/uni-life.git
   cd uni-life