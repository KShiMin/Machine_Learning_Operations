import os
from flask import Flask, redirect, url_for, render_template, request, session, flash
# from forms import createEvent, signupForm, loginForm, forgetpw, changPw,  addOrder, CreateQnForm
import shelve, account
import pandas as pd
import numpy as np


from pycaret.anomaly import *

# session timeout
import flask
# import flask_login
import datetime

# from werkzeug.utils import secure_filename
# # from flask_login import LoginManager
# from werkzeug.datastructures import CombinedMultiDict
import smtplib
from email.message import EmailMessage


import hydra
from hydra import utils

# csv_data=None

# admin name: admin
# admin email: admin@gmail.com
# admin pw: eventnest

# Paypal
# https://developer.paypal.com/developer/accounts
# Account: eventnest1@gmail.com
# Password: eventnest1*
# The above account if used to create the testing payment account => Adjust Funding Here

# https://www.sandbox.paypal.com/us/home
# user payment account
# payment account: eventnestbuyer1@personal.example.com
# payment password: p!:stYK7

# business account that receive payment
# business email: eventnestbusiness1@business.example.com
# business password: p-E"OA8s
# Check for payment paid/received from the link above

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sweet like candy'
app.config['UPLOAD_FOLDER'] = 'static/images'

@app.before_request
def before_request():
    flask.session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=30)
    flask.session.modified = True
    # flask.g.user = flask_login.current_user


@app.before_request
def before_request():
    flask.session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=30)
    flask.session.modified = True
#     flask.g.user = flask_login.current_user


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html'), 404

# current_path = utils.get_originial_cwd() + "/"

@hydra.main(config_path='../'+ 'config', config_name='main')
def run_configs(config):
    global anomalyModel, cols, csv_data

    dataFilePath = '../' + config.data.processed
    csv_data = pd.read_csv(dataFilePath)  # Read CSV file
    cols = csv_data.columns

    modelFile = '../' + config.pipeline.pipeline1
    anomalyModel = load_model(modelFile)



# --- functions

def isweekday(dd):
    weekno = dd.weekday()

    if weekno < 5:
        return 1
    else:  # 5 Sat, 6 Sun
        return 0



# ----------------------------------------------------------------------------------------------------------------------------------------------------------
# Zowie

@app.route('/anomalyDetectionInput', methods=['GET', 'POST'])
def create_user():
    from forms import signupForm
    signup = signupForm(request.form)
    if request.method == 'POST':

        # store new data in shelve to allow for future retraining
        users_dict = {}
        db = shelve.open('storage.db', 'c')

        try:
            users_dict = db['Users']
        except:
            print("Error in retrieving Users from storage.db.")
        

        user = account.Account(signup.Fyear.data, signup.Fmonth.data, signup.DEPname.data.upper(), 
                                signup.DIVname.data.upper(), signup.MERname.data.upper(), signup.category.data.upper(), 
                                signup.transDate.data, signup.amount.data)
        users_dict[user.get_id()] = user
        db['Users'] = users_dict

        db.close()

        print('new data')
        # pre process data
        # convert date to datetime64 object
        transDate = pd.to_datetime(signup.transDate.data)

        # Create a dictionary with original column names
        userNewData = [{
            'FISCAL_YR': int(signup.Fyear.data),
            'FISCAL_MTH': int(signup.Fmonth.data),
            'DEPT_NAME': signup.DEPname.data.upper(),
            'DIV_NAME': signup.DIVname.data.upper(),
            'MERCHANT': signup.MERname.data.upper(),
            'CAT_DESC': signup.category.data,
            'TRANS_DT' : transDate,
            'AMT': float(signup.amount.data),
            'DayOfWeek': transDate.strftime('%A'),
            'isWeekday': isweekday(transDate)
        }]

        user_df = pd.DataFrame(userNewData)

        # Test codes
        # users_dict = db['Users']
        # user = users_dict[user.get_id()]
        # print(user.get_name(), "was stored in storage.db successfully with user_id ==", user.get_user_id())
        

        # perform perdiction
        prediction = predict_model(anomalyModel, data=user_df)
        print(prediction.Anomaly)
        print(prediction.Anomaly_Score)

        pred = prediction.Anomaly[0]
        session['predLabel'] = int(pred)
        print('resultofanomaly : ',pred)
        # label = int(prediction.Label[0])
        return redirect(url_for('anomalyResults'))


    return render_template('corporateInput/signup.html', form=signup)

    
@app.route('/anomalyResults')
def anomalyResults():
   print('results page')
   predLabel = session.get('predLabel')
   if predLabel == 0:
       newLabel='Not an anomaly'
   else:
       newLabel='Anomaly!'
   return render_template('corporateInput/results.html', predLabel=newLabel)



# -----------------------------------------------------------


if __name__ == '__main__':
    run_configs()
    
    app.run(debug=True)


    