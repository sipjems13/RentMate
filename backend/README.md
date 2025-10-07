# RentMate Django Backend

This is the Django backend for the RentMate rental management system.

## Setup Instructions

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Environment Variables**
   - Copy `env.example` to `.env`
   - Update the values as needed

3. **Run Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create Superuser (Optional)**
   ```bash
   python manage.py createsuperuser
   ```

5. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```
   
   Or use the convenience script:
   ```bash
   python run_server.py
   ```

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/profile/` - Get user profile
- `PUT /api/auth/profile/` - Update user profile

### Properties
- `GET /api/properties/units/` - List units
- `POST /api/properties/units/` - Create unit (landlords only)
- `GET /api/properties/units/{id}/` - Get unit details
- `PUT /api/properties/units/{id}/` - Update unit (landlords only)
- `DELETE /api/properties/units/{id}/` - Delete unit (landlords only)

### Leases
- `GET /api/properties/leases/` - List leases
- `POST /api/properties/leases/` - Create lease (landlords only)
- `GET /api/properties/leases/{id}/` - Get lease details
- `PUT /api/properties/leases/{id}/` - Update lease (landlords only)
- `DELETE /api/properties/leases/{id}/` - Delete lease (landlords only)

### Maintenance
- `GET /api/properties/maintenance/` - List maintenance requests
- `POST /api/properties/maintenance/` - Create maintenance request (tenants only)
- `GET /api/properties/maintenance/{id}/` - Get maintenance request details
- `PUT /api/properties/maintenance/{id}/` - Update maintenance request
- `DELETE /api/properties/maintenance/{id}/` - Delete maintenance request

## Authentication

The API uses token-based authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your-token>
```

## User Roles

- **Landlord**: Can create and manage units, leases, and view maintenance requests
- **Tenant**: Can view available units, their leases, and create maintenance requests

## Database

The default configuration uses SQLite for development. For production, update the database settings in `rentmate/settings.py`.

