#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path

def main():
    # Añade la raíz del repo al PYTHONPATH para encontrar apps como 'users'
    # Este archivo está en .../web/manage.py -> la raíz del repo es parent de 'web'
    REPO_ROOT = Path(__file__).resolve().parent.parent
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.web.settings')

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
