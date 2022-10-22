import json
from enum import Enum

import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.exceptions import RequestValidationError
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory='')
app = FastAPI()


class DataToSend(Enum):
    number1 = 'Первое слагаемое'
    number2 = 'Второе слагаемое'


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    temp = json.loads(exc.json())
    error_text = f'{DataToSend[temp[0]["loc"][-1]].value} : {temp[0]["msg"]}'
    return templates.TemplateResponse('index.html', {'request': request, 'error': error_text})


@app.get("/calc")
async def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@app.post("/calc")
async def index(request: Request, number1: int = Form(gt=0), number2: int = Form(ge=0)):
    return templates.TemplateResponse('index.html', {'request': request, 'result': number1 + number2})


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
