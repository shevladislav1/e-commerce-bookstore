import json
import requests
from application.settings import API_KEY


def get_data_from_path(data):
    if data == 'rating':
        order_by = 'rating'
    elif data == 'cheap':
        order_by = 'price'
    elif data == 'expansive':
        order_by = '-price'
    else:
        order_by = '-id'

    return order_by


def get_cities():
    url = 'https://api.novaposhta.ua/v2.0/json/'
    data = {
        "apiKey": API_KEY,
        "modelName": "Address",
        "calledMethod": "getCities",
        "methodProperties": {}
    }

    data = json.dumps(data)
    response = requests.get(url=url, data=data)

    return response.json()['data']


def get_warehouses_by_city(city):
    url = 'https://api.novaposhta.ua/v2.0/json/'
    data = {
        "apiKey": API_KEY,
        "modelName": "Address",
        "calledMethod": "getWarehouses",
        "methodProperties": {
            "CityName": f'{city}'
        }
    }

    data = json.dumps(data)
    response = requests.get(url=url, data=data)

    return response.json()['data']
