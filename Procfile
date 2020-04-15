release: python manage.py migrate
web: gunicorn mysite.wsgi --log-level debug
web: daphne mysite.asgi:channel_layer --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker -v2
