import os

from flask import Flask
import json
import redis
import pickle
from algorithms import * 
from utility import *
from api import *
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

# current provided algorithm,temporarily hard coded 

algs = ['ARIMA','PROPHET']
alg_param = {'ARIMA':['P','I','Q'],'PROPHET':[]}

# global Variable
QUERY_NAME_TIME_SERIES = {}
SELECTED_TIME_SERIES = ""

SELECTED_ALGS = ""


app = Flask(__name__)

db = redis.StrictRedis(host='localhost', port=6379, db=0,decode_responses=True)
index = json.loads(db.get('indexing'))

@app.route('/')
def main_page():
	global QUERY_NAME_TIME_SERIES
	global SELECTED_ALGS	
	global SELECTED_TIME_SERIES	
	if request.args:
		if request.args.get('algorithms'):
			SELECTED_ALGS = request.args['algorithms']
			SELECTED_TIME_SERIES = request.args.get('tags')
			# print(SELECTED_TIME_SERIES)
			return render_template('main_page.html',values = SELECTED_TIME_SERIES,selected_algs = SELECTED_ALGS, algs = algs,params = alg_param[SELECTED_ALGS])
		else:
			tags = request.args['search_tags']
			QUERY_NAME_TIME_SERIES = query(tags,index,db)
			if(QUERY_NAME_TIME_SERIES):
				return render_template('main_page.html',values = QUERY_NAME_TIME_SERIES,algs = algs)
			else:
				return render_template('main_page.html',values = False)
	return render_template('main_page.html')

@app.route('/result',methods=['GET'])
def result():
	global SELECTED_ALGS
	global SELECTED_TIME_SERIES
	data = get_from_database(SELECTED_TIME_SERIES,db,index)
	operator = request.args['operator']
	data_type = request.args['data_type']
	request_time = request.args['frequency']
# def apply(algorithm,params,data,operator,data_type,time,weight):
	if is_valid(data):
		predicted_data = apply(algorithm = SELECTED_ALGS,params = request.args,data = data,operator =operator,data_type = data_type,time = request_time)
		return render_template('result.html',values = predicted_data)
	else:
		return render_template('result.html',values = {'no/invalid data':'no/invaid data'})

@app.route('/data',methods =['POST'])
def get_data():
	showed_data_name = request.form.get('data_name')
	print(showed_data_name)
	if showed_data_name:
		data_value = get_from_database(showed_data_name,db,index)
		return render_template('data.html',values = data_value)

@app.route('/transform', methods = ['POST'])
def get_transform():
	global SELECTED_TIME_SERIES
	data_type = ['aggregate','average']
	showed_data_name = request.form.get('data_name')
	SELECTED_TIME_SERIES = showed_data_name 

	# print(SELECTED_TIME_SERIES)
	if showed_data_name:
		data_value = get_from_database(showed_data_name,db,index)
		# get frequent
		freq= infer_freq(data_value)
		freq_list = get_freqlist(freq)
		return render_template('transform.html',values = freq_list,type = data_type)

@app.route('/test', methods = ['POST'])
def testing():
	return 5


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
