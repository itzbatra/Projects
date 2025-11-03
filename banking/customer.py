class Customer:
    """
    A simple class that represents a customer at the bank.
    """

    def __init__(self, name, ssn):
        if type(name) is not str or len(name) < 2:
            raise AttributeError("Invalid name for the account.")

        if type(ssn) is not str or not ssn.isnumeric():
            raise AttributeError("Invalid SSN for the account.")

        self.name = name
        self.ssn = ssn
