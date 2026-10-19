import random
import requests

BASE_URL = "http://127.0.0.1:5000/api/products"


def test_get_all_products_api():
    response = requests.get(BASE_URL)
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)


def test_add_product_api():
    unique_name = f"מוצר בדיקה Requests_{random.randint(1000, 9999)}"
    new_product = {
        "name": unique_name,
        "price": 88.0,
        "image": "http://example.com/test.jpg"
    }

    response = requests.post(BASE_URL, json=new_product)
    assert response.status_code in [200, 201]

    data = response.json()
    assert "id" in data


def test_api_bypass_negative_price_rejected():
    payload = {
        "name": "מוצר תקין",
        "price": -500.0,
        "image": "http://example.com/image.jpg"
    }

    response = requests.post(BASE_URL, json=payload)
    assert response.status_code == 400
    assert "error" in response.json()


def test_api_bypass_xss_protection():
    unique_xss_name = f"<script>alert('hack')</script>_{random.randint(1000, 9999)}"

    malicious_payload = {
        "name": unique_xss_name,
        "price": 99.99,
        "image": "http://example.com/hack.jpg"
    }

    response = requests.post(BASE_URL, json=malicious_payload)

    assert response.status_code in [200, 201]


def test_api_bypass_sql_injection_vulnerability():
    unique_sqli_name = f"MaliciousProduct_{random.randint(1000, 9999)}'); DROP TABLE products; --"

    sql_injection_payload = {
        "name": unique_sqli_name,
        "price": 150.0,
        "image": "http://example.com/sql.jpg"
    }

    response = requests.post(BASE_URL, json=sql_injection_payload)

    assert response.status_code in [200, 201]
    data = response.json()
    assert "id" in data

def test_api_type_confusion_price():
    payload = {
        "name": "BadTypeProduct",
        "price": "NotARealPrice! HaHa!",
        "image": "http://example.com/badtype.jpg"
    }

    response = requests.post(BASE_URL, json=payload)

    print(f"Type Confusion Status: {response.status_code}")
    print(f"Type Confusion Response: {response.text}")
    assert response.status_code in [400, 422, 500]