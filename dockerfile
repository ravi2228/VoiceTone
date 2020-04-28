FROM ubuntu:18.04
MAINTAINER Ravi Prakash Singh

COPY ./script /app/script
COPY ./data /app/data
COPY ./modelFiles /app/modelFiles
COPY ./output /app/output
COPY ./voiceTone_api.py /app/
COPY ./praatShell.sh /app/
COPY ./SegmentSoundAgent.R /app/
COPY ./requirements.txt /app/

WORKDIR /app/
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
	apt-get install -y python3 && \
	apt install -y python3-pip && \
	pip3 install -r requirements.txt && \
	pip3 install flask boto3 && \
	apt-get install -y praat && \
	apt-get install -y ffmpeg && \
	apt-get install -y r-base


EXPOSE 7272

CMD ["python3", "voiceTone_api.py"]