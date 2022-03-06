python manage.py collectstatic --noinput

python manage.py makemigrations

python manage.py migrate

gunicorn --worker-tmp-dir /dev/shm CRM_App.wsgi