from http import HTTPStatus


def test_root_deve_retornar_ok_hello_world(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'hello world'}


def test_root_html_deve_retornar_ok_ola_mundo(client):
    response = client.get('/html')

    assert response.status_code == HTTPStatus.OK
    assert '<h1> ola mundo </h1>' in response.text
