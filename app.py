import socket
import flask_excel as excel
import json
from flask_bootstrap import Bootstrap
from flask import (Flask, render_template, request, redirect, url_for,
    make_response)
from postal_code_distance import PostalCodeDistance
from flask_wtf import Form as FlaskForm
from wtforms.validators import DataRequired
from wtforms import Form, TextAreaField, SubmitField, StringField, SelectField
import os
import csv
import logging

port = int(os.environ.get('PORT', 5000))
API_KEY_FILE_NAME = "apikey.txt"
CSV_MESSAGE = "Export CSV'"
class PostalForm(FlaskForm):
    postal_code_data = TextAreaField("Postal code data")
    submit_button = SubmitField("Submit")


hostname=socket.gethostname()


app = Flask(__name__)
Bootstrap(app)
app.secret_key='I am secret'

def get_api_key():
	if "GAPI_KEY" in os.environ: 
		return os.environ['GAPI_KEY']
	else: 
		api_path = os.path.join(os.getcwd(),API_KEY_FILE_NAME)
		with open(api_path) as key_file:
			api_key = key_file.read().rstrip()
		return api_key

def get_mapit_key():
	if "MAPIT_KEY" in os.environ: 
		return os.environ['MAPIT_KEY']
	else: 
		api_path = os.path.join(os.getcwd(),MAPIT_KEY_FILE_NAME)
		with open(api_path) as key_file:
			api_key = key_file.read().rstrip()
		return api_key


@app.route('/')
def index():
    return render_template('index.html',
        list_of_distances = None, route = "fastest")

@app.route('/save', methods=['POST'])
def save():
    data = dict(request.form.items())
    postal_code_data = (data['postal_code_data'])
    route_choice = data['route choice']
    pc = PostalCodeDistance(postal_code_data, get_api_key(), get_mapit_key())
    postal_code_list = pc.get_postal_codes(postal_code_data)
    logging.warning(postal_code_list)
    list_of_distances = pc.get_list_of_distances(route_choice)
    logging.warning(list_of_distances)
    return render_template('index.html', route=route_choice,
        list_of_distances = list_of_distances,
        postal_code_data = postal_code_data, postal_code_list = postal_code_list)
"""
@app.route('/auth')
def auth():
    drive_helper = google_drive_helper.Google_Drive_Helper(
        google_drive_helper.SCOPES, google_drive_helper.APPLICATION_NAME,
        google_drive_helper.JSON_FILE_NAME)
    url = drive_helper.get_credentials(
        "http://192.168.0.122:8000/" , 'british_miles.json', "https://www.googleapis.com/auth/drive.metadata.readonly")
    return(redirect(url))
@app.route('/sheets')
def sheets():
    print('test')
    return 0
"""
@app.route('/getmiles')
def getmiles():
    postal_code_data = request.query_string.decode("utf-8")
    pc = PostalCodeDistance(postal_code_data, get_api_key())
    postal_code_list = pc.get_postal_codes(postal_code_data)
    
    route_choice = "fastest"
    list_of_distances = pc.get_list_of_distances(route_choice)
    return render_template('index.html', route=route_choice,
        list_of_distances = list_of_distances,
        postal_code_data = postal_code_data, postal_code_list = postal_code_list)


@app.route('/download', methods=['POST'])
def download():
    data = dict(request.form.items())
    postal_code_data = (data['postal_code_data'])
    pc = PostalCodeDistance(postal_code_data, get_api_key())
    postal_code_list = pc.get_postal_codes(postal_code_data)
    list_of_distances = (data['list_of_distances'])
    fixed_list_of_distances = json.loads(list_of_distances) # needed to re-serialize list
    route_choice = data['route_choice']
    csv_data = pc.generate_csv_data(postal_code_list,
        fixed_list_of_distances, route_choice)
    #if data['format'] == CSV_MESSAGE:
    output = excel.make_response_from_array(csv_data, 'csv')
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output
    """else:
        response = make_response(redirect(url_for('auth')))
        response.set_cookie('csv', json.dumps(csv_data))
        return response
"""
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
