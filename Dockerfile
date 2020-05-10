FROM python:3.7

RUN apt-get -y install libatlas-base-dev
RUN pip install -r requirements.txt

RUN pip install git+https://github.com/joan2937/pigpio/archive/v76.zip
