#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path


def main():
    """Run administrative tasks."""
    # <<< CLAVE: agregar /repo/web al PYTHONPATH >>>
    WEB_ROOT = Path(__file__).resolve().parent  # .../repo/web
    if str(WEB_ROOT) not in sys.path:
        sys.path.insert(0, str(WEB_ROOT))

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.web.settings')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
