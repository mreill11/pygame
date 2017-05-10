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
        #pass
        self.posPlayer1 = 0
        self.posPlayer2 = 0
        self.posBall = [0, 0]
        self.velPlayer1 = 0
        self.velPlayer2 = 0
        self.velBall = [0, 0]
        self.scorePlayer1 = 0
        self.scorePlayer2 = 0



    def getPlayer1_Connection(self, p1_conn):
        self.player1_Conn = p1_conn

    def getPLayer2_Connection(self, p2_conn):
        self.player2_Conn = p2_conn

    def decodeData(self, data):
        dataList = data.split(":")
        if dataList[1] == '-1':
            return
        if dataList[0] == '1':  # player 1
            if dataList[1] == 'UP':
                # move paddle up
                self.velPlayer1 -= 16
            elif dataList[1] == 'DOWN':
                # move paddle down
                self.velPlayer2 += 16
            else:
                velPlayer2 = 0
                #pass
        elif dataList[0] == '2':
            if dataList[1] == 'UP':
                # move paddle up
                self.velPlayer2 -= 16
            elif dataList[1] == 'DOWN':
                # move paddle down
                self.velPlayer2 += 16
            else:
                self.velPlayer2 = 0
                #pass

        else:
            print "Error: unexpected data."

        response = json.dumps({'posPlayer1':self.posPlayer1,
                                'posPlayer2':self.posPlayer2,
                                'posBall':posBall,
                                'velPlayer1':velPlayer1,
                                'velPlayer2':velPlayer2,
                                'velBall':velBall,
                                'scorePlayer1':scorePlayer1,
                                'scorePlayer2':scorePlayer2})

        self.player1_Conn.sendData(response)
        self.player2_Conn.sendData(response)
        dq.get().addCallback(self.decode_data)



gs = GameState()


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

if __name__ == "__main__":
    reactor.listenTCP(PLAYER1_PORT, Player1_ConnFactory())
    reactor.run()