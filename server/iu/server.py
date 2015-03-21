from __future__ import absolute_import

import json
import sockjs.tornado
from time import time
from iu.game import Game
from iu.messages import CLIENT_MESSAGES
from iu.utils import logger, uuid


game = Game(logger)
last_time = time()
connections = {}


class GameConnection(sockjs.tornado.SockJSConnection):
    def __init__(self, *args, **kwargs):
        super(GameConnection, self).__init__(*args, **kwargs)
        self.id = "connection_{}".format(uuid())

    def on_open(self, info):
        connections[self.id] = self

    def on_message(self, message):
        data = json.loads(message)

        if data["type"] not in CLIENT_MESSAGES:
            raise ValueError("Unknown message type {}".format(data["type"]))

        msg = CLIENT_MESSAGES[data["type"]](game, self.id, data)
        msg.process()

    def on_close(self):
        connections.pop(self.id, None)


def main_loop():
    """
    Will be called periodically to progress the game
    :return:
    """
    global last_time

    start = time()
    elapsed = start - last_time
    game.tick(elapsed)

    messages = game.get_messages()

    for connection_id in messages:
        if connection_id in connections:
            connection = connections[connection_id]
            connection.send(json.dumps([
                message.to_dict()
                for message in messages[connection_id]
            ]))

    last_time = time()
