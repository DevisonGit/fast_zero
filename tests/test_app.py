from http import HTTPStatus


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
