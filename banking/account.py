import uuid
from customer import Customer

class Account:
    def __init__(self, owner: Customer, amount: float = 0.0):
        if not isinstance(owner, Customer):
            raise TypeError("owner must be a customer instance")
        self.owner = owner
        self.amount = float(amount)
        self.id = str(uuid.uuid4())

    def deposit(self, value: float):
        if value < 0:
            raise AttributeError("Negative amount cannot be deposited")
        self.amount += value

    def withdraw(self, value:float):
        if value < 0:
            raise AttributeError("withdrawable amount cannot be negative")
        self.amount -= value

    def transfer(self, account, value:float):
        if not isinstance(account, Account):
            raise TypeError("target must be an Account")
        self.withdraw(value)
        account.deposit(value)


class CreditAccount(Account):
    def __init__(self, owner, interest):
        super().__init__(owner)
        self.interest = interest

    def compute_interest(self):
        if self.amount < 0:
            self.amount *= (100 + self.interest) / 100
            self.amount -= 10


class SavingsAccount(Account):
    def __init__(self, owner):
        super().__init__(owner)
        self._amount = 0.0 

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        if value < 0:
            raise UserWarning("Savings account cannot have negative balance")
        self._amount = value

