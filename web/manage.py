#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path

# === AÑADIDO: hacer que el paquete de proyecto sea el interno "web/web" importable como "web" ===
# /repo/web  (carpeta que contiene el paquete de proyecto "web" con settings.py, urls.py, etc.)
PROJECT_DIR = Path(__file__).resolve().parent  # /repo/web
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

def main():
    """Run administrative tasks."""
    # ahora importamos el settings del paquete interno como "web.settings"
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
