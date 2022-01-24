#class Stuff():
 #   def __init__(self,name,email,address,city,state,postalcode):
  #      self.__name=name
   #    self.__address=address
    #    self.__city=city
     #   self.__state=state
      #  self.__zip=postalcode

    #def get_name(self):
    #    return self.__name
    #def get_email(self):
     #   return self.__email
    #def get_address(self):
     #   return self.__address
    #def get_city(self):
     #   return self.__city
    #def get_state(self):
     #   return self.__state
    #def get_zip(self):
     #   return self.__zip


    #def set_name(self,name):
     #   self.__name=name
    #def set_email(self,email):
     #   self.__email=email
    #def set_address(self,address):
     #   self.__address=address
    #def set_city(self,city):
     #   self.__city=city
    #def set_state(self,state):
     #   self.__state=state
    #def set_zip(self,zip):
     #   self.__zip=zip

class Loan2:
    count_id = 0

    # Loan init
    def __init__(self, First_name, Last_name, amount, plan, email):
        Loan2.count_id += 1
        self.__LoanId = Loan2.count_id
        self.__FirstName = First_name
        self.__LastName = Last_name
        self.__amount = amount
        self.__plan = plan
        self.__email = email

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

    def get_loan_email(self):
        return self.__email

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
