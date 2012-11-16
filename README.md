arduino_car_websocket_server
============================

A project to control my arduino car through a web socket

The client should open a web socket to http://ip:8888/ and send JSON messages like these:  
{direction: ['left'], speed: 0..3}  
{direction: ['right'], speed: 0..3}  
{direction: ['forward'], speed: 0..3}  
{direction: ['reverse'], speed: 0..3}  
{direction: ['forward', 'left']}  
{direction: ['forward', 'right']}  
{direction: ['reverse', 'left']}  
{direction: ['reverse', 'right']}  

The car schematics are unavailable at this time.
