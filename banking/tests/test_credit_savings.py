import pytest

from account import Account, CreditAccount, SavingsAccount
from customer import Customer


@pytest.fixture
def tim():
    """Tim is a regular customer"""
    return Customer("Tim", "142904328")


@pytest.fixture
def credit10(tim):
    """Credit account with 10% interest"""
    return CreditAccount(tim, 10)


@pytest.fixture
def savings(tim):
    """Savings account"""
    return SavingsAccount(tim)


def test_inheritance(credit10, savings):
    """Check attributes and inheritance of instances"""
    assert isinstance(credit10, Account)
    assert isinstance(savings, Account)


def test_credit_interest(credit10):
    """Interest is only charged on a credit account when the amount is negative"""
    credit10.withdraw(500)
    assert credit10.amount == -500

    credit10.compute_interest()
    # 10% of 500 = $50 + $10 admin fees
    assert credit10.amount == -560

    credit10.deposit(1000)
    credit10.compute_interest()
    # No interest when amount > 0
    assert credit10.amount == 440


def test_savings_withdraw(savings):
    """Check you cannot go below 0 on a savings account"""
    savings.deposit(500)

    with pytest.raises(UserWarning):
        savings.withdraw(1000)

    assert savings.amount == 500
