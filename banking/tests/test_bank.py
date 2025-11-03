import pytest

from account import Account, CreditAccount, SavingsAccount
from bank import Bank
from customer import Customer


@pytest.fixture
def tim():
    """Tim is a regular customer"""
    return Customer("Tim", "84093232")


@pytest.fixture
def mybank():
    """Your typical bank"""
    return Bank("My bank")


def test_bank(mybank):
    """Check attributes"""
    assert mybank.name == "My bank"


def test_create_account(mybank, tim):
    """Check the different accounts that can be created"""
    acc = mybank.create_account("account", tim)
    assert isinstance(acc, Account)
    assert acc.owner.name == "Tim"

    credit = mybank.create_account("credit", tim, 10)
    assert isinstance(credit, CreditAccount)
    assert credit.interest == 10
    assert credit.owner.name == "Tim"

    savings = mybank.create_account("savings", tim)
    assert isinstance(savings, SavingsAccount)
    assert savings.owner.name == "Tim"


def test_bank_balance(mybank, tim):
    assert isinstance(Bank.balance, property)

    tim_acc = mybank.create_account("account", tim)
    tim_acc2 = mybank.create_account("credit", tim, 10)

    tim_acc.deposit(1000)
    assert mybank.balance == 1000

    tim_acc2.withdraw(2000)
    assert mybank.balance == -1000


def test_find_accounts_by_ssn(mybank, tim):
    """Check that the correct accounts are returned"""
    alice = Customer("Alice", "218309321")
    alice_acc = mybank.create_account("account", alice)
    alice_credit10 = mybank.create_account("credit", alice, 10)
    alice_savings = mybank.create_account("savings", alice)

    tim_savings = mybank.create_account("savings", tim)

    alice_accounts = mybank.find_accounts_by_ssn("218309321")
    assert len(alice_accounts) == 3
    assert alice_acc in alice_accounts
    assert alice_credit10 in alice_accounts
    assert alice_savings in alice_accounts

    tim_accounts = mybank.find_accounts_by_ssn("84093232")
    assert len(tim_accounts) == 1
    assert tim_accounts[0] == tim_savings


def test_find_accounts_by_name(mybank, tim):
    """The bank can have two customers with the same name"""
    tim2 = Customer("Tim", "540954354")
    tim_acc = mybank.create_account("account", tim)
    tim2_acc = mybank.create_account("account", tim2)

    accounts = mybank.find_accounts_by_name("Tim")
    assert tim_acc in accounts
    assert tim2_acc in accounts
