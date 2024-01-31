web: gunicorn DMS.wsgi
web: daphne -p $PORT DMS.asgi:application
web: daphne -b 0.0.0.0 -p ${PORT:-8000} DMS:application
web: python manage.py runserver 0.0.0.0:8000
