web: gunicorn astigmia.wsgi
release: python manage.py migrate
worker: celery -A astigmia worker -B -l INFO --without-heartbeat
