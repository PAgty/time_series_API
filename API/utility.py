import json
import pandas as pd


def is_valid(train):
	if not train:
		return False
	else:
		for n,k in train.items(): 
			try:
				float(k)
			except:
				return False
	return True

def get_freqlist(freq):
	selection_list = ['H','D','W','M','Q','Y']
	name_list = ['Hour','Day','Week','Month','Quarter','Year']
	for ind,val in enumerate(selection_list):
		if val in freq:
			return name_list[1:ind]

def infer_freq(data):
	'''
	just a test version, need further improve,ex,business day consideration, quarter start or end, holodays, etc.. 
	'''

	def find(v,d):
		l = list(d.keys())
		start = 0
		end = len(l) - 1
		while start < end - 1:
			mid = int((start + end)/2)
			if l[mid] == v:
				return l[mid]
			if l[mid] > v:
				end = mid
			if l[mid] < v:
				start = mid
		if abs(v - l[start]) > abs(v - l[end]):
			return l[end]
		else:
			return l[start]

	def get_index(data):
		df = pd.Series(data)
		df.index = pd.to_datetime(df.index,format = '%Y-%m-%d')
		df = pd.to_numeric(df, errors='coerce')
		df = df.astype(float)
		return df.index


	index = get_index(data)

	freq = pd.infer_freq(index)
	# print(freq)
	if freq == None:
		diff_day = []
		diff_second = []
		sec_base ={1:'S',60:'min',3600:'H',86400:'D'}
		day_base ={1:'D',7:'W',30:'M',90:'QS',365:'Y'}
		for ind,val in enumerate(index):
			if ind > 0:
				diff_day.append((index[ind] - index[ind - 1]).days)
				diff_second.append((index[ind] - index[ind - 1]).seconds)
		mode_day = max(set(diff_day), key=diff_day.count)
		mode_second = max(set(diff_second), key=diff_second.count)
		if mode_day < 1:
			return sec_base[find(mode_second,sec_base)]
		else:
			return day_base[find(mode_day,day_base)]
	else:
		return freq



def standardrized_freq(freq):
		
		pass






















		