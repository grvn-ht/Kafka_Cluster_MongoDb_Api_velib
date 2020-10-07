import json
import time
import urllib.request

from kafka import KafkaProducer

url = "https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel&rows=1500"

producer = KafkaProducer(bootstrap_servers=["kafka1:29092","kafka2:29093","kafka3:29094"], api_version=(0, 10, 1))

while True:
    response = urllib.request.urlopen(url)
    api_velib = json.loads(response.read().decode())
    records=api_velib['records']
    for i in range(len(records)):
        station=records[i]
        infos_station=station['fields']
        producer.send("velib-stations", json.dumps(infos_station).encode(), key=str(infos_station["stationcode"]).encode())
#    print("{} Produced {} station records".format(time.time(), len(infos_station)))
    time.sleep(1)

