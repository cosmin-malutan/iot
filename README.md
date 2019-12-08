# IOT Project notes
* Wire Raspberry PI and arduino as in schematics
* Flash arduino chip with program under arduino directory
* Install MQTT server and clients on raspberry, python and pip
* Copy python directory to raspberry device and edit the config file so it can connect to MQTT
* Install python dependencies
* Connect Arduino and Rapsberry via USB bus
* Start python program on Rapsberry
* Copy server directory to a computer
* Install node dependencies using ```npm i```
* Edit config.json under server directory so it can connect to MQTT broker
* Start the node server ```node server.js```
* Navigate to page ```http://localhost:8080/```

### Schematics
![schematics](https://github.com/cosmin-malutan/iot/raw/master/IO_bb.png)

![App screenshot](https://github.com/cosmin-malutan/iot/raw/master/screenshot3.png)

![Device screenshot 1](https://github.com/cosmin-malutan/iot/raw/master/screenshot1.jpg)

![Device screenshot 2](https://github.com/cosmin-malutan/iot/raw/master/screenshot2.jpg)

#### MQTT subscribe from OSX
mosquitto_sub -d -t "SENSOR" -L mqtts://username:pi@192.168.100.31:1883/SENSOR 

#### MQTT send message to device from OSX
mosquitto_pub -d  -L mqtts://pi:pi@192.168.100.31:1883/DEVICE_MESSAGE -m "Hello world"
mosquitto_pub -d  -L mqtts://pi:pi@192.168.100.31:1883/LIGHT_TOGGLE -m "";
