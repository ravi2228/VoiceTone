import pandas as pd
import numpy as np
df = pd.read_csv('../modelFiles/agent_profileRaw.csv')
allAgent = df.groupby(['agent_name']).agg({'enthusiastic':np.median, 'transid':lambda x: x.nunique()}).reset_index()

xmlDF = pd.read_csv('../xmlParsed.csv')
dt = xmlDF['date'][0]
fname = '../agentProfiles/agentProfile' + dt + '.csv'
allAgent.to_csv(fname)

fname2 =  '../xmlOutput/xmlParsed' + dt + '.csv'
xmlDF.to_csv(fname2)
