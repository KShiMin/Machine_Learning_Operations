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
from hydra import test_utils


# start command ======= python -m gunicorn -w 4 main:app
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



# ----------------------------------------------------------------------------------------------------------------------------------------------------------
# Zowie


# current_path = utils.get_originial_cwd() + "/"

@hydra.main(config_path='../'+ 'config', config_name='main')
def run_configs(config):
    global anomalyModel, cols, csv_data

    dataFilePath = config.data.processed
    csv_data = pd.read_csv(dataFilePath)  # Read CSV file
    cols = csv_data.columns

    modelFile = config.pipeline.pipeline1
    anomalyModel = load_model(modelFile)

@hydra.main(config_path='../'+ 'config/process', config_name='anomalyProcess')
def processing(config):
    global dpath, tpath, fpath

    dpath = config.date_column
    tpath = config.text_column
    fpath = config.float_column



# --- functions

def isweekday(dd):
    weekno = dd.weekday()

    if weekno < 5:
        return 1
    else:  # 5 Sat, 6 Sun
        return 0
    
def new_cols(date):
    daynum = date.strftime('%A'),
    return daynum


# ----------------------------------------------------------------------------------

@app.route('/')
def home():
   return render_template('home.html')


@app.route('/anomalyDetectionInput', methods=['GET', 'POST'])
def create_user():
    from forms import signupForm
    signup = signupForm(request.form)
    if request.method == 'POST':

        run_configs()
        processing()

        inputvalues = list(request.form.values())

        # store new data in shelve to allow for future retraining
        users_dict = {}
        db = shelve.open('storage.db', 'c')

        try:
            users_dict = db['Users']
        except:
            print("Error in retrieving Users from storage.db.")
        
        user = account.Account(inputvalues)
        users_dict[user.get_id()] = user
        db['Users'] = users_dict

        db.close()

        
#       put data together
        print('new data')  
        userNewData = {}

        for index, name in enumerate(cols[0:-2]):
            userNewData[name] = inputvalues[index]

        user_df = pd.DataFrame([userNewData])
        user_df['DayOfWeek'] = 0
        user_df['isWeekday'] = 0

        # pre process data
        for dd in dpath:
            dat = user_df[dd].values[0]
            datobject = pd.to_datetime(dat)
            user_df[dd] = datobject
            user_df['DayOfWeek'] = new_cols(datobject)
            user_df['isWeekday'] = isweekday(datobject)

        for strings in tpath:
            user_df[strings] = user_df[strings].str.upper()
        
        for flt in fpath:
            user_df[flt] = user_df[flt].astype(float)
        

        print(user_df.columns)

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


    