import uuid

class Account:

    def __init__(self, fyear, fmonth, DEPname, DIVname, merchant, category, trans_dt, amt):

        self.__data_id = str(uuid.uuid4())
        self.__fyear = fyear
        self.__fmonth = fmonth
        self.__DEPname = DEPname
        self.__DIVname = DIVname
        self.__merchant = merchant
        self.__category = category
        self.__trans_dt = trans_dt
        self.__amt = amt


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


