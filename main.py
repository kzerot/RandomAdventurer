# -*- coding: utf-8 -*-
from utility.utility import safe_loads
from classes.world import *


__author__ = 'murre'

from direct.showbase.ShowBase import ShowBase
from twisted.internet.task import LoopingCall
from twisted.internet import reactor, defer
from twisted.internet.threads import deferToThread
from twisted.internet.protocol import Protocol, Factory, ClientFactory


from utility.enum import *
import json
import sys

isServer = "-s" in sys.argv
print sys.argv
if isServer:
    print 'Mode: server'
else:
    print 'Mode: client'


class Server(Protocol):

    """docstring for Server"""

    def __init__(self, factory, world):
        self.factory = factory
        self.world = world
        # self.id is connection and player id
        self.id = -1

    def connectionMade(self):
        print 'New player'
        dataToSend = {"add_player": self.factory.numProtocols}
        for p in self.factory.clients:
            p.transport.write(json.dumps(dataToSend))

        players = []
        for pl in self.world.players:
            client_player = self.world.players[pl]
            players.append({
                "id": client_player.id,
                "loc": client_player.get_pos(),
                "actions": client_player.actions
            })
        dataToSend = {"id": self.factory.numProtocols,
                      "players": players}
        self.factory.clients.append(self)
        self.world.player_enter(self.factory.numProtocols)
        self.id = self.factory.numProtocols
        self.transport.write(json.dumps(dataToSend))
        self.factory.numProtocols = self.factory.numProtocols + 1

    def connectionLost(self, reason):
        #self.factory.numProtocols = self.factory.numProtocols - 1
        pass

    def dataReceived(self, data):
        print 'Data received', data
        for jdata in safe_loads(data):
            dataToSend = jdata

            if "id" not in dataToSend:
                dataToSend["id"] = self.id
            self.world.update_player(dataToSend)
            for p in self.factory.clients:
                if p != self:
                    p.transport.write(json.dumps({"player": dataToSend}))


class ServerFactory(Factory):

    def __init__(self, world):
        self.world = world
        self.numProtocols = 0
        self.clients = []

    def buildProtocol(self, addr):
        return Server(self, self.world)


class GameClient(Protocol):

    """docstring for Server"""

    def __init__(self, factory, world):
        self.factory = factory
        self.world = world
        self.world.state_change = self.sendData

    def connectionMade(self):
        print 'Client connected OK'

    def connectionLost(self, reason):
        print 'Lost connect'

    def dataReceived(self, data):
        print "Data received", data
        bigdata = safe_loads(data)
        for jdata in bigdata:
            if "id" in jdata:
                self.world.player.id = jdata["id"]
            self.world.update_data(jdata)

    def sendData(self, data):
        '''data in json.dumps!'''
        print 'send', data
        if not isinstance(data, type("")):
            data = json.dumps(data)
        self.transport.write(data)


class GameClientFactory(ClientFactory):

    def __init__(self, world):
        self.world = world

    def startedConnecting(self, connector):
        print 'Started to connect.'

    def buildProtocol(self, addr):
        print 'Connected.'
        return GameClient(self, self.world)

    def clientConnectionLost(self, connector, reason):
        print 'Lost connection.  Reason:', reason
        # connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print 'Connection failed. Reason:', reason

w = World(reactor, isServer)

if isServer:
    reactor.listenTCP(8123, ServerFactory(w))
else:
    reactor.connectTCP('localhost', 8123, GameClientFactory(w))

LoopingCall(w.taskMgr.step).start(1 / 60)
reactor.run()