class Stuff():
    def __init__(self,name,email,address,city,state,postalcode):
        self.__name=name
        self.__email=email
        self.__address=address
        self.__city=city
        self.__state=state
        self.__zip=postalcode

    def get_name(self):
        return self.__name
    def get_email(self):
        return self.__email
    def get_address(self):
        return self.__address
    def get_city(self):
        return self.__city
    def get_state(self):
        return self.__state
    def get_zip(self):
        return self.__zip


    def set_name(self,name):
        self.__name=name
    def set_email(self,email):
        self.__email=email
    def set_address(self,address):
        self.__address=address
    def set_city(self,city):
        self.__city=city
    def set_state(self,state):
        self.__state=state
    def set_zip(self,zip):
        self.__zip=zip