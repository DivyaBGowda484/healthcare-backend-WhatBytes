# Healthcare Backend (Django + DRF + JWT + PostgreSQL)

A reference implementation for the assignment: user registration/login with JWT, and CRUD APIs for Patients, Doctors, and Patient–Doctor mappings.

## Quickstart (Local, macOS/Linux)

```bash
# 1) Create and activate a virtualenv
python3 -m venv .venv
source .venv/bin/activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) Copy env template and fill values
cp .env.example .env
# For local Postgres, set DATABASE_URL like:
# DATABASE_URL=postgres://postgres:postgres@localhost:5432/healthcare_db

# 4) Run migrations & create a superuser (optional)
python manage.py migrate
python manage.py createsuperuser

# 5) Start dev server
python manage.py runserver 0.0.0.0:8000
```

## Quickstart (Docker)

```bash
cp .env.docker.example .env   # uses service host "db"
docker compose up --build
# App: http://localhost:8000/
```

## API Base URL

`/api/`

### Auth
- `POST /api/auth/register/` — body: `{ "name": "...", "email": "...", "password": "..." }`
- `POST /api/auth/login/` — body: `{ "email": "...", "password": "..." }` → `{ "access": "...", "refresh": "..." }`
- `POST /api/auth/token/refresh/` — body: `{ "refresh": "..." }`

### Patients (auth required)
- `POST /api/patients/`
- `GET /api/patients/` — **only patients created by the authenticated user**
- `GET /api/patients/<id>/`
- `PUT /api/patients/<id>/`
- `DELETE /api/patients/<id>/`

### Doctors (auth required)
- `POST /api/doctors/`
- `GET /api/doctors/`
- `GET /api/doctors/<id>/`
- `PUT /api/doctors/<id>/`
- `DELETE /api/doctors/<id>/`

### Mappings (auth required)
- `POST /api/mappings/` — assign a doctor to a patient
- `GET /api/mappings/` — list all mappings
- `GET /api/mappings/<patient_id>/` — list doctors assigned to the given patient
- `DELETE /api/mappings/<id>/` — remove a specific mapping

## Example cURL

```bash
# Register
curl -X POST http://localhost:8000/api/auth/register/   -H "Content-Type: application/json"   -d '{"name":"Divya","email":"divya@example.com","password":"P@ssw0rd123"}'

# Login
curl -X POST http://localhost:8000/api/auth/login/   -H "Content-Type: application/json"   -d '{"email":"divya@example.com","password":"P@ssw0rd123"}'

# Use the access token from login below
ACCESS=REPLACE_WITH_ACCESS_TOKEN

# Create patient
curl -X POST http://localhost:8000/api/patients/   -H "Authorization: Bearer $ACCESS" -H "Content-Type: application/json"   -d '{"name":"John Doe","age":35,"gender":"M","address":"221B Baker Street"}'

# List my patients
curl -X GET http://localhost:8000/api/patients/   -H "Authorization: Bearer $ACCESS"

# Create doctor
curl -X POST http://localhost:8000/api/doctors/   -H "Authorization: Bearer $ACCESS" -H "Content-Type: application/json"   -d '{"name":"Dr. House","specialization":"Diagnostics","email":"house@hospital.org","phone":"+1-555-1234"}'

# Map doctor to patient
curl -X POST http://localhost:8000/api/mappings/   -H "Authorization: Bearer $ACCESS" -H "Content-Type: application/json"   -d '{"patient":1,"doctor":1}'
```

## Tech
- Django, Django REST Framework
- JWT via `djangorestframework-simplejwt`
- PostgreSQL
- `django-environ` for `.env` management
