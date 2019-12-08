
from functools import partial
# pylint: disable=import-error
import paho.mqtt.client as mqtt
import threading

from config import MQTT_HOST, MQTT_PORT, MQTT_USERNAME, MQTT_PASSWORD

class MqttClient:

    # Initializer / Instance Attributes
    def __init__(self, on_connect, on_message, userData):
      self.on_connect = on_connect
      self.on_message = on_message

      self.client = mqtt.Client()
      self.client.username_pw_set(MQTT_USERNAME, password=MQTT_PASSWORD)
      self.client.on_connect = on_connect
      self.client.on_message = on_message
      self.client.user_data_set(userData)

      self.client.connect(MQTT_HOST, MQTT_PORT, 60)
      mqtt_client_thread = threading.Thread(target=self.client.loop_forever)
      mqtt_client_thread.daemon = True
      mqtt_client_thread.start()
      mqtt_client_thread.join(20)

    def publish(self, topic, payload):
      self.client.publish(topic=topic, payload=payload, qos=0, retain=False)