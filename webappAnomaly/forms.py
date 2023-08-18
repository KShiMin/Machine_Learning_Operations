from logging import PlaceHolder
from wtforms import Form, StringField, SelectField, TextAreaField, PasswordField, validators, DateField, TimeField, FileField, FieldList, FormField, RadioField, IntegerField, SubmitField
from wtforms.fields import DateField
from flask_wtf import FlaskForm

import pandas as pd
import datetime



nowDate = datetime.datetime.now().year
years = [(year, str(year)) for year in range(nowDate - 4, nowDate + 1)]
months = list(range(1, 13))



# anomaly detection form
class signupForm(Form):
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

        
# hdb pricce prediction form