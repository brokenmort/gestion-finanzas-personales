#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path


def main():
    """Run administrative tasks."""
    # AÑADIR la raíz del repo al PYTHONPATH para que encuentre apps como 'users'
    current_dir = Path(__file__).resolve().parent          # .../web
    project_root = current_dir.parent                      # raíz del repo
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    # Tu settings real vive en web/web/settings.py
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.web.settings')

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
