import os
from flask import Flask, redirect, url_for, render_template, request, session, flash
# from forms import createEvent, signupForm, loginForm, forgetpw, changPw,  addOrder, CreateQnForm
from py_scripts import account
from py_scripts.hdbForm import HDB 
import shelve
import pandas as pd
import numpy as np



from pycaret.anomaly import *
from pycaret.regression import *

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

@hydra.main(config_path='config', config_name='main')
def run_configs(config):

    print('configfile found')

    global anomalyModel, cols, csv_data, hdbModel, towns, storey_ranges, flat_models

    # Zowie
    dataFilePath = '../' + config.data.processed
    csv_data = pd.read_csv(dataFilePath)  # Read CSV file
    cols = csv_data.columns

    modelFile = '../' + config.pipeline.pipeline1
    anomalyModel = load_model(modelFile)

    # HDB dynamic form select options preparations
    hdb_dataFile = '../' + config.data.raw
    hdb = pd.read_csv(hdb_dataFile)
    towns = sorted(hdb['town'].unique())
    storey_ranges = sorted(hdb['storey_range'].unique())
    flat_models = sorted(hdb['flat_model'].unique())

    # HDB Model loading
    hdb_modelFile = '../' + config.pipeline.pipeline2
    hdbModel = load_model(hdb_modelFile)


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
   print('homepage')
   run_configs()
   return render_template('home.html')


@app.route('/anomalyDetectionInput', methods=['GET', 'POST'])
def create_user():
    from py_scripts.forms import signupForm
    signup = signupForm(request.form)
    if request.method == 'POST':

        
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


# -----------------------------------------------------------
# Shi Min's Routes and Functions
def toUpper(data):
    """Function to convert form data to uppercase for model prediction"""
    return data.upper()

@app.route('/hdb_predict', methods=['GET', 'POST'])
def hdb_predict():
    
    
    # initalize form fields
    hdbPred = HDB(request.form)
    # set form fields option based on historical data
    hdbPred.town.choices = [(town, town) for town in towns]
    hdbPred.storey_range.choices = [(sr, sr) for sr in storey_ranges]
    hdbPred.flat_model.choices = [(fm, fm) for fm in flat_models]

    if request.method == "POST" and hdbPred.validate():

        # Get Datas and do necessary datatype transformations
        results = {
            'block': [toUpper(hdbPred.block.data)],
            'street_name': [toUpper(hdbPred.street_name.data)],
            'town': [hdbPred.town.data],
            'postal_code': [int(hdbPred.postal_code.data)],
            'month': [hdbPred.month.data],
            'storey_range': [hdbPred.storey_range.data],
            'floor_area_sqm': [hdbPred.floor_area_sqm.data],
            'flat_model': [hdbPred.flat_model.data],
            'lease_commence_date': [int(hdbPred.lease_commence_date.data)],
            'cbd_dist': [hdbPred.cbd_dist.data],
            'min_dist_mrt': [hdbPred.min_dist_mrt.data]
        }

        # Convert user inputs into a dataframe
        hdb_unseen = pd.DataFrame(results, columns = results.keys())
        prediction = predict_model(hdbModel, data=hdb_unseen)
        prediction = "{:.2f}".format(float(prediction.prediction_label))

        # provide prediction value back to html file and set check = true to display popup container
        return render_template('hdbPrediction/hdb_main.html', pred=prediction, form=hdbPred, check="true")
    
    return render_template('hdbPrediction/hdb_main.html', form=hdbPred)

# ------------------------------------------------------------


if __name__ == '__main__':
    run_configs()
    
    app.run(debug=True, port=8080)


    