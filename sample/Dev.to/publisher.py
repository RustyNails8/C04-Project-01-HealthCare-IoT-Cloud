# import vars from connect.py
from connect import args, client_id, mqtt_connection

from awscrt import mqtt
from datetime import datetime
import json, random, time

while True:
    # set timestamp
    now = datetime.now()

    # set temperature
    temp = random.randrange(10, 40)

    # form the message
    message = f'id: {client_id}, temp: {temp}, time: {now}'

    # publish the  message
    mqtt_connection.publish(
        topic=args.topic,
        payload= json.dumps(message),
        qos=mqtt.QoS.AT_LEAST_ONCE
    )
    print(f'Message published: {message}')
    time.sleep(1)