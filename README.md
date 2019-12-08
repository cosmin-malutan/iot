# IOT Project notes


#### MQTT subscribe from OSX
mosquitto_sub -d -t "SENSOR" -L mqtts://username:pi@192.168.100.31:1883/SENSOR 

#### MQTT send message to device from OSX
mosquitto_pub -d  -L mqtts://pi:pi@192.168.100.31:1883/DEVICE_MESSAGE -m "Hello world"
mosquitto_pub -d  -L mqtts://pi:pi@192.168.100.31:1883/LIGHT_TOGGLE -m "";

#### Before starting up
edit wpa_supplicant.conf (/Volumes/boot) on pi SD and set the network sid