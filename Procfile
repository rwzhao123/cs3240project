release: python manage.py migrate
web: daphne -b 0.0.0.0 -p 8001 mysite.asgi:application
worker: daphne -e ssl:443:privateKey=key.pem:certKey=crt.pem mysite.asgi:application
