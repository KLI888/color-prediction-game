release: python manage.py migrate
web: daphne celery_project.asgi:application --port $PORT --bind 0.0.0.0 -v2
celery: celery -A celery_project.celery worker --pool=solo -i info
celerybeat: celery -A celery_project beat -l info