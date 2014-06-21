__author__ = 'murre'
from classes.entity import Entity
from utility.enum import *
import json


class Movable(Entity):
    def __init__(self, model, world):
        Entity.__init__(self, model, world)
        self.actions = []
        self.id = -1
        # simplify
        self.gc = self.world.gc

        self.speed_forward = 20
        self.speed_back = -10
        self.speed_rotate = 20

        self.look_vec = (0, 0)
        # only H rotate
        self.rotate = 0

    def set_move_task(self):
        self.world.taskMgr.add(self.move, "playerTask")

    def is_key(self, key):
        return key in self.actions

    def move(self, task):
        if self.is_key(FORWARD):
            self.model.setY(self.model, self.gc.getDt() * self.speed_forward)
        elif self.is_key(BACK):
            self.model.setY(self.model, self.gc.getDt() * self.speed_back)

        if self.is_key(ROT_LEFT):
            self.model.setH(self.model, self.gc.getDt() * self.speed_rotate)
        elif self.is_key(ROT_RIGHT):
            self.model.setH(self.model, -self.gc.getDt() * self.speed_rotate)
        self.rotate = self.model.getH(self.world.render)
        return task.cont

    def json(self):
        return json.dumps(self.actions)

    def set_rot(self, rot):
        self.model.setH(rot)