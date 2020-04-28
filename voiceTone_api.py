#!/usr/bin/python
from flask import Flask, request, jsonify, make_response

import numpy as np
import boto3
import sys
import os
import subprocess
import glob
from script.parseXML import xml
from script.shortlistCalls import shortlistCalls
from script.ScoreAgents import ScoreAgents

#%% Initialize app

app = Flask(__name__)

# wavURL = 'https://voice-emotion-for-quality.s3.amazonaws.com/ravi_files/sprint/dockerFiles/ext100_04_20_2020_10%3B02%3B22_37018_WPRNEDCCQVS015V.wav'
# xmlURL = 'https://voice-emotion-for-quality.s3.amazonaws.com/ravi_files/sprint/dockerFiles/ext100_04_20_2020_10%3B02%3B22_37018_WPRNEDCCQVS015V.xml'


@app.route('/', methods=['POST'])
def post1():

	wavURL = request.get_json()['wavURL']
	xmlURL = request.get_json()['xmlURL']

	wavBucket = wavURL[wavURL.find('voice'):wavURL.find('s3')-1]
	wavKey = wavURL[wavURL.find('s3.amazonaws.com/') + len('s3.amazonaws.com/'):].replace('%3B',';')
	xmlBucket = xmlURL[xmlURL.find('voice'):wavURL.find('s3')-1]
	xmlKey = xmlURL[xmlURL.find('s3.amazonaws.com/') + len('s3.amazonaws.com/'):].replace('%3B',';')

# 	session = boto3.Session(
# aws_access_key_id='ASIATEW4EMGDNYJZ6FH6',
# aws_secret_access_key='bfnDsVIWInwuTFcWNtxHGlBqhQHSyqQlgqOvCEKi',
# aws_session_token='FwoGZXIvYXdzEGAaDH46y9o9OOA47CZKjCKQAtFjcj2+83jUC7kYIrB3H37CCIWl+vBgin+FUvSZQirWfThawCvKfqCdClrIYp56u7LwLDM5HLuI4OkWcYrU56f47kTirAA7pCu/spanyuRhrXrSoOlbCjhUm3d7stRHdXz0Bely21K3NmRX2hDdtzyUVXUFUo+oyvoiWbKHbf5NuF3RHQYvwRAL1tfUPURC7yraGN6mhkyvhFA2V/vtj263Pbl12qp4pmF7zLab6C3W4ejMHhFlZI2QlHnQ0ULmyJ/dPKJMPM+4F9yESQ0e6qLqLhK+akn8QodQcObuCLIKcmqfn5vrGEqUrvoPbjn0iH6ItnuG4g4tB+53z1si1iXrC6doNs+9cmhVG8BJDymZKJT7i/UFMit5cTJos3oarMzOY/NdV+6imvpNwOdvrGDAx7/p7qSWtTA/n0C6QqzH8W9V'	)
	

	s3 = boto3.resource('s3')
	# s3 = session.resource('s3')
	wvbucket = s3.Bucket(wavBucket)
	xlbucket = s3.Bucket(xmlBucket)
	wvbucket.download_file(wavKey, "data/wavData/wavFile.wav")
	xlbucket.download_file(xmlKey, "data/xmlData/xmlFile.xml")

	parseXML = xml('data/xmlData/')
	parseXML.to_csv('output/xmlParsed.csv')

	defaultScored = shortlistCalls(parseXML)


	if (defaultScored[0] != '.wav'):
		files = glob.glob('data/wavDataProcessed/*')
		for f in files:
		    os.remove(f)
		subprocess.call(['ffmpeg', '-i', 'data/wavData/wavFile.wav', 'data/wavDataProcessed/wavFile.wav.wav'])

		files = glob.glob('data/wavDataSegmented/*')
		for f in files:
		    os.remove(f)
		# print('I am before Rscript')
		subprocess.call(['Rscript', "SegmentSoundAgent.R"], shell=False)
		# print('I am after R script')
		subprocess.call(['sh', 'praatShell.sh'], shell=False)
		toneProfile = ScoreAgents(parseXML)
	else:
		parseXML['agent_name'] = parseXML['fname'] + " " + parseXML['lname']
		toneProfile = toneProfile[['agent_name', 'name', 'transid']]
		toneProfile['isEnthusiastic'] = 'Yes'
		toneProfile['isDefault'] = 'Yes'

    # result = array_1.dot(array_2).sum()
	return jsonify({'IsEnthusiastic': toneProfile['isEnthusiastic'][0], 'isDefault':toneProfile['isDefault'][0]})

@app.route('/health', methods = ['GET'])
def health():
    return make_response('OK', 200)

if __name__ == "__main__":
	app.run(host = '0.0.0.0', port = 7272, debug = False)





# https://voice-emotion-for-quality.s3.amazonaws.com/ravi_files/sprint/dockerFiles/ext100_04_20_2020_10%3B02%3B22_37018_WPRNEDCCQVS015V.wav