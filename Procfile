web: gunicorn copa.wsgi --log-file -
release: python manage.py makemigrations --noinput && python manage.py migrate --noinput
