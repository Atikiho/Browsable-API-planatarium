# Browsable API planetarium
API which allows you to view show themes, sessions, reservations and tickets reservation by your own

### Getting started

###### Create .env file using .env_sample as sample. It's crucial because code is using .env variables and won't work without it

##### Installing using GitHub
```
git clone https://github.com/Atikiho/Browsable-API-planetarium.git
docker-compose up --build
cd Browsable-API-planetarium
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
python manage.py runserver 8000
```
API is available on http://127.0.0.1:8000/
##### Using Docker
```
git clone https://github.com/Atikiho/Browsable-API-planetarium.git
docker-compose up --build
```

API is available on http://127.0.0.1:8001/

##### Getting access
create user via /api/user/register/
get access token via api/user/token

### Technologies
 - Python
 - Django
 - DRF
 - Docker
 - SQLite
 - PostgreSQL

### Features
 - Authentication via JWT tokens
 - registration and token obtain via email
 - Documentation at api/doc/swagger/
 - CRUD operations for show themes, astronomy shows, planetarium domes, show sessions and tickets
 - filtering for astronomy shows
 - automatically creating reservation on ticket creation
 - deleting reservation on ticket deletion via signals