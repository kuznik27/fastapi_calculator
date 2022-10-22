from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_calc_correct_innput():
    response = client.get("/calc")
    assert response.status_code == 200
    assert response.template.filename == 'index.html'


def test_calc_incorrect_numbers():
    response = client.post("/calc", data={"number1": 0, "number2": 0})
    assert response.status_code == 200
    assert response.context['error'] == 'Первое слагаемое : ensure this value is greater than 0'
    response = client.post("/calc", data={"number1": 1, "number2": -1})
    assert response.status_code == 200
    assert response.context['error'] == 'Второе слагаемое : ensure this value is greater than or equal to 0'


def test_calc_incorrect_format_data():
    response = client.post("/calc", data={"number1": 'dummy', "number2": 0})
    assert response.status_code == 200
    assert response.context['error'] == 'Первое слагаемое : value is not a valid integer'
    response = client.post("/calc", data={"number1": 1, "number2": 'dummy'})
    assert response.status_code == 200
    assert response.context['error'] == 'Второе слагаемое : value is not a valid integer'
