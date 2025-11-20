# personal-notes-manager-209715-209751

Backend: Django + DRF Notes API

How to run locally:
- Install requirements: pip install -r notes_backend/requirements.txt
- Apply migrations: python notes_backend/manage.py migrate
- Create superuser (optional): python notes_backend/manage.py createsuperuser
- Start server: python notes_backend/manage.py runserver 0.0.0.0:3001

Auth:
- POST /api/auth/register { "username": "...", "password": "..." } -> { token, username }
- POST /api/auth/token { "username": "...", "password": "..." } -> { token, username }
Use header: Authorization: Token <token>

Notes:
- GET /api/notes?search or ?q=term
- POST /api/notes { title, content }
- GET /api/notes/{id}
- PATCH /api/notes/{id} { title?, content? }
- DELETE /api/notes/{id}

Health:
- GET /api/health/

Docs:
- /docs
- /redoc
