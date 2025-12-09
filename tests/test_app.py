from http import HTTPStatus

from fast_zero.schema import UserPublic


def test_root_return_ok_and_hello_world(client):
    # Act
    response = client.get('/')

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'hello world'}


def test_rooot_return_ok_and_hello_world_html(client):
    response = client.get('/html')

    assert response.status_code == HTTPStatus.OK
    assert '<h1> Hello world </h1>' in response.text


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'ciri',
            'email': 'ciri@example.com',
            'password': '333331',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'ciri',
        'email': 'ciri@example.com',
        'id': user.id,
    }


def test_update_integrity_error(client, user, token):
    client.post(
        '/users',
        json={
            'username': 'ciri',
            'email': 'ciri@example.com',
            'password': '333331',
        },
    )

    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'ciri',
            'email': 'bobo@example.com',
            'password': '333331',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username or email already exists'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(client, token):
    response = client.delete(
        '/users/2', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_update_user_not_found(client, token):
    response = client.put(
        '/users/2',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'ciri',
            'email': 'ciri@example.com',
            'password': '333331',
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_read_user_not_found(client):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_read_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_create_user_username_exists(client, user):
    response = client.post(
        '/users',
        json={
            'username': user.username,
            'email': 'other@test.com',
            'password': '123',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_email_exists(client, user):
    response = client.post(
        '/users',
        json={'username': 'other', 'email': user.email, 'password': '123'},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already exists'}


def test_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token


def test_token_not_user(client):
    response = client.post(
        '/token', data={'username': 'invalid', 'password': 'test'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_token_invalid_password(client, user):
    response = client.post(
        '/token', data={'username': user.email, 'password': 'invalid'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}
