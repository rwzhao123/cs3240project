release: python manage.py migrate
web: gunicorn mysite.wsgi --log-level debug
daphne chat.asgi:channel_layer --port $PORT --bind 0.0.0.0 -v2
