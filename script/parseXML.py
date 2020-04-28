import xml.etree.ElementTree as ET
import pandas as pd
import os

def xml(pth):
    path = pth
    parsedf = pd.DataFrame(columns=['name', 'transid', 'direction','date', 'fname', 'lname','agentID', 'duration', 'radioselection', 'glowEligible', 'glowAccepted', 'glowOffered', 'glowDeclineReason', 'glowproductsku'])
    for filename in os.listdir(path):
        if not filename.endswith('.xml'): continue
        fullname = os.path.join(path, filename)
        print(fullname)
        tree = ET.parse(fullname)
        root = tree.getroot()
        trans_id = root[0].text
        dire = root[13].text
        d = root[1].text
        first_name = root[6].text
        last_name = root[7].text
        agent_id = root[4].text
        dur = root[8].text
        if len(root[16]) > 6:
            glowE = root[16][1].text
            glowA = root[16][2].text
            glowO = root[16][3].text
            glowDR = root[16][5].text
            glowpr = root[16][4].text
            rs = root[16][6].text
        else:
            glowE = 'empty'
            glowA = 'empty'
            glowO = 'empty'
            glowDR = 'empty'
            glowpr = 'empty'
            rs = 'empty'

        dict1 = {'name': 'wavFile', 'transid':trans_id,'direction':dire,'date':d, 'fname': first_name, 'lname': last_name, 'agentID': agent_id, 'duration':dur, 'radioselection': rs,  'glowEligible': glowE, 'glowAccepted': glowA, 'glowOffered': glowO, 'glowDeclineReason': glowDR, 'glowproductsku': glowpr}
        parsedf = parsedf.append(dict1, ignore_index=True)
        return parsedf



# In[ ]:


#parsedf.to_csv('../xmlParsed.csv')

