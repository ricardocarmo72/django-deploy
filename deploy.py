# -*- coding: utf-8 -*-
import os
import sys
import stat
from subprocess import call

SUPERVISOR = '''[program:%s]
command = /var/www/webapps/%s/env/bin/gunicorn -c /var/www/gunicorn/%s.py %s.wsgi:application
directory = /var/www/webapps/%s/public/
autostart = true
autorestart = true
autoreload = true
stderr_logfile = /var/www/webapps/%s/logs/long.err.log
stdout_logfile = /var/www/webapps/%s/logs/long.out.log'''

GUNICORN = '''command = "/var/www/webapps/%s/env/bin/gunicorn"
pythonpath = "/var/www/webapps/%s/env/"
user = "suporte"
group = "www-data"
bind = "0.0.0.0:%s"
workers = %s'''

INSTALL = '''#!/bin/bash
virtualenv -p %s env 
source env/bin/activate
env/bin/pip install -U pip
env/bin/pip install Django==%s
env/bin/pip install gunicorn
django-admin startproject %s ./public
deactivate'''

NGINX_SERVER = '''server {
        server_name %s;

        access_log /var/www/webapps/%s/logs/nginx_access.log;
        error_log  /var/www/webapps/%s/logs/nginx_error.log;

        location /static {
                alias /var/www/webapps/%s/public/static;
        }

        location / {
                proxy_pass_header Server;
                proxy_set_header Host $http_host;
                proxy_redirect off;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Scheme $scheme;
                proxy_connect_timeout 60;
                proxy_read_timeout 60;
                proxy_pass http://0.0.0.0:%s/;
                add_header P3P 'CP="ALL DSP COR PSAa PSDa OUR NOR ONL UNI COM NAV"';
        }
}'''

ACTIVATE = '''#!/bin/bash
supervisorctl reload
ln -s /etc/nginx/sites-available/%s.conf /etc/nginx/sites-enabled/
service nginx reload'''

def runScript(DIR, content):
    os.chdir(DIR)
    path = DIR+'/run.sh'
    with open(path, 'w') as f:
        f.write(content)
    
    st = os.stat(path)
    os.chmod(path, st.st_mode | stat.S_IEXEC)
    call([path])

def setAllowedHosts(path, url):
    with open(path,'r') as f:
        linhas = f.readlines()
    
    f = open(path,'w')
    for i in range(len(linhas)):
        if "ALLOWED_HOSTS" in linhas[i]:
            f.write("ALLOWED_HOSTS = ['%s']\n" % url)
        else: 
            f.write(linhas[i]+'\n')
    f.close()

def newProject(alias, port, workers, python_version, django_version, url):
    dirs = ['/var/www',
            '/var/www/supervisor',
            '/var/www/gunicorn',
            '/var/www/webapps',
            '/var/www/webapps/%s' % alias,
            '/var/www/webapps/%s/env' % alias,
            '/var/www/webapps/%s/logs' % alias,
            '/var/www/webapps/%s/public' % alias]
    
    for dir in dirs:
        if not os.path.exists(dir):
            os.makedirs(dir)
    
    content = SUPERVISOR % (alias, alias, alias, alias, alias, alias, alias)
    with open('/var/www/supervisor/%s.conf' % alias, 'w') as f:
        f.write(content)
    
    content = GUNICORN % (alias, alias, port, workers)
    with open('/var/www/gunicorn/%s.py' % alias, 'w') as f:
        f.write(content)
    
    content = NGINX_SERVER % (url, alias, alias, alias, port) 
    with open('/etc/nginx/sites-available/%s.conf' % alias, 'w') as f:
        f.write(content)

    DIR = '/var/www/webapps/%s' % alias
    
    content = INSTALL % (python_version, django_version, alias)
    runScript(DIR, content)        

    setAllowedHosts('/var/www/webapps/%s/public/%s/settings.py' % (alias, alias), url)
    
    content = ACTIVATE % alias
    runScript(DIR, content)
    
alias          = input("Enter the project alias: ") #ex. myproject
port           = input("Gunicorn port: ") # ex. 8001
workers        = input("Number of workers: ") # ex. 2
python_version = input("Python version: ") # ex. python3, python3.7 etc
django_version = input("Django version: ") # ex. 2.0
url            = input("Hostname application: ") # ex. myproject.mybusiness.com

newProject(alias,port,workers,python_version,django_version,url)
