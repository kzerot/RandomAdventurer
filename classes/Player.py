from classes.creature import Creature

import json


class Player(Creature):
    """Player has many parts, and all of them we must sync"""

    def __init__(self, model, world):
        Creature.__init__(self, model, world)
        self.is_player = False
        self.target_rotation = (0, 0)
        self.target = None

    def set_control(self, key, value):
        """TODO """
        changed = False
        if value and key not in self.actions:
            self.actions.append(key)
            changed = True
        elif not value and key in self.actions:
            self.actions.remove(key)
            changed = True

        if changed and self.is_player:
            self.world.state_change(json.dumps({"action": [key, value]}))

    def move(self, task):
        return Creature.move(self, task)