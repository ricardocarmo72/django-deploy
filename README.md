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
Just download the deploy.py file and type:

`python deploy.py <alias> <port> <workers> <python_version> <django_version> <url>`

where:

  - **_alias_** is the project name of your Django application (directory name with no spaces)
  - **_port_** is the port used by gunicorn process
  - **_workers_** is the number of workers
  - **_python_version_** is python2 or python3
  - **_django_version_** is the Django version, ex: 1.9, 2.0, 2.0.4 etc
  - **_url_** is the domain name of application, ex: www.mywebapp.com
    
