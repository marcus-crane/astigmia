web: cd astigmia && gunicorn astigmia.wsgi
release: cd astigmia && python manage.py migrate
worker: cd astigmia && celery -A astigmia worker -B -l INFO --without-heartbeat
