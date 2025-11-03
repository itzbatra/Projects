from account import Account, CreditAccount, SavingsAccount

class Bank:
    def __init__(self, name):
        self.name = name
        self.accounts = []

    def create_account(self, category, owner, amount=0.0, interest=0.0):
        if category == "account":
            account = Account(owner, amount)
        elif category == "credit":
            account = CreditAccount(owner, amount)
        elif category == "savings":
            account = SavingsAccount(owner)
        else:
            raise ValueError("unknown account type")

        self.accounts.append(account)
        return account

    def find_accounts_by_ssn(self, ssn):
        return [account for account in self.accounts if account.owner.ssn == ssn]

    def find_accounts_by_name(self, name):
        return [account for account in self.accounts if account.owner.name == name]

    @property
    def balance(self):
        return sum(account.amount for account in self.accounts)
