class Loan:
    count_id = 0

    # Loan init
    def __init__(self, First_name, Last_name, amount, plan):
        Loan.count_id += 1
        self.__LoanId = Loan.count_id
        self.__FirstName = First_name
        self.__LastName = Last_name
        self.__amount = amount
        self.__plan = plan

    # Loan getter method

    def get_loan_id(self):
        return self.__LoanId

    def get_loan_name(self):
        return self.__FirstName + " " + self.__LastName

    def get_loan_first(self):
        return self.__FirstName

    def get_loan_last(self):
        return self.__LastName

    def get_loan_plan(self):
        return self.__plan

    def get_loan_amount(self):
        return self.__amount

    # Loan setter method

    def set_loan_id(self, new_loan_id):
        self.__LoanId = new_loan_id

    def set_loan_name1(self, new_loan_first_name):
        self.__FirstName = new_loan_first_name

    def set_loan_name2(self, new_loan_last_name):
        self.__LastName = new_loan_last_name

    def set_loan_plan(self, plan):
        self.__plan = plan

    def set_loan_amount(self, amount):
        self.__amount = amount
