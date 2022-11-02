import pytest
from flask import template_rendered
from contextlib import contextmanager
from Python_Testing import server


@contextmanager
def captured_templates(app):
    """defines helper context manager that can be used in a unit
    test to determine which templates were rendered and what
    variables were passed to the template"""
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)


@pytest.fixture
def client():
    """client app configuration for testing purposes"""
    app = server.app
    with captured_templates(app) as templates:
        with app.test_client() as client:
            yield client, templates
