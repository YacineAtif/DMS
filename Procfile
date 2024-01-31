web: gunicorn DMS.wsgi
web: daphne -p $PORT DMS.asgi:application
web: python manage.py runserver 0.0.0.0:\$PORT
