release: cd web && python manage.py migrate && python manage.py collectstatic --noinput
web: cd web && gunicorn gestion_finanzas.wsgi --log-file -