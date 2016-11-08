# Tesis
Tesis

"""
    <GALATEA WEB: Web system simulations>
    Copyright (C) 2016  Erik Velasquez erikvelasquez.25@gmail.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

Install Django-Roles-Permission
https://github.com/vintasoftware/django-role-permissions
https://django-role-permissions.readthedocs.io/en/latest/

Install drivers for mysql
apt-get install python-mysqldb python3-mysqldb         or    pip install MySQL-python

Install drivers for pillow
pip install pillow  or  pip3 install pillow

Install html2text for html manage
pip install html2text

Install java 8
Configure java 8
http://www.webupd8.org/2014/03/how-to-install-oracle-java-8-in-debian.html

Install Galatea
Configure Galatea
http://galatea.sourceforge.net/Home.htm

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
