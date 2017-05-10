# Matt Reilly and Nick Palutsis

import sys
import os
import math
import pygame
import json
from pygame.locals import *
from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from pong_game import GameSpace
from twisted.internet.task import LoopingCall

GAME_SERVER = 'ash.campus.nd.edu'
PORT1 = 40052
PORT2 = 40001   # TODO: replace with Nicks port

#server receives on

class PlayerConnectionFactory(ClientFactory):
    def __init__(self, game):
        self.game = game

    def buildProtocol(self, addr):
        return PlayerConnection(self.game)

class PlayerConnection(LineReceiver):
    def __init__(self, game):
        self.game = game
        # Send player connection to the game
        self.game.transferConnectionObject(self) 

    def lineReceived(self, line):
        self.handleReceivedData(line)

    def connectionMade(self):
        print 'Made connection with game server.'

    def connectionLost(self, reason):
        print 'Lost connection to game server.'

    def handleReceivedData(self, data):
        # Load data into JSON object, let the game handle it
        obj = json.loads(data)
        self.game.handleData(obj)


if __name__ == "__main__":
    # host is the first to connect, and hosts the game
    # join attaches to the game
    if len(sys.argv) == 1 or len(sys.argv) > 2:     # CLA will be either host or joing
        print "Incorrect number of arguments."
        sys.exit(0)
    # Set up a twisted LoopingCall for server ticks, bind it to the game tick
    if sys.argv[1] == 'host':
        game = GameSpace(1)
        DESIRED_FPS = 30.0
        tick = LoopingCall(game.game_tick)
        tick.start(1.0 / DESIRED_FPS)
        reactor.connectTCP(GAME_SERVER, PORT1, PlayerConnectionFactory(game))
    elif sys.argv[1] == 'join':
        game = GameSpace(2)
        DESIRED_FPS = 30.0
        tick = LoopingCall(game.game_tick)
        tick.start(1.0 / DESIRED_FPS)
        reactor.connectTCP(GAME_SERVER, PORT2, PlayerConnectionFactory(game))
    else:
        print "Either host or join must be the argument"
        sys.exit(0)
    reactor.run()