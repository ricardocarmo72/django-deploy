# django-deploy

This is a python script that creates a new Django application on development or production server, deploying automatically trough NGINX webserver.

### Pre-requisites
This script assumes the following pre-requisites:

- Your server has NGINX installed on /etc/nginx
- Your server has supervisor installed on /etc/supervisor
- The archive /etc/supervisor/supervisord.conf contains the line:

`files=/var/www/supervisor/*.conf`

- The script must to be running with root privileges.

### How to use
Just download the deploy.py file, type:

`python deploy.py`

And enter the required parameters:

- alias          #ex. myproject
- port           #ex. 8001
- workers        # ex. 2
- python_version # ex. python3
- django_version # ex. 2.0
- url            # ex. myproject.mybusiness.com
