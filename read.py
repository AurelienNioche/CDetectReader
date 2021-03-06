import os
import django
import json

os.environ["DJANGO_SETTINGS_MODULE"] = "CDetectReader.settings"

django.setup()

from read.models import Entry

import random

from paho.mqtt import client as mqtt_client

broker = '172.30.194.93'  # '192.168.0.14'
port = 1883
topic = "cdetect/capture"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'

user_id = -1


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):

    def on_message(client, userdata, msg):
        try:
            json_dic = msg.payload.decode()
            print(f"Received `{json_dic}` from `{msg.topic}` topic")
            write_in_db(json_dic)
        except:
            print(f"Error with msg: {msg}")

    client.subscribe(topic)
    client.on_message = on_message


def run():
    global user_id
    user_id = int(input("user_id:"))
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


def write_in_db(json_dic):
    global user_id
    content = json.loads(json_dic)
    e = Entry(user_id=user_id, **content)
    e.save()


if __name__ == "__main__":
    run()
