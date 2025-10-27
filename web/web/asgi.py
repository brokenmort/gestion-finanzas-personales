"""
ASGI config for web project.
"""
import os
import sys
from pathlib import Path
from django.core.asgi import get_asgi_application

# Añadimos /repo/web al PYTHONPATH
WEB_ROOT = Path(__file__).resolve().parents[1]  # .../repo/web
if str(WEB_ROOT) not in sys.path:
    sys.path.insert(0, str(WEB_ROOT))

# settings vive en /repo/web/web/settings.py => 'web.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.web.settings')

application = get_asgi_application()
