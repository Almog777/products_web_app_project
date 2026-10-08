import pytest
from models.models import Product
from repositories.product_repository import (
    create_product,
    read_one,
    read_all,
    update_product,
    delete_product,
    ProductRepositoryError
)


@pytest.fixture(autouse=True)
def clean_database():
    try:
        products = read_all()
        for p in products:
            delete_product(p.product_id)
    except Exception:
        pass


def test_create_product_success():
    p = Product(product_id=None, name="מוצר Repo", price=25.0, image="http://example.com/img.jpg")
    returned_id = create_product(p)

    assert returned_id is not None
    assert p.product_id == returned_id


def test_create_product_missing_name():
    p = Product(product_id=None, name=None, price=20.0, image="")
    with pytest.raises(ProductRepositoryError):
        create_product(p)


def test_create_product_duplicate_name():
    p1 = Product(product_id=None, name="שם ייחודי", price=20.0, image="")
    create_product(p1)

    p2 = Product(product_id=None, name="שם ייחודי", price=30.0, image="")
    with pytest.raises(ProductRepositoryError):
        create_product(p2)


def test_create_product_name_too_long():
    long_name = "א" * 51
    p = Product(product_id=None, name=long_name, price=20.0, image="")
    with pytest.raises(ProductRepositoryError):
        create_product(p)


def test_create_product_missing_price():
    p = Product(product_id=None, name="מוצר ללא מחיר", price=None, image="")
    with pytest.raises(ProductRepositoryError):
        create_product(p)


def test_read_one_existing():
    p = Product(product_id=None, name="מוצר לקריאה", price=15.0, image="")
    product_id = create_product(p)

    fetched = read_one(product_id)
    assert fetched is not None
    assert fetched.product_id == product_id
    assert fetched.name == "מוצר לקריאה"


def test_read_one_not_found():
    result = read_one(99999)
    assert result is None


def test_read_all_empty_and_full():
    assert read_all() == []

    p1 = Product(product_id=None, name="מוצר 1", price=10.0, image="")
    p2 = Product(product_id=None, name="מוצר 2", price=20.0, image="")
    create_product(p1)
    create_product(p2)

    products = read_all()
    assert isinstance(products, list)
    assert len(products) == 2


def test_update_product_success():
    p = Product(product_id=None, name="שם ישן", price=10.0, image="")
    product_id = create_product(p)

    updated_p = Product(product_id=product_id, name="שם חדש", price=12.0, image="")
    result = update_product(updated_p)

    assert result is True
    assert read_one(product_id).name == "שם חדש"


def test_update_product_not_found():
    p = Product(product_id=99999, name="לא קיים", price=10.0, image="")
    result = update_product(p)
    assert result is False


def test_update_product_invalid_data_keeps_old_data():
    p = Product(product_id=None, name="מוצר מקורי", price=100.0, image="")
    product_id = create_product(p)

    invalid_p = Product(product_id=product_id, name="א" * 51, price=100.0, image="")
    with pytest.raises(ProductRepositoryError):
        update_product(invalid_p)

    assert read_one(product_id).name == "מוצר מקורי"



def test_delete_product_success():
    p = Product(product_id=None, name="למחיקה", price=5.0, image="")
    product_id = create_product(p)

    result = delete_product(product_id)
    assert result is True
    assert read_one(product_id) is None


def test_delete_product_not_found():
    result = delete_product(99999)
    assert result is False

def test_create_product_name_exact_minimum_length():
    p = Product(product_id=None, name="אב", price=10.0, image="")
    returned_id = create_product(p)
    assert returned_id is not None


def test_create_product_name_exact_maximum_length():
    exact_50_name = "א" * 50
    p = Product(product_id=None, name=exact_50_name, price=10.0, image="")
    returned_id = create_product(p)
    assert returned_id is not None

@pytest.mark.xfail(reason="BUG: System accepts whitespace-only name instead of raising ProductServiceError/ProductRepositoryError")
def test_create_product_name_whitespace_only():
    p = Product(product_id=None, name="   ", price=10.0, image="")
    with pytest.raises(ProductRepositoryError):
        create_product(p)


def test_create_product_name_special_characters_and_emoji():
    p = Product(product_id=None, name="חולצה 👕 #123!", price=40.0, image="")
    returned_id = create_product(p)
    assert returned_id is not None