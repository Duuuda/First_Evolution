from random import randint
from collections import namedtuple


# important_shit
Coordinates = namedtuple('Coordinates', ['x', 'y'])


# structure_0
class Storage:
    def __init__(self, *args):
        self.alive = dict()
        self.dead = dict()
        for item in args:
            self.add_item(item)

    def add_item(self, item):
        self.alive[item.id] = item

    def delete_item(self, item):
        if item.id in self.alive:
            del self.alive[item.id]
        if item.id in self.dead:
            del self.dead[item.id]

    def move_to_dead(self, new_id, old_id):
        item = self.alive[new_id]
        del self.alive[new_id]
        self.dead[old_id] = item


# structure_1
class Genome:
    def __init__(self, color='#00ff00', genes=None):
        # energy
        self.energy = 5.0
        # generation
        self.children_left = 10
        self.mutant_child = randint(1, self.children_left)
        # color
        self.color = color
        self.line_color = '#000000'
        self.die_color = '#800080'
        # command
        self.command_photosynthesis = (22, 23, 24, 25)
        self.command_eat = (12, 13, 14, 15)
        # profits
        self.move_profit = 1.0
        self.child_profit = 4.0
        self.food_profit = 3.0
        self.photosynthesis_profit = 1.0
        # steps
        self.now_gen = 0
        self.genes = genes if genes is not None else [12, 25, 25, 25, 14, 25, 15, 13, 25]
