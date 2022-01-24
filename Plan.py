class Plan:
    count_id = 0

    # Loan init
    def __init__(self, Plan_name, Plan_description, Plan_interest, image):
        Plan.count_id += 1
        self.__PlanId = Plan.count_id
        self.__Plan_name = Plan_name
        self.__Plan_description = Plan_description
        self.__Plan_interest = Plan_interest
        self.__Plan_image = image

    # Loan getter method

    def get_loan_plan_id(self):
        return self.__PlanId

    def get_loan_plan_name(self):
        return self.__Plan_name

    def get_loan_plan_desc(self):
        return self.__Plan_description

    def get_loan_plan_int(self):
        return self.__Plan_interest

    def get_loan_plan_image(self):
        return self.__Plan_image


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

    def set_loan_email(self, email):
        self.__email = email
