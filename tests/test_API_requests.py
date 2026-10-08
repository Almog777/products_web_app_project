import pytest
import requests

BASE_URL = "http://127.0.0.1:5000/api/products"


def test_get_all_products_api():
    response = requests.get(BASE_URL)

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)


def test_add_product_api():
    new_product = {
        "name": "מוצר בדיקה Requests",
        "price": 88.0,
        "image": "http://example.com/test.jpg"
    }

    response = requests.post(BASE_URL, json=new_product)

    assert response.status_code in [200, 201]

    data = response.json()
    assert "id" in data