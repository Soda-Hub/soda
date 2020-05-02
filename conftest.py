import pytest
from starlette.config import environ
from async_asgi_testclient import TestClient

# This sets `os.environ`, but provides some additional protection.
# If we placed it below the application import, it would raise an error
# informing us that 'TESTING' had already been read from the environment.
environ['TESTING'] = 'True'
environ['DATABASE_TEST_URL'] = 'sqlite:///test.db'


from app import app


@pytest.fixture()
async def client():
    """
    When using the 'client' fixture in test cases, we'll get full database
    rollbacks between test cases:

    def test_homepage(client):
        url = app.url_path_for('homepage')
        response = client.get(url)
        assert response.status_code == 200
    """
    async with TestClient(app) as client:
        yield client
