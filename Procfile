release: cd web && python manage.py migrate && python manage.py collectstatic --noinput
web: cd web && gunicorn web.wsgi --log-file -
web: gunicorn web.gestion_finanzas.wsgi
