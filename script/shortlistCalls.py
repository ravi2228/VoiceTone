#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None

# In[22]:

def shortlistCalls(file):
	# xml = pd.read_csv('../xmlParsed.csv')
	xml = file

	xml['agent_name'] = xml['fname'] +" "+ xml['lname']
	xml_default_emotion = xml[['agent_name', 'name', 'transid']]
	#xml_default_emotion.to_csv('../output/defaultEmotionProfile.csv')


	#xml_agents = xml.merge(agents, on='agent_name')
	#xml = xml_agents[xml_agents['duration']>10]
	xml = xml[(xml['direction']=='Inbound') | (xml['direction']=='Outbound')]
	print(xml)
	lst = xml['name'] + '.wav'
	return lst
	# lst.to_csv('../agents.txt', sep = ' ', index=False, header=False)

