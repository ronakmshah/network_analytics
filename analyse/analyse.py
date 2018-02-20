import copy
import pandas as pd
import numpy as np
import xgboost
import elasticsearch
from sklearn.preprocessing import LabelEncoder


def process_es_search(flows):
	#Process the ES flows returned. This is only a prototype & specific function. The general version would be written after finalising the indexes and columns
    return [[x['_source']['nuage_metadata']['service'],
                                                    x['_source']['nuage_metadata']['sourcevport'],
                                                    x['_source']['nuage_metadata']['acl_source_name']] for x in flows]
   
class Analyse():
	def __init__(self,handle):
		if handle.type!='elasticsearch':
			return
		self.es = handle.handle

	def data_read(self):
		#Create a list for data
		data = []
		page = self.es.search(index='nuage_flow_test',
		                 doc_type='nuage_doc_type',
		                 body={"query": {"match_all": {}}},
		                scroll = '2m',
		                size = 10000)

		#print(page['hits']['hits'][0])
		data += process_es_search(page['hits']['hits'])
		sid = page['_scroll_id']
		scroll_size = len(page['hits']['hits'])
		while scroll_size>0:
		    page = self.es.scroll(scroll_id = sid, scroll = '2m')
		    data += process_es_search(page['hits']['hits'])
		    sid = page['_scroll_id']
		    scroll_size = len(page['hits']['hits'])
		cols = ['service','sourcevport','acl_source_name']
		df = pd.DataFrame(data,columns=cols)
		return df

	def create_model_and_validate(self,df):
		#Labelling string data to class-ed data
		le = LabelEncoder()
		le.fit(df['service'])
		df['service'] = le.transform(df['service'])

		le2 = LabelEncoder()
		le2.fit(df['sourcevport'])
		df['sourcevport'] = le2.transform(df['sourcevport'])

		le3 = LabelEncoder()
		le3.fit(df['acl_source_name'])
		df['acl_source_name'] = le3.transform(df['acl_source_name'])

		X = df[['service','sourcevport']] #Predictor variable
		Y = df['acl_source_name'] #Response variable

		#Create random samples of validation and training data
		np.random.seed(123)
		#msk is a mask for numpy array i.e. list of booleans equalivalent to size of df
		msk = np.random.randn(len(df))<0.75
		trainX,testX = X[msk],X[~msk]
		trainY,testY = Y[msk],Y[~msk]

		#XGB model - straightforward implementation out of the box, no changes
		xgb = xgboost.XGBClassifier(gamma = 0.1)
		self.model = xgb.fit(trainX,trainY)
		predictedY = model.predict(testX)
		from sklearn.metrics import recall_score,precision_score
		recall = recall_score(testY,predictedY,average='micro')
		precision = precision_score(testY,predictedY,average='micro')
		return (recall,precision)

	def predict_acl_source_name(self,service,sourcevport):
		return self.model.predict(pd.DataFrame([[service,sourcevport]])).tolist()[0]



		
