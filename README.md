# Healthcare Backend

A **Django + DRF** backend for managing patients, doctors, and patient-doctor assignments with authentication, filtering, search, and bulk operations. This project is designed to serve as a robust backend for healthcare management systems.

## Features

- User authentication using **JWT** (`djangorestframework-simplejwt`)
- CRUD operations for **Patients**, **Doctors**, and **Patient-Doctor mappings**
- Bulk operations for creating/updating patients and assigning doctors
- Filtering, searching, and ordering on key fields
- Validation to prevent duplicate doctor-patient assignments
- API landing page and documentation links

## Tech Stack

- **Backend**: Python 3.13, Django 5, Django REST Framework, django-filter  
- **Database**: PostgreSQL 
- **Auth**: JWT authentication (access + refresh tokens)  
- **Dev Tools**: Docker & docker-compose for containerized setup  

## Requirements

- Python 3.13+  
- pip packages (install via `requirements.txt`)

```bash
pip install -r requirements.txt
```

## Setup Instructions

### Clone the repository
```bash
git clone https://github.com/DivyaBGowda484/healthcare-backend-WhatBytes.git
cd healthcare-backend-WhatBytes
```

### Create virtual environment and activate
```bash
python3 -m venv venv
source venv/bin/activate
```

### Install backend dependencies
```bash
pip install -r requirements.txt
```

### Run migrations
```bash
python manage.py migrate
```

### Create a superuser (for admin access)
```bash
python manage.py createsuperuser
```

### Start the development server
```bash
python manage.py runserver
```

## Access Endpoints

- **Landing page**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)  
- **API routes**: `/api/patients/`, `/api/doctors/`, `/api/mappings/`  

## Testing
Run the automated tests:
```bash
python manage.py test
```

## API Endpoints Overview

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/patients/` | GET, POST, PUT, DELETE | CRUD operations for patients |
| `/api/doctors/` | GET, POST, PUT, DELETE | CRUD operations for doctors |
| `/api/mappings/` | GET, POST | Assign patients to doctors |
| `/api/mappings/<patient_id>/` | GET | List doctors assigned to a specific patient |
| `/api/patients/bulk-create/` | POST | Bulk create patients |
| `/api/patients/bulk-update/` | POST | Bulk update patients |
| `/api/mappings/bulk-assign/` | POST | Bulk assign a doctor to multiple patients |

---

### 1. Register a new user
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
-H "Content-Type: application/json" \
-d '{"name":"John Smith","email":"john@example.com","password":"SecurePass123"}'
```

### 2. Login to get JWT tokens
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
-H "Content-Type: application/json" \
-d '{"email":"john@example.com","password":"SecurePass123"}'
```

### Copy the access token from the login response and set it here:
ACCESS=REPLACE_WITH_ACCESS_TOKEN


### 3. Create a superuser (optional, admin access)
```bash
python manage.py createsuperuser
```

### 4. Apply migrations
```bash
python manage.py migrate
```

### 5. Start the development server
```bash
python manage.py runserver
```

### 6. Create a patient
```bash
curl -X POST http://localhost:8000/api/patients/ \
-H "Authorization: Bearer $ACCESS" \
-H "Content-Type: application/json" \
-d '{"name":"Alice Johnson","age":29,"gender":"F","address":"123 Main Street"}'
```

### 7. List patients
```bash
curl -X GET http://localhost:8000/api/patients/ \
-H "Authorization: Bearer $ACCESS"
```

### 8. Create a doctor
```bash
curl -X POST http://localhost:8000/api/doctors/ \
-H "Authorization: Bearer $ACCESS" \
-H "Content-Type: application/json" \
-d '{"name":"Dr. Sarah Lee","specialization":"Cardiology","email":"sarah.lee@hospital.org","phone":"+1-555-9876"}'
```

### 9. List doctors
```bash
curl -X GET http://localhost:8000/api/doctors/ \
-H "Authorization: Bearer $ACCESS"
```

### 10. Map a doctor to a patient
```bash
curl -X POST http://localhost:8000/api/mappings/ \
-H "Authorization: Bearer $ACCESS" \
-H "Content-Type: application/json" \
-d '{"patient":1,"doctor":1}'
```

### 11. List doctor-patient mappings
```bash
curl -X GET http://localhost:8000/api/mappings/ \
-H "Authorization: Bearer $ACCESS"
```
