python manage.py collectstatic --noinput

python manage.py makemigrations --noinput

python manage.py migrate --noinput

gunicorn --worker-tmp-dir /dev/shm CRM_App.wsgi