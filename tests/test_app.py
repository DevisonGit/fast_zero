from http import HTTPStatus


def test_root_retornar_ok_e_hello_world(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello world!'}


def test_root_retornar_ok_e_hello_world_html(client):
    response = client.get('/html')

    assert response.status_code == HTTPStatus.OK
    assert (
        response.text
        == """
    <html>
        <head>
            <title> Nosso hello world</title>
        </head>
        <body>
            <h1> Hello World! </h1>
        </body>
    </html>
    """
    )


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@exemplo.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'alice',
        'email': 'alice@exemplo.com',
    }


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'id': 1,
                'username': 'alice',
                'email': 'alice@exemplo.com',
            },
        ]
    }


def test_update_users(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'alice',
            'email': 'alice@exemplo.com.br',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'alice',
        'email': 'alice@exemplo.com.br',
    }


def test_update_not_found(client):
    response = client.put(
        '/users/0',
        json={
            'username': 'alice',
            'email': 'alice@exemplo.com.br',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(client):
    response = client.delete('/users/0')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
