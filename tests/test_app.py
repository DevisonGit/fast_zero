from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app


def test_root_return_ok_and_hello_world():
    # Arrange
    client = TestClient(app)

    # Act
    response = client.get('/')

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'hello world'}


def test_rooot_return_ok_and_hello_world_html():
    client = TestClient(app)

    response = client.get('/html')

    assert response.status_code == HTTPStatus.OK
    assert '<h1> Hello world </h1>' in response.text
