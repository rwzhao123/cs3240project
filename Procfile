release: python manage.py migrate
web: gunicorn mysite.wsgi --log-level debug
daphne -p 8001 mysite.asgi:application
daphne mysite.asgi:application
daphne -b 0.0.0.0 -p 8001 mysite.asgi:application
