import pytest
from app import app

from models.users import user_manager


@pytest.mark.asyncio
async def test_users(client):
    response = await client.get('/')
    assert response.status_code == 404

    await user_manager.add_user('testuser', '1234')

    response = await client.get('/', query_string={'username': 'testuser'})
    assert response.status_code == 200
