from http import HTTPStatus


def test_read_root_retonar_ok_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Ola Mundo'}


def test_read_root_html_ok_e_ola_mundo(client):
    response = client.get('/html')

    assert response.status_code == HTTPStatus.OK
    assert (
        response.text
        == """
    <html>
        <head>
            <title>Nosso ola mundo</title>
        </head>
        <body>
            <h1> Olá Mundo </h1>
        </body>
    </html>
    """
    )
