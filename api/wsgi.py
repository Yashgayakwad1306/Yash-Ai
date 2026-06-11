# api/wsgi.py
import os
from django.core.wsgi import get_wsgi_application

# Point to your main aichat folder settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aichat.settings')

application = get_wsgi_application()

app = application