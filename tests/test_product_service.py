import pytest

from models.models import Product

from services.product_service import (
    add_product,
    get_product,
    get_all_products,
    update_product,
    delete_product,
    ProductServiceError,
    ProductNotFoundServiceError
)

from repositories.product_repository import read_all, delete_product as repo_delete_product


@pytest.fixture(autouse=True)
def clean_database():
    try:
        existing_products = read_all()
        for product in existing_products:
            repo_delete_product(product.product_id)
    except Exception:
        pass



def test_add_product_success():
    p = Product(product_id=None, name="חולצה", price=50.0, image="http://example.com/img.jpg")
    product_id = add_product(p)

    assert product_id is not None


def test_add_product_name_too_short():
    p = Product(product_id=None, name="א", price=50.0, image="")
    with pytest.raises(ProductServiceError):
        add_product(p)


def test_add_product_negative_price():
    p = Product(product_id=None, name="מכנס", price=-10.0, image="")
    with pytest.raises(ProductServiceError):
        add_product(p)


def test_add_product_zero_price_allowed():
    p = Product(product_id=None, name="מוצר חינם", price=0.0, image="")
    product_id = add_product(p)
    assert product_id is not None


def test_get_product_not_found():
    with pytest.raises(ProductNotFoundServiceError):
        get_product(99999)


def test_get_all_products():
    products = get_all_products()
    assert isinstance(products, list)


def test_update_product_not_found():
    p = Product(product_id=99999, name="מוצר פיקטיבי", price=20.0, image="")
    with pytest.raises(ProductNotFoundServiceError):
        update_product(p)


def test_delete_product_not_found():
    with pytest.raises(ProductNotFoundServiceError):
        delete_product(99999)


def test_add_product_missing_name():
    p1 = Product(product_id=None, name=None, price=50.0, image="")
    with pytest.raises(ProductServiceError):
        add_product(p1)

    p2 = Product(product_id=None, name="", price=50.0, image="")
    with pytest.raises(ProductServiceError):
        add_product(p2)


def test_add_product_missing_price():
    p = Product(product_id=None, name="מוצר ללא מחיר", price=None, image="")
    with pytest.raises(ProductServiceError):
        add_product(p)

def test_add_product_repository_error_wrapped():
    p1 = Product(product_id=None, name="מוצר ייחודי", price=50.0, image="")
    add_product(p1)

    p2 = Product(product_id=None, name="מוצר ייחודי", price=30.0, image="")
    with pytest.raises(ProductServiceError):
        add_product(p2)

def test_get_product_success():
    p = Product(product_id=None, name="חולצה ירוקה", price=80.0, image="")
    product_id = add_product(p)

    fetched_product = get_product(product_id)
    assert fetched_product is not None
    assert fetched_product.product_id == product_id
    assert fetched_product.name == "חולצה ירוקה"


def test_update_product_success():
    p = Product(product_id=None, name="שעון ישן", price=100.0, image="")
    product_id = add_product(p)

    updated_p = Product(product_id=product_id, name="שעון חדש", price=150.0, image="")
    result = update_product(updated_p)

    assert result is None

    saved_p = get_product(product_id)
    assert saved_p.name == "שעון חדש"
    assert saved_p.price == 150.0


def test_update_product_invalid_input_raises_service_error():
    p = Product(product_id=None, name="מוצר תקין", price=50.0, image="")
    product_id = add_product(p)

    invalid_p = Product(product_id=product_id, name="מוצר תקין", price=-20.0, image="")
    with pytest.raises(ProductServiceError):
        update_product(invalid_p)


def test_delete_product_success():
    p = Product(product_id=None, name="מוצר למחיקה", price=40.0, image="")
    product_id = add_product(p)

    result = delete_product(product_id)

    assert result is None

    with pytest.raises(ProductNotFoundServiceError):
        get_product(product_id)


def test_add_product_name_exact_minimum_length_success():
    p = Product(product_id=None, name="גג", price=15.0, image="")
    product_id = add_product(p)
    assert product_id is not None

@pytest.mark.xfail(reason="BUG: System accepts whitespace-only instead of raising ProductServiceError")
def test_add_product_name_whitespace_only_raises_error():
    p = Product(product_id=None, name="  ", price=15.0, image="")
    with pytest.raises(ProductServiceError):
        add_product(p)