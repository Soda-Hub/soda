import json
import pytest
from app import app
from settings import ALLOWED_HOSTS

from models.users import user_manager
from models.crypto_utils import encrypt_password, compare_password


def test_password():
    pwd = '1234'
    encrypted = encrypt_password(pwd)
    assert compare_password(pwd, encrypted) is True

    assert compare_password('12345', encrypted) is False


@pytest.mark.asyncio
async def test_webfinger(client):
    url = '/.well-known/webfinger'
    response = await client.get(url)
    assert response.status_code == 400

    domain = ALLOWED_HOSTS[0]
    response = await client.get(url, query_string={
        'resource': 'abc@' + 'abc' + domain})
    assert response.status_code == 404

    response = await client.get(url, query_string={
        'resource': 'abc@' + domain})
    assert response.status_code == 404

    await user_manager.add_user('testuser', '1234')

    response = await client.get(url, query_string={
        'resource': 'testuser@'+domain})
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_users(client):
    url = '/users/'
    response = await client.get(url + 'testuser')
    assert response.status_code == 404

    await user_manager.add_user('testuser', '1234')

    response = await client.get(url + 'testuser')
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_user_followers(client):
    url = '/users/testuser/followers'
    response = await client.get(url)
    assert response.status_code == 404

    await user_manager.add_user('testuser', '1234')

    response = await client.get(url)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_user_inbox(client):
    url = '/users/testuser/inbox'
    response = await client.post(url, data={})
    assert response.status_code == 400

    data = {'id': '123',
            'type': 'Follow',
            'actor': 'abc@cde.com',
            'object': 'testuser@' + ALLOWED_HOSTS[0]}

    response = await client.post(url, json=data)
    assert response.status_code == 404

    await user_manager.add_user('testuser', '1234')

    response = await client.post(url, json=data)
    assert response.status_code == 200

    data = {'id': '123',
            'type': 'Undo',
            'actor': 'abc@cde.com',
            'object':
                {'id': '123',
                'type': 'Follow',
                'actor': 'abc@cde.com',
                'object': 'testuser@' + ALLOWED_HOSTS[0]}}

    response = await client.post(url, json=data)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_user_outbox(client):
    url = '/users/testuser/outbox'
    response = await client.get(url)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_shared_inbox(client):
    url = '/inbox'
    response = await client.post(url, data={})
    assert response.status_code == 200
