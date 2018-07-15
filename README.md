# django-deploy

This is a python script that creates a new Django application on development or production server, deploying automatically trough nginx webserver.

This script assumes the following pre-requisites:

-Your server has supervisor installed on /etc/supervisor
-The archive /etc/supervisor/supervisord.conf contains the line:

files=/var/www/supervisor/*.conf

-Your server has nginx installed on /etc/nginx
-The script must to be running with root privileges.

To run the script:
python deploy.py alias xxxx n url_web

Where:
alias: Is a name to your app, used in directories names.
xxxx: Is the port to bind gunicorn process.
n: Number of workers.
url_web: server url to your app.

Sample:
sudo python deploy.py mywebapp 8001 3 http://www.mywebapp.com
