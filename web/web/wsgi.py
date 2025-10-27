"""
WSGI config for web project.
"""

import os
import sys
from pathlib import Path
from django.core.wsgi import get_wsgi_application

# Este archivo está en .../web/web/wsgi.py
# Raíz del repo = 2 niveles arriba
REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.web.settings')

application = get_wsgi_application()
