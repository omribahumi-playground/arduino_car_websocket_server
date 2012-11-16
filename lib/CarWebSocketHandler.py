#!/usr/bin/python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from tornado import websocket
import json
from CarDispatcher import *

class CarWebSocketHandler(websocket.WebSocketHandler):
    def on_message(self, message):
        CarDispatcher.instance().dispatch(**json.loads(message))

__all__ = ['CarWebSocketHandler']
