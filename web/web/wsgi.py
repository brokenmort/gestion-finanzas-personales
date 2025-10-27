import os
import sys
from pathlib import Path

# AÑADIR la raíz del repo al PYTHONPATH
# Este archivo está en .../web/web/wsgi.py -> subimos 3 niveles hasta la raíz
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.web.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
