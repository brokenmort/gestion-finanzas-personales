"""
ASGI config for web project.

It exposes the ASGI callable as a module-level variable named ``application``.
"""

import os
import sys
from pathlib import Path
from django.core.asgi import get_asgi_application

# Añadir la raíz del repo al PYTHONPATH
# Este archivo está en .../web/web/asgi.py → subimos 2 niveles hasta la raíz del repo
REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Configuración del módulo de settings correcto
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.web.settings')

application = get_asgi_application()
