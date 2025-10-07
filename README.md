## RentMate - Rental Management System

Backend: Django REST Framework (Python)
Frontend: Static HTML/CSS/JavaScript

### Prerequisites
- Python 3.8+

### Setup
1. Install dependencies:
```
pip install -r requirements.txt
```

2. Navigate to backend directory:
```
cd backend
```

3. Run migrations:
```
python manage.py migrate
```

4. Create superuser (optional):
```
python manage.py createsuperuser
```

5. Start Django development server:
```
python manage.py runserver
```

The API runs at `http://127.0.0.1:8000`

6. Open `index.html` with a local server (e.g. VS Code Live Server) or any static server.

### API Endpoints

#### Authentication
- POST `/api/auth/register/` - User registration
- POST `/api/auth/login/` - User login
- POST `/api/auth/logout/` - User logout
- GET `/api/auth/profile/` - Get user profile

#### Properties
- GET `/api/properties/units/` - List units
- POST `/api/properties/units/` - Create unit (landlords only)
- GET `/api/properties/units/{id}/` - Get unit details

#### Leases
- GET `/api/properties/leases/` - List leases
- POST `/api/properties/leases/` - Create lease (landlords only)

#### Maintenance
- GET `/api/properties/maintenance/` - List maintenance requests
- POST `/api/properties/maintenance/` - Create maintenance request (tenants only)

### User Roles
- **Landlord**: Can create and manage units, leases, and view maintenance requests
- **Tenant**: Can view available units, their leases, and create maintenance requests

### Authentication
The API uses token-based authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your-token>
```

# RentMate
This is the repository of the project named Rent Mate with the Project Managers of G1
