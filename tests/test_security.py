from http import HTTPStatus

from jwt import decode

from fast_zero.security import (
    SECRET_KEY,
    create_access_token,
)


def test_jwt():
    data = {'test': 'test'}
    token = create_access_token(data)

    decoded = decode(token, SECRET_KEY, algorithms=['HS256'])

    assert decoded['test'] == data['test']
    assert 'exp' in decoded


def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer token-invalid'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_token_not_sub(client):
    data = {'test': 'test'}
    token = create_access_token(data)

    response = client.delete(
        '/users/1', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_token_not_user(client, token):
    # data = {'username': 'invalid@teste.com', 'password': 'invalid'}
    # token = create_access_token(data)

    response = client.delete(
        '/users/2', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
