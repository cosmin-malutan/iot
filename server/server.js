"use strict";
process.title = 'node-server';
const webSocketsServerPort = 8090;
const webSocketServer = require('websocket').server;
const http = require('http');
const express = require('express');
const mqtt = require('mqtt')
const config = require('./config.json')
const app = express();


var clients = {};

var link = config.mqtt.protocol + "://" + config.mqtt.host + ":" + config.mqtt.port;
console.log(link)
const client = mqtt.connect(link, {
    username:  config.mqtt.username,
    password: config.mqtt.password,
    rejectUnauthorized: false
})
client.on('connect', () => {
    console.log('Connected to MQTT');
    client.subscribe(config.mqtt.sensorTopic)
})

client.on('message', (topic, message) => {
    if (topic == config.mqtt.sensorTopic) {
        Object.values(clients).forEach(wsClient => {
            wsClient.sendUTF(message);
        });
    }
})

client.on('error', (error) => {
    console.error(error)
})

app.get('/', function (req, res) {
    res.sendfile(__dirname + '/ui/index.html');
});
app.use(express.static('ui'))
app.listen(8080, function () {
    console.log('Example app listening on port 8080!')
})

/**
 * HTTP server
 */
var server = http.createServer(function(request, response) {
    // Not important for us. We're writing WebSocket server, not HTTP server
});
server.listen(webSocketsServerPort, function() {
    console.log((new Date()) + " Server is listening on port " + webSocketsServerPort);
});
/**
 * WebSocket server
 */
var wsServer = new webSocketServer({
    httpServer: server
});

// This callback function is called every time someone
// tries to connect to the WebSocket server
wsServer.on('request', function(request) {
    console.log((new Date()) + ' Connection from origin ' + request.origin + '.');

    // accept connection - you should check 'request.origin' to make sure that
    // client is connecting from your website
    // (http://en.wikipedia.org/wiki/Same_origin_policy)
    var connection = request.accept(null, request.origin); 
    // we need to know client index to remove them on 'close' event
    clients[connection.remoteAddress] = connection;
    console.log((new Date()) + ' Connection accepted.');

    // user sent some message
    connection.on('message', function(message) {
       var command = JSON.parse(message.utf8Data);
       if (command.type == "message") {
           client.publish(config.mqtt.messageTopic, command.message);
       }
       if (command.type == "toggle") {
           client.publish(config.mqtt.lightToggleTopic, "");
       }
    });

    // user disconnected
    connection.on('close', function(connection) {
        console.log((new Date()) + " Peer "  + this.remoteAddress + " disconnected.");
        delete clients[this.remoteAddress];
    });

});

setInterval(() => {
    console.log("Clients length " + Object.keys(clients).length);
}, 10000)