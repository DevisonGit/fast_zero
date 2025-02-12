from http import HTTPStatus


def test_root_deve_retorna_ok_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'olá mundo!'}


def test_root_html_retorna_ok_e_ola_mundo(client):
    response = client.get('/html')

    assert response.status_code == HTTPStatus.OK
    assert (
        response.text
        == """
    <html>
        <head>
            <title> Nosso olá mundo! </title>
        </head>
        <body>
            <h1> Olá Mundo </h1>
        </body>
    </html>
    """
    )
