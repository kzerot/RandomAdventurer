__author__ = 'murre'


class Entity(object):
    def __init__(self, model, world):
        self.world = world
        self.model = None
        self.set_model(model)

    def set_model(self, model_path):
        self.model = self.world.loader.loadModel(model_path)

    def get_pos(self):
        return [self.model.getX(), self.model.getY(), self.model.getZ()]

    def set_pos(self, *args):
        x, y, z = 0, 0, 0
        if len(args) == 1:
            x, y, z = args[0]
        elif len(args) == 3:
          x, y, z = args
        self.model.setPos(self.world.render, x, y, z)
