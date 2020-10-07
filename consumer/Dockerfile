FROM python:3.8-slim-buster

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY velib_monitor_stations.py ./

CMD [ "python", "./velib_monitor_stations.py" ]
