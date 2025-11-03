import pytest

from account import Account
from customer import Customer


@pytest.fixture
def tim():
    """Tim is a regular customer"""
    return Customer("Tim", "142904328")


@pytest.fixture
def tim_acc(tim):
    """Tim's account"""
    return Account(tim)


def test_invalid_account():
    """The Account initialization takes a Customer instance, not a string!"""
    with pytest.raises(TypeError):
        Account("Tim")


def test_account(tim_acc):
    """Check attributes of the instance"""
    assert tim_acc.owner.name == "Tim"
    assert tim_acc.amount == 0


def test_account_deposit(tim_acc):
    """Deposit method"""
    tim_acc.deposit(1000)
    assert tim_acc.amount == 1000

    tim_acc.deposit(100)
    assert tim_acc.amount == 1100

    with pytest.raises(AttributeError):
        tim_acc.deposit(-500)

    assert tim_acc.amount == 1100


def test_account_withdraw(tim_acc):
    """Withdraw method"""
    tim_acc.withdraw(1000)
    assert tim_acc.amount == -1000

    tim_acc.withdraw(100)
    assert tim_acc.amount == -1100

    with pytest.raises(AttributeError):
        tim_acc.deposit(-500)
    assert tim_acc.amount == -1100


def test_account_transfer(tim_acc):
    """Transfer money between accounts"""
    other_person = Customer("Other", "89048904")
    other_account = Account(other_person)
    tim_acc.deposit(1000)
    tim_acc.transfer(other_account, 500)

    assert tim_acc.amount == 500
    assert other_account.amount == 500
