# Matt Reilly and Nick Palutsis

from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue
from twisted.internet.task import LoopingCall
import json

PLAYER1_PORT = 40052
PLAYER1_HOST = ""

PLAYER2_PORT = 40001 # replace with Nicks port
PLAYER2_HOST = ""

dq = DeferredQueue()

FPS = 30.0

class GameState:
    def __init__(self):
        # variables to track game state

    def getPlayer1_Connection(self, p1_conn):
        self.player1_Conn = p1_conn

    def getPLayer2_Connection(self, p2_conn):
        self.player2_Conn = p2_conn






class Player1_ConnFactory(Factory):
    def buildProtocol(self, addr):
        return Player1_Connection(addr)

class Player1_Connection(Protocol):
    def __init__(self, addr):
        self.addr = addr
        PLAYER1_HOST = addr.host
        #self.player2_conn = ""

    def dataReceived(self, data):
        # data received from player 1
        dq.put(data)
        #print str(data)

    def connectionMade(self):
        print "Connection receieved from player 1"
        # listen for player 2
        gs.getPlayer1_Connection(self)
        reactor.listenTCP(PLAYER2_PORT, Player2_ConnFactory(self))
 
    def connectionLost(self, reason):
        print "Lost connection from player 1:", str(reason)

    def startForwarding(self):
        # start forwarding the player 1 data
        print "sendData"
        dq.get().addCallback(gs.decode_data)

    def sendData(self, data):
        self.transport.write(data + '\r\n')        

    def getPlayer2_Connection(self, player2_conn):
        self.player2_conn = player2_conn

class Player2_ConnFactory(Factory):
    def __init__(self, player1_conn):
        self.player1_conn = player1_conn

    def buildProtocol(self, addr):
        return Player2_Connection(addr, self.player1_conn)

class Player2_Connection(Protocol):
    def __init__(self, addr, player1_conn):
        self.addr = addr
        print addr
        PLAYER2_HOST = addr.host
        self.player1_conn = player1_conn

    def dataReceived(self, data):
        # data received from player 2
        dq.put(data)

    def connectionMade(self):
        print "Connection receieved from player 2"
        print "ready to begin game"
        self.player1_conn.getPlayer2_Connection(self)
        gs.getPlayer2_Connection(self)
        self.startForwarding()

    def connectionLost(self, reason):
        print "Lost connection from player 2:", str(reason)

    def startForwarding(self):
        # start forwarding the player 2 data
        #dq.get().addCallback(gs.decode_data)
        dq.get().addCallback(gs.decode_data)

    def sendData(self, data):
        self.transport.write(data + '\r\n')