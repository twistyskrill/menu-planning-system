import os

import django
import pytest

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "menu_project.settings")
django.setup()

from django.core.management import call_command  # noqa: E402
from django.db import transaction  # noqa: E402
from django.test.utils import setup_databases, teardown_databases  # noqa: E402


@pytest.fixture(scope="session")
def orm_database():
    config = setup_databases(verbosity=0, interactive=False)
    try:
        yield
    finally:
        teardown_databases(config, verbosity=0)


@pytest.fixture
def empty_orm(orm_database):
    with transaction.atomic():
        yield
        transaction.set_rollback(True)


@pytest.fixture
def seeded_orm(empty_orm):
    call_command("import_pr7")
