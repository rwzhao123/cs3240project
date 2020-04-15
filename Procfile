release: python manage.py migrate
web: gunicorn mysite.wsgi --log-level debug
daphne -b 0.0.0.0 -p 8001 mysite.asgi:application
