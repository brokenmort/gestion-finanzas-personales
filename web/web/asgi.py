"""
ASGI config for web project.

It exposes the ASGI callable as a module-level variable named ``application``.
"""

import os
import sys
from pathlib import Path
from django.core.asgi import get_asgi_application

# Añade la raíz del repo al PYTHONPATH para que se encuentren apps como 'users'
# Este archivo está en .../web/web/asgi.py  -> subimos 3 niveles hasta la raíz del repo
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Ajusta a tu módulo de settings real
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.web.settings')

application = get_asgi_application()
