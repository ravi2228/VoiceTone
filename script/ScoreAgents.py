#!/usr/bin/env python
# coding: utf-8

# In[15]:


import glob
import pandas as pd
import numpy as np
import pickle
# import re
# from scipy.stats import spearmanr
pd.options.mode.chained_assignment = None 


# In[16]:

def ScoreAgents(xml):

	xmlDF = xml
	dt = xmlDF['date'][0]

	allDF = pd.read_csv('./output/praatResults.csv', sep="\t", na_values=['--undefined--'])


	# In[17]:


	allDF_cumNA = allDF.dropna()
	allDF_cumNA = allDF_cumNA[allDF_cumNA['unvoiced']<=0.90]
	allDF_cumNA = allDF_cumNA[allDF_cumNA['intensity']>=40]
	allDF_cumNA = allDF_cumNA[allDF_cumNA['HNR']>=9]
	final_df = allDF_cumNA

	# Remove calls <= 10 seconds duration
	dur = final_df.groupby(['group']).agg({'duration':sum})
	dur = dur.reset_index()
	final_df = final_df[~(final_df['group'].isin(list(dur[dur['duration'] <=10]['group'])))]

	if final_df.empty:
		xmlDF['agent_name'] = xmlDF['fname'] + " " + xmlDF['lname']
		test_profile_emotion = xmlDF[['agent_name', 'name', 'transid']]
		test_profile_emotion['isEnthusiastic'] = 'Yes'
		test_profile_emotion['isDefault'] = 'Yes'
	else:

		X_finalDF = np.array(final_df.values[:,3:], dtype = 'double')

		# Load the same scaler used for training data
		filename2 = './modelFiles/scaler.sav'
		loaded_scaler = pickle.load(open(filename2, 'rb'))

		# Scale the agents data using same scaler
		X_finalDF_scaled = loaded_scaler.transform(X_finalDF)


		# Load the model file
		filename = './modelFiles/finalized_model.sav'
		model = pickle.load(open(filename, 'rb'))

		svm_predictions_proba = model.predict_proba(X_finalDF_scaled)

		probs = pd.DataFrame(svm_predictions_proba)
		probs.columns = ['enthusiastic', 'not enthusiastic']

		calls = final_df.copy()
		calls.reset_index(inplace=True)

		# Get probabilties of happiness for each snippet
		calls_emotion = pd.merge(calls, probs, left_index=True, right_index=True)

		calls_emotion_sub = calls_emotion[['group', 'enthusiastic', 'not enthusiastic']]
		calls_emotion_sub.columns = ['name', 'enthusiastic', 'not enthusiastic']

		calls_emotion_xml = xmlDF.merge(calls_emotion_sub, on = 'name')



		# In[19]:


		agent_profile = pd.read_csv('./modelFiles/agent_profileRaw.csv')
		del agent_profile['Unnamed: 0']


		# In[22]:


		calls_emotion_xml['agent_name'] = calls_emotion_xml['fname'] + " " + calls_emotion_xml['lname']
		agent_profileTest = calls_emotion_xml[['agent_name','transid', 'enthusiastic']]
		agent_profile = pd.concat([agent_profile, agent_profileTest], ignore_index = True)
		agent_profile.to_csv('./modelFiles/agent_profileRaw.csv')
		agent_profile = agent_profile.groupby(['agent_name']).agg({'enthusiastic':np.median, 'transid':lambda x: x.nunique()}).reset_index()
		agent_profile = agent_profile[agent_profile['transid'] >= 100]
		agent_profile.columns = ['agent_name', 'mean_enthusiastic', 'numCalls']


		test = calls_emotion_xml
		test_profile = test.merge(agent_profile, on = 'agent_name')
		if test_profile.empty:
			xmlDF['agent_name'] = xmlDF['fname'] + " " + xmlDF['lname']
			test_profile_emotion = xmlDF[['agent_name', 'name', 'transid']]
			test_profile_emotion['isEnthusiastic'] = 'Yes'
			test_profile_emotion['isDefault'] = 'Yes'
		else:
			test_profile['isEnthusiastic'] = np.where(test_profile['enthusiastic'] >= test_profile['mean_enthusiastic'], 'Yes', 'No')
			test_profile_emotion = test_profile[['agent_name', 'name', 'transid','isEnthusiastic']].pivot_table(index = ['agent_name', 'name', 'transid'], columns = 'isEnthusiastic', aggfunc=lambda x: len(x))
			test_profile_emotion['isEnthusiastic'] = test_profile_emotion.idxmax(axis = 1)
			test_profile_emotion = test_profile_emotion.reset_index()
			test_profile_emotion = test_profile_emotion[['agent_name', 'name', 'transid', 'isEnthusiastic']]
			test_profile_emotion['isDefault'] = 'No'

	return(test_profile_emotion)



# In[ ]:




