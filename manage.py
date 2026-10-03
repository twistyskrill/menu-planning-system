#!/usr/bin/env python
"""Командная утилита Django."""
import os
import sys


def main() -> None:
    """Запустить административную команду Django."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "menu_project.settings")
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
