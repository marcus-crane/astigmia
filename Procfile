web: gunicorn astigmia.wsgi
release: python manage.py migrate
worker: celery -A astigmia worker -l INFO --without-heartbeat
