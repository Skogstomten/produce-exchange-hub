"""config for tests."""

pytest_plugins = [
    "tests.fixtures.mongo_document_database_fixtures",
    "tests.fixtures.user_fixtures",
]
