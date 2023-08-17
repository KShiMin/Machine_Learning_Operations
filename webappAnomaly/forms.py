from logging import PlaceHolder
from wtforms import Form, StringField, SelectField, TextAreaField, PasswordField, validators, DateField, TimeField, FileField, FieldList, FormField, RadioField, IntegerField, SubmitField
from wtforms.fields import EmailField, DateField
from flask_wtf import FlaskForm

import pandas as pd
import datetime

# from main import og_data

# dataFile = og_data
# # print(dataFile)


nowDate = datetime.datetime.now().year
years = [(year, str(year)) for year in range(nowDate - 4, nowDate + 1)]
months = list(range(1, 13))

# div_names = dataFile['DIV_NAME'].str.replace('_', ' ')
# DIVunique = sorted(div_names.unique())
# DIVchoices = [(value, value) for value in DIVunique]

# categories = dataFile['CAT_DESC'].str.replace('_', ' ')
# CATunique = sorted(categories.unique())
# CATchoices = [(value, value) for value in CATunique]



class signupForm(Form):

    # def __init__(self, og_data=None):
    #     self.og_data = og_data
    #     print(self.og_data.head())
    #     self.setting()

    # def setting(self):
    #     print(self.og_data.head())
    #     global DIVchoices, CATchoices
    #     div_names = self.og_data['DIV_NAME'].str.replace('_', ' ')
    #     DIVunique = sorted(div_names.unique())
    #     DIVchoices = [(value, value) for value in DIVunique]

    #     categories = self.og_data['CAT_DESC'].str.replace('_', ' ')
    #     CATunique = sorted(categories.unique())
    #     CATchoices = [(value, value) for value in CATunique]
    #     self.html_set()
    
    # def html_set(self):
        Fyear = SelectField('Fiscal Year', [validators.DataRequired()], choices=years, default='2023')
        Fmonth = SelectField('Fiscal Month', [validators.DataRequired()], choices=months, default='1')
        DEPname = StringField('Department Name', [validators.Length(min=1, max=150), validators.DataRequired()], render_kw={"placeholder": "E.g. Dept of education"})
        DIVname = StringField('Division Name', [validators.Length(min=1, max=150), validators.DataRequired()], render_kw={"placeholder": "E.g. Special needs programs"})
        # DIVname = SelectField('Division Name', [validators.DataRequired()], choices=DIVchoices)
        MERname = StringField('Merchant Name', [validators.Length(min=1, max=150), validators.DataRequired()], render_kw={"placeholder": "E.g. Amazon.com"})
        transDate = DateField('Transaction Date', [validators.length(max=8), validators.Optional()])
        category = StringField('Category', [validators.Length(min=1, max=150), validators.DataRequired()], render_kw={"placeholder": "E.g. Eating places restaurants"})
        # category = SelectField('Category', [validators.DataRequired()], choices=CATchoices)
        amount = IntegerField('Amount in SGD', [validators.NumberRange(min=1, max=1000000), validators.DataRequired()])

        # email = EmailField('Email', [validators.Email(), validators.DataRequired()])
        # password = PasswordField('Password', [validators.Length(min=8, max=20), validators.DataRequired()])
        # comfirmpw = PasswordField('Confirm Password', [validators.Length(min=8, max=20), validators.DataRequired()])
    

class loginForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', [validators.length(max=100), validators.DataRequired()])


# no html link yet
class changPw(Form):
    nowpassword = PasswordField('Current Password', [validators.Length(min=8, max=20), validators.DataRequired()])
    newpassword = PasswordField('New Password', [validators.length(max=100), validators.DataRequired()])
    comfirmpw = PasswordField('Confirm Password', [validators.Length(min=8, max=20), validators.DataRequired()])

class forgetpw(Form):
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])


class createSeating(Form):
    seat_type = StringField('Seat Type', [validators.Length(min=1, max=150), validators.DataRequired()])
    seat_available = IntegerField('Seat Available', [validators.NumberRange(min=1, max=100000), validators.DataRequired()])
    seat_price = IntegerField('Seat Price', [validators.NumberRange(min=1, max=100000), validators.DataRequired()])
    


class createEvent(Form):
    event_name = StringField('Event Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    event_category = SelectField('Event Category', [validators.DataRequired()], choices=[('', 'Select'), ('S', 'Sport'), ('C', 'Concert')], default='')
    seating_plan = FieldList(FormField(createSeating), min_entries=1)
    event_date = DateField('Event Date',  [validators.DataRequired()], format='%Y-%m-%d')
    event_time = TimeField('Event Time', [validators.DataRequired()], format='%H:%M')
    event_location = StringField('Event Location', [validators.Length(min=1, max=150), validators.DataRequired()])
    event_poster = FileField('Poster Image')
    event_desc = TextAreaField('Description', [validators.DataRequired()])
    seat_image = FileField('Seating Plan')

class addOrder(Form):
    order_price = RadioField('Seat Price', [validators.DataRequired()] , choices=[])
    order_quantity = IntegerField('Ticket', [validators.NumberRange(min=1), validators.DataRequired()], default=1)
    # def order_price_multiply_quantity(self):
    #     return self.order_price * self.order_quantity



class CreateQnForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    subject = SelectField('Subject', [validators.DataRequired()], choices=[('', 'Select'), ('Technical', 'Technical Issue of the Transaction'), ('Ticket', 'Ticket Policy'),('Refund', 'Ticket Refund' ),('Feedback', 'Feedback/Review')], default='')
    email = StringField('Email',[validators.Email(), validators.DataRequired()])
    remarks = TextAreaField('Remarks', [validators.DataRequired()])
    answers = TextAreaField('Answers', [validators.DataRequired()], default='-')
    
  
