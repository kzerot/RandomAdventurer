__author__ = 'murre'
from direct.showbase.ShowBase import ShowBase

from classes.controls import *
from classes.player import Player
import sys


class World(ShowBase):

    def __init__(self, reactor, is_server=False):
        ShowBase.__init__(self)
        self.reactor = reactor
        self.client = None
        self.players = {}
        self.player = None
        self.instance = None
        self.gc = globalClock
        self.load_instance("content/entity/terr")
        self.is_server = is_server
        if not is_server:
            self.set_player()
            Controls(self)

    def load_instance(self, model):
        self.instance = self.loader.loadModel(model)
        self.instance.reparentTo(render)
        #self.instance.setScale(0.25, 0.25, 0.25)
        self.instance.setPos(0, 0, 0)
        self.instance.setScale(5, 5, 5)

    def set_player(self):
        self.player = Player("content/entity/man", self)
        self.player.set_pos(0, 0, 0)
        self.player.set_move_task()
        self.player.is_player = True

    def player_enter(self, id=None):
        player = Player("content/entity/man", self)
        player.set_pos(0, 0, 0)
        player.set_move_task()
        player.id = id
        self.player_add(player, id)
        return player

    def player_add(self, player, id):
        # self.players.append(player)
        self.players[id] = player

    def state_change(self, data):
        """data: players, mobs
        fires then state changed
        Default - server version"""
        print 'Server stateChange', data

    def update_data(self, data):
        print "updateData", data
        if "add_player" in data:
            self.player_enter(data["add_player"])
        if "player" in data:
            self.update_player(data["player"])
        if "players" in data:
            for p in data["players"]:
                self.update_player(p)

    def update_player(self, data):
        player = None
        if "id" not in data or (not self.is_server and data["id"] == self.player.id):
            # Without ID it's client's player
            player = self.player
        elif "id" in data:
            if data["id"] in self.players:
                player = self.players[data["id"]]
            else:
                # Add player!
                player = self.player_enter(data["id"])
        else:
            print "Incorrect data", data
            return
        if "action" in data:
            player.set_control(data["action"][0], data["action"][1])
        if "actions" in data:
            player.actions = data["actions"]
        if "loc" in data:
            player.set_pos(data["loc"])

    def get_players(self):
        return self.players

    def stop(self):
        print 'going to bed...'
        self.taskMgr.stop()
        print 'stop reactor'
        self.reactor.stop()
        print 'close window'
        self.closeWindow(self.win)
        print 'sys.exit'
        sys.exit()
        print 'user exit'
        base.userExit()