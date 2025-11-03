import pytest

from customer import Customer


def test_customer_invalid():
    with pytest.raises(AttributeError):
        Customer("", "0123456")
    with pytest.raises(AttributeError):
        Customer("A", "0123456")
    with pytest.raises(AttributeError):
        Customer("Tim", "abc")
    with pytest.raises(AttributeError):
        Customer("Tim", 123456)
