import os,sys

sys.path.insert(0,'/home/k/kivvesty/kivvesty.beget.tech/project')
sys.path.insert(1,'/home/k/kivvesty/kivvesty.beget.tech/djangoenv/lib/python3.10/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

