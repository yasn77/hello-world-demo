import pytest
import json
from hello_world.hello import app


def test_index_route_string():
    response = app.test_client().get('/')

    assert response.status_code == 200
    assert response.data.decode('utf-8') == 'Hello, World!'


def test_name_route_string():
    response = app.test_client().get('/hello/tester')

    assert response.status_code == 200
    assert response.data.decode('utf-8') == 'Hello, Tester!'


def test_index_route_json():
    response = app.test_client().get('/?output=json')

    resp = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert resp['output'] == 'Hello, World!'
    assert resp['name'] == 'World'


def test_name_route_json():
    response = app.test_client().get('/hello/tester?output=json')

    resp = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert resp['output'] == 'Hello, Tester!'
    assert resp['name'] == 'Tester'
