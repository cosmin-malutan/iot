

# pylint: disable=import-error
from renderer_client import RendererClient
from mqtt_client import MqttClient
from utils import get_ip_address

import time
import serial

from config import DEVICE_MESSAGE_TOPIC, LIGHT_TOGGLE_TOPIC

global led
led = True

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(DEVICE_MESSAGE_TOPIC)
    client.subscribe(LIGHT_TOGGLE_TOPIC)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print("topic " + msg.topic + " message " + msg.payload)
    if (msg.topic == LIGHT_TOGGLE_TOPIC):
        global led
        led = False if led else True
        userdata[1].write([1] if led else [2])
        userdata[0].setLed(led)
    elif (msg.topic == DEVICE_MESSAGE_TOPIC):
        userdata[0].setMessage(msg.payload)



def main():
    ip_address = get_ip_address('wlan0')
    ser = serial.Serial('/dev/ttyUSB0', 9600)
    renderer_client = RendererClient(ip_address)
    mqtt_client = MqttClient(on_connect, on_message, (renderer_client, ser))


    print("Proceeed to drawing part")

    while (True):
        sensorData = ser.readline()
        while (sensorData):
            renderer_client.setSensorData(sensorData)
            mqtt_client.publish("SENSOR", renderer_client.getState())
            sensorData = ser.readline()

if __name__ == '__main__':
    main()
