import uuid

class Account:

    # def __init__(self, fyear, fmonth, DEPname, DIVname, merchant, category, trans_dt, amt):
    def __init__(self,list):

        self.__data_id = str(uuid.uuid4())
        self.__fyear = list[0]
        self.__fmonth = list[1]
        self.__DEPname = list[2]
        self.__DIVname = list[3]
        self.__merchant = list[4]
        self.__category = list[5]
        self.__trans_dt = list[6]
        self.__amt = list[7]


    def get_id(self):
        return self.__data_id
    def set_id(self, data_id):
        self.__data_id = data_id
    
    def get_fyear(self):
        return self.__fyear
    def set_fyear(self, fyear):
        self.__fyear = fyear

    def get_fmonth(self):
        return self.__fmonth
    def set_fmonth(self, fmonth):
        self.__fmonth = fmonth

    def get_DEPname(self):
        return self.__DEPname
    def set_DEPname(self, DEPname):
        self.__DEPname = DEPname

    def get_DIVname(self):
        return self.__DIVname
    def set_DIVname(self, DIVname):
        self.__DIVname = DIVname


    def get_merchant(self):
        return self.__merchant
    def set_get_merchant(self, merchant):
        self.__merchant = merchant

    def get_category(self):
        return self.__category
    def set_get_category(self, category):
        self.__category = category

    def get_trans_dt(self):
        return self.__trans_dt
    def set_get_trans_dt(self, trans_dt):
        self.__trans_dt = trans_dt

    def get_amt(self):
        return self.__amt
    def set_get_amt(self, amt):
        self.__amt = amt


