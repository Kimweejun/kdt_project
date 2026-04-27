class Sangpum:
    def __init__(self):
        self._code = None
        self._irum = None
        self._su = 0
        self._price = 0
        self._kumack = 0
        
    def get_code(self):
        return self._code

    def set_code(self, code):
        self._code = code
    
    code = property(get_code, set_code)
    
    def get_irum(self):
        return self._irum
    
    def set_irum(self, irum):
        self._irum = irum
    
    irum = property(get_irum, set_irum)
    
    def get_su(self):
        return self._su
    
    def set_su(self, su):
        self._su = su
    
    su = property(get_su, set_su)
    
    def get_price(self):
        return self._price
    
    def set_price(self, price):
        self._price = price
    
    price = property(get_price, set_price)
    
    def get_kumack(self):
        return self._kumack
    
    def set_kumack(self, kumack):
        self._kumack = kumack
    
    kumack = property(get_kumack, set_kumack)

    def number_data(self):

        while True:
            try:
                self._su = int(input("수량 입력 : "))
            except Exception as e:
                print("\n숫자 입력!!!", e.args[0], "\n")
            else:
                break
        while True:
            try:
                self._price = int(input("단가 입력 : "))
            except Exception as e:
                print("\n숫자 입력!!!", e.args[0], "\n")
            else:
                break

    def input_data(self):
        self._code = input("상품코드 입력 : ")
        self._irum = input("상품명 입력 : ")
        self.number_data()

    def proc_kumack(self):
        self._kumack = self._su * self._price