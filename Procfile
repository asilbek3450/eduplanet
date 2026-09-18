release: python manage.py migrate --noinput && python manage.py sync_platform_content && python manage.py collectstatic --noinput
web: gunicorn root.wsgi:application
