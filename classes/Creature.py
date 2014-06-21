from classes.movable import Movable
from direct.actor.Actor import Actor


class Creature(Movable):
    def __init__(self, model, world):
        self.body = None
        self.run_path = '-Run'
        self.model = None
        Movable.__init__(self, model, world)

    def set_model(self, model_path):
        # Player has some parts

        self.model = self.world.render.attachNewNode("creature")
        self.body = Actor(model_path, {
                          'run': model_path + self.run_path,
                          })
        self.body.loop('run')
        self.body.reparentTo(self.model)
        #TODO Make point for sword etc
        #point = self.legs.exposeJoint(None, "modelRoot", "pelvis")
        #self.body = self.world.loader.loadModel('content/entity/torso')
        #self.body.reparent_to(point)