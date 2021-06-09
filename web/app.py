from flask import Flask, render_template
from flask import jsonify, request
from process import generate_key, generate_data
import requests
import csv
import sys
import os
import argparse
import subprocess
import datetime as dt
import urllib, json
import glob
import configparser

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


@app.route('/process', methods=['POST'])
def download_files():
    collection = request.form.get('collection')
    max_records = request.form.get('max_records')
    processing_level = request.form.get('processing_level')
    sort_by = request.form.get('sort_by')
    sort_order = request.form.get('sort_order')
    status = request.form.get('status')
    dataset = request.form.get('dataset')
    timeliness = request.form.get('timeliness')
    product_type = request.form.get('product_type')
    instrument = request.form.get('instrument')
    start_date = request.form.get('start_date')
    completion_date = request.form.get('completion_date')

    variables = [{
        "collection": collection, 
        "max_records": max_records, 
        "processing_level": processing_level, 
        "sort_by": sort_by, 
        "sort_order": sort_order, 
        "status": status, 
        "dataset": dataset, 
        "timeliness": timeliness, 
        "product_type": product_type, 
        "instrument": instrument, 
        "start_date": start_date, 
        "completion_date": completion_date, 
    }]
    # turn variables into string to send in request
    listString = json.dumps(variables)
    # calls generate key in process.py
    generate_key()
    # calls generate_data in process.py with vairables
    return generate_data(listString)


    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')