from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from schemas import Message

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Hello world!'}


@app.get('/html', response_class=HTMLResponse)
def read_root_html():
    return """
    <html>
        <head>
            <title> Nosso hello world</title>
        </head>
        <body>
            <h1> Hello World! </h1>
        </body>
    </html>
    """
