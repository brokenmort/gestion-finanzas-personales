#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path


def main():
    """Run administrative tasks."""
    # Añadimos /repo/web al PYTHONPATH para que 'users', 'urls', 'wsgi' funcionen
    WEB_ROOT = Path(__file__).resolve().parent  # .../repo/web
    if str(WEB_ROOT) not in sys.path:
        sys.path.insert(0, str(WEB_ROOT))

    # OJO: settings dentro de web/web/settings.py se importa como 'web.settings'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
