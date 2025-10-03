## RentMate (Python + JS Hybrid)

Backend: FastAPI (Python)
Frontend: Static HTML/CSS with small JS calling the Python API

### Prerequisites
- Python 3.10+

### Setup
1. Create venv and install deps:
```
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
```
2. Configure Supabase Postgres connection (optional):
   - In Supabase project, copy the connection string (General > Connection string > URI). It looks like:
     `postgresql://postgres:YOUR_PASSWORD@YOUR_HOST:5432/postgres`
   - Set environment variable before running (Windows PowerShell):
     ```
     $env:DATABASE_URL="postgresql://postgres:YOUR_PASSWORD@YOUR_HOST:5432/postgres"
     ```

3. Run API:
```
uvicorn backend.main:app --reload
```
API runs at `http://127.0.0.1:8000`.

3. Open `index.html` with a local server (e.g. VS Code Live Server) or any static server.

### Endpoints
- POST /api/register
  - body: { email, password, firstName?, lastName?, address?, phone?, city?, state? }
  - returns: { access_token, token_type }
- POST /api/login
  - body: { email, password }
  - returns: { access_token, token_type }

Roles supported: set `role` in body to `landlord` or `tenant` (default `tenant`).

### Configuration
Optionally set `window.API_BASE` in a small inline script before loading `api.js` if your API is hosted elsewhere.

# RentMate
This is the repository of the project named Rent Mate with the Project Managers of G1
