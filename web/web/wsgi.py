"""
WSGI config for web project.
"""
import os
import sys
from pathlib import Path
from django.core.wsgi import get_wsgi_application

# === AÑADIDO: asegurar que el repo root está en sys.path ===
BASE_DIR = Path(__file__).resolve().parents[2]  # .../repo/
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.web.settings')
application = get_wsgi_application()
