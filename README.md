# Tesis
Tesis


Install Django-Roles-Permission
https://github.com/vintasoftware/django-role-permissions
https://django-role-permissions.readthedocs.io/en/latest/

Install drivers for mysql
apt-get install python-mysqldb

Install html2text for html manage
pip install html2text

Create DB and configuration

Copy secrets_example to secrets and configure
cp secrets_exaple.py secrets.py

Run migrations
python manage.py migrate

Create super user
python manage.py createsuperuser

Create image for superuser
In Model UserImage

Create Folder for superuser
In Model Folder

Create DiskSpace for superuser
In Model DiskSpace

