"""
WSGI config for web project.
"""
import os
import sys
from pathlib import Path
from django.core.wsgi import get_wsgi_application

# AÑADIDO: que Python vea /repo/web para importar "web.*" (el paquete interno)
PROJECT_DIR = Path(__file__).resolve().parents[1]  # .../repo/web
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')
application = get_wsgi_application()
