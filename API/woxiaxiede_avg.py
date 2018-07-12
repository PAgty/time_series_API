from transform import transform
import pandas as pd
from utility import infer_freq
import numpy as np

class woxiaxiede_avg(transform):
	diff = {}
	df = {}
	converted_df = {}
	def __init__(self):
		pass

	def fit(self,data):
		self.time = data.keys()
		self.df = pd.Series(data)
		self.df.index = pd.to_datetime(self.df.index,format = '%Y-%m-%d')
		self.df = pd.to_numeric(self.df, errors='coerce')
		self.df = self.df.astype(float)
		self.data_freq = infer_freq(self.df)
		self.weight = self.compute_weight(self.df.index)
		self.df.index.freq = self.data_freq
		
	def apply(self,time):	
		# print(time)
		# print(self.df)
		upsampled = self.df.resample('1D')
		self.converted_df = upsampled.interpolate(method='linear')
		self.adjusted_df = self.adjust(self.converted_df,self.df)	
		# print(self.converted_df)	
		if time == 'Month':
			return self.adjusted_df.resample('1M').agg(np.sum)
		if time == 'Week':
			return self.adjusted_df.resample('W').agg(np.sum)
		if time == 'Quarter':
			return self.adjusted_df.resample('3M').agg(np.sum)
		if time == 'Day':
			return self.adjusted_df

	def adjust(self,df,old_df):
		index = 0
		old_index = 0
		# print(df)
		for i in self.weight:
			stride = i/2
			if i % 2 == 0:
				adj_1 = df.iloc[int(index + stride)] - old_df.iloc[int(old_index)]
				adj_2 = df.iloc[int(index + stride - 1)] - old_df.iloc[int(old_index)]
				adj = (adj_1 + adj_2)/2
			else:
				adj = df.iloc[int(index + stride)] - old_df.iloc[int(old_index)]
			df.iloc[int(index):int(index + i)] = df.iloc[int(index):int(index + i)] - adj
			index = index + i
			old_index = old_index + 1
		return df
	def compute_weight(self,index):
		diff =[]
		self.df = self.append_index(self.df)
		index_length = len(self.df.index)
		# print(self.df.index)
		for i in range(1,index_length):
			value = (self.df.index[i] - self.df.index[i - 1]).total_seconds()
			diff.append(value/86400)
			# else:
			# 	if final_freq == 'M':
			# 		diff.append(self.diff_month(self.df.index[i],self.df.index[i - 1]))
		return diff
	def append_index(self,df):
	# index_length = len(df)
		if df.index.freq:
				df[df.index[-1] + 1] = np.nan
				# print(self.df)
				# print(time_stamp.date())
				# self.df.set_value(pd.DatetimeIndex([time_stamp.date()]),np.nan)
				# index.append(pd.DatetimeIndex([time_stamp.date()]))

		return df
# # data = {"2004-09-01": "14089", "2005-09-01": "5758", "2006-03-01": "3382", "2006-06-01": "3186", "2006-09-01": "3271", "2007-01-01": "5300", "2007-03-01": "20518", "2007-06-01": "18373", "2007-09-01": "53265", "2008-01-01": "91193", "2008-03-01": "223883", "2008-06-01": "197119", "2008-09-01": "237820", "2009-01-01": "208096", "2009-03-01": "100704", "2009-06-01": "92290", "2009-09-01": "60550", "2010-01-01": "44254", "2010-03-01": "110052", "2010-06-01": "157617", "2010-09-01": "117208", "2011-01-01": "92753", "2011-03-01": "64638", "2011-06-01": "154511", "2011-09-01": "151503", "2012-01-01": "136955", "2012-03-01": "176194", "2012-06-01": "196928", "2012-09-01": "194400", "2013-01-01": "240000", "2013-03-01": "296500", "2013-06-01": "306500", "2013-09-01": "385300", "2014-01-01": "402300", "2014-03-01": "309200", "2014-06-01": "387100", "2014-09-01": "330300", "2015-01-01": "438700", "2015-03-01": "415600", "2015-06-01": "541800", "2015-09-01": "731900", "2016-01-01": "1074900", "2016-03-01": "1010500", "2016-06-01": "1649000", "2016-09-01": "1309100", "2017-01-01": "810600", "2017-03-01": "986800", "2017-06-01": "2362600", "2017-09-01": "3003400", "2018-01-01": "5212800"}
# model = woxiaxiede_avg()
# model.fit(data)
# conv_model = model.predict('D')
# print(conv_model.resample('1M').sum())
# s = 0
# for i in range(1,31):
# 	s = s + conv_model['2004-09-%.2d'%i]
# # print(s)
# time = 'D'
# conv = model.predict(time)
# print(conv)