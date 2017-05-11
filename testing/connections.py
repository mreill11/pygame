from twisted.internet.protocol import Factory
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
import sys

#normal player factory
class PlayerFactory(Factory):
    def __init__(self, pNum):
        self.playerConn = PlayerConnection(pNum)

    def buildProtocol(self, addr):
        return self.playerConn


class PlayerConnection(Protocol):
    def __init__(self, pNum):
        self.connected = 0
        self.pNum = pNum
        #self.poke = poke
        self.inp = ""

    def connectionMade(self):
        print "Connection made."
        self.connected = 1

    def dataReceived(self, data):
        if data.startswith("getPoke"):
            #self.transport.write(self.poke)
            pass
        elif data == "special":
            self.inp = "special"
        else:
            self.inp = data

#client player factory
class PlayerCFactory(ClientFactory):
    def __init__(self, pNum):
        self.playerConn = PlayerConnection(pNum)

    def buildProtocol(self, addr):
        return self.playerConn