from arima import *
import json
import pandas as pd
from woxiaxiede_agg import *
from woxiaxiede_avg import *
from Prophet import *

def query(tags,index,db):
	# words = tags.split(' ')
	# index_pool = dict(index)
	# new_pool = {}
	# query_index =[]
	# for word in words:
	# 	for qs in index_pool:
	# 		if word in qs:
	# 			new_pool[qs] = index_pool[qs]
	# 	index_pool = dict(new_pool) 
	# 	new_pool = {}
	# return search(index_pool,db)
	words = tags.split(' ')
	index_pool = {}
	# print(words)
	k = 0
	for key_string in index:
		temp = key_string.split('.')
		if all(word in temp for word in words):
			index_pool[key_string] = index[key_string]
	return search(index_pool,db)

def search(i,db):
	answers = {}
	for k,v in i.items():
		r = db.get(v)
		if r:
			answers[k] = r 
	return answers

def get_from_database(name,db,index):
	i = index[name]
	value = json.loads(db.get(i))
	return value


def transform(algorithm,data,data_type,time,weight):
	if data_type =='aggregate':
		return aggregate(algorithm,data,time,weight)
	if data_type == 'average':
		return average(algorithm,data,time)


def aggregate(algorithm,data,time,weight):
	# if algorithm == "woxiaxiede_agg":
	agg_model = woxiaxiede_agg()
	agg_model.fit(data)
	result = agg_model.apply(time,weight)
	return result

def average(algorithm,data,time):
	alg_name = algorithm.lower()	
	# if algorithm == 'woxiaxiede_avg':
	avg_model = woxiaxiede_avg()
	avg_model.fit(data)
	result = avg_model.apply(time)
	return result

def predict(algorithm,params,data,time):
	alg_name = algorithm.lower()
	if alg_name == 'arima':
		arima_model = arima(params)
		arima_model.fit(data)
		result = arima_model.predict(time)
		return result
	if alg_name == 'Prophet':
		prophet_model = Prophet(params)
		prophet_model.fit(data)
		result = prophet_model.predict(time)
		return result

def apply(algorithm,params,data,operator,data_type,time = '5',weight = []):
	if operator == 'p':
		return predict(algorithm,params,data,time)
	if operator == 't':
		return transform(algorithm,data,data_type,time,weight)
	return False
