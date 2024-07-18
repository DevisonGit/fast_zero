from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app


def test_root_retornar_ok_e_hello_world():
    client = TestClient(app)

    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello world!'}


def test_root_retornar_ok_e_hello_world_html():
    client = TestClient(app)

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
