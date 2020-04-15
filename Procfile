release: python manage.py migrate
web: gunicorn mysite.wsgi --log-level debug
worker: daphne mysite.asgi:application --port $PORT --bind 0.0.0.0
