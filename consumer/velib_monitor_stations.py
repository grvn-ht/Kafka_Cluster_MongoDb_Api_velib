import json
from kafka import KafkaConsumer
from pymongo import MongoClient

stations={}

consumer = KafkaConsumer("velib-stations", bootstrap_servers=['kafka1:29092','kafka2:29093','kafka3:29094'], group_id="velib-monitor-stations", api_version=(0, 10, 1))
for message in consumer:
    infos_station = json.loads(message.value.decode())
    station_number = infos_station["stationcode"]
    city = infos_station["nom_arrondissement_communes"]
    available_bike_stands = infos_station["numbikesavailable"]

    if city not in stations:
        stations[city] = {}
    city_stations = stations[city]
    if station_number not in city_stations:
        city_stations[station_number] = available_bike_stands

    count_diff = available_bike_stands - city_stations[station_number]
    if count_diff != 0:
        city_stations[station_number] = available_bike_stands
        print("{}{} {} ({})".format(
            "+" if count_diff > 0 else "",
            count_diff, infos_station["name"], city
        ))

    client = MongoClient('mongodb', 27017)
    db = client['velib']
    posts = db.posts
    result = posts.insert_one(infos_station)
print('One post: {0}'.format(result.inserted_id))
