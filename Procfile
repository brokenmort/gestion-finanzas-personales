release: python web/manage.py migrate && python web/manage.py collectstatic --noinput
web: cd web && gunicorn web.wsgi --log-file -
