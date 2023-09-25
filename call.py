import random
import time

from paho.mqtt import client as mqtt_client
from faker import Faker


broker = 'ec2-34-215-20-244.us-west-2.compute.amazonaws.com'
port = 1883
topic_A = "Annoy/A"
topic_B = "Annoy/B"
# Generate a Client ID with the publish prefix.
client_id = f'publish-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'


fake = Faker(['zh_TW'])
Faker.seed(0)
fake.seed_instance(0)
fake.seed_locale('zh_TW', 4000)


def connect_mqtt():
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


def publish(client):
    msg_count = 1
    while True:
        time.sleep(1)
        msg_A = f"{fake.phone_number()}"
        time.sleep(1)
        msg_B = f"{fake.phone_number()}"
        time.sleep(1)
        result_A = client.publish(topic_A, msg_A)
        result_B = client.publish(topic_B, msg_B)
        # result: [0, 1]
        status_A = result_A[0]
        status_B = result_B[0]
        if status_A == 0:
            print(f"Send `{msg_A}` to topic `{topic_A}`")
        else:
            print(f"Failed to send message to topic {topic_A}")
        if status_B == 0:
            print(f"Send `{msg_B}` to topic `{topic_B}`")
        else:
            print(f"Failed to send message to topic {topic_B}")
        msg_count += 1
        if msg_count > 1:
            break


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)
    client.loop_stop()


if __name__ == '__main__':
    while True:
        run()
        time.sleep(5)
