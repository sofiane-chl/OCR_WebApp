"""Shared pytest fixtures."""

import pytest
from fastapi.testclient import TestClient

from ocr_webapp.api.app import create_app


@pytest.fixture(scope="session")
def app():
    return create_app()


@pytest.fixture(scope="session")
def client(app):
    return TestClient(app)
