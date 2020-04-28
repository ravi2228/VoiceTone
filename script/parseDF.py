import xml.etree.ElementTree as ET
import pandas as pd
import os

path = '/home/ec2-user/data/xmlData/'
out_path = '/home/ec2-user/data/output/'
parsedf = pd.DataFrame(columns=['name', 'transid', 'fname', 'lname'])
for filename in os.listdir(path):
    if not filename.endswith('.xml'): continue
    fullname = os.path.join(path, filename)
    tree = ET.parse(fullname)
    root = tree.getroot()
    trans_id = root[0].text
    first_name = root[6].text
    last_name = root[7].text
    dict1 = {'name': fullname, 'transid':trans_id, 'fname': first_name, 'lname': last_name}
    print(dict1)
    parsedf = parsedf.append(dict1, ignore_index=True)

parsedf.to_csv(out_path + 'parseDF.csv')
