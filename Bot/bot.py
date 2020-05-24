from random import randint, choice
from Structures import Coordinates, Genome


class Bot:
    def __init__(self, pos, bitmap, genome, storage):
        # init_bot's_params
        self.pos = pos  # bot's_position
        self.bitmap = bitmap  # bot's_environment
        self.genome = genome  # bot's_genome
        self.storage = storage  # structure_containing_all_bots
        # init_global_params
        self.bot_size = Coordinates(int(self.bitmap['width']) // 100, int(self.bitmap['height']) // 100)
        self.max_coords = Coordinates(int(self.bitmap['width']) // self.bot_size.x - 1,
                                      int(self.bitmap['height']) // self.bot_size.y - 1)
        # first_draw
        self.id = self.bitmap.create_rectangle(self.pos.x * self.bot_size.x - (self.bot_size.x // 2 - 1),
                                               self.pos.y * self.bot_size.y - (self.bot_size.y // 2 - 1),
                                               self.pos.x * self.bot_size.x + (self.bot_size.x // 2 - 1),
                                               self.pos.y * self.bot_size.y + (self.bot_size.y // 2 - 1),
                                               fill=self.genome.color, outline=self.genome.line_color)

    # one_evolutionary_cycle--------------------------------------------------------------------------------------------
    def evolve(self):
        if self.genome.color == '#00ff00':
            self.__green()
        else:
            self.__red()

    def __green(self):
        if self.genome.energy > 0.0:
            if self.genome.energy >= self.genome.child_profit:
                self.genome.energy += self.reproduction(self.nearby_bots())
            elif self.genome.now_gen < len(self.genome.genes):
                if self.genome.genes[self.genome.now_gen] in self.genome.command_photosynthesis:
                    self.genome.energy += self.photosynthesis()
                elif self.genome.energy >= self.genome.move_profit:
                    self.genome.energy += self.move_bot(self.nearby_bots(), self.genome.genes[self.genome.now_gen] % 4)
                self.genome.now_gen += 1
            else:
                self.genome.now_gen = 0  # you_can_also_use_this -> self.kill_bot()
        else:
            self.kill_bot()

    def __red(self):
        if self.genome.energy > 0.0:
            if self.genome.energy >= self.genome.child_profit:
                self.genome.energy += self.reproduction(self.nearby_bots())
            elif self.genome.now_gen < len(self.genome.genes):
                if self.genome.genes[self.genome.now_gen] in self.genome.command_eat:
                    self.genome.energy += self.eat_bot(self.nearby_bots(), self.genome.genes[self.genome.now_gen] % 4)
                elif self.genome.energy >= self.genome.move_profit:
                    self.genome.energy += self.move_bot(self.nearby_bots(), self.genome.genes[self.genome.now_gen] % 4)
                self.genome.now_gen += 1
            else:
                self.genome.now_gen = 0  # you_can_also_use_this -> self.kill_bot()
        else:
            self.kill_bot()

    # reproduction------------------------------------------------------------------------------------------------------
    def reproduction(self, nearby_bots):
        if len(nearby_bots) < 4 and self.genome.children_left:
            num_purpose = choice(tuple(filter(lambda x: x not in nearby_bots.keys(), range(4))))
            if self.genome.mutant_child == self.genome.children_left:
                new_genome = self.genome.genes.copy()
                new_genome[randint(0, len(new_genome) - 1)] = randint(0, 25)
                new_genome[randint(0, len(new_genome) - 1)] = randint(0, 25)
                new_genome[randint(0, len(new_genome) - 1)] = randint(0, 25)
                bot = Bot(self.pos,
                          self.bitmap,
                          Genome(color=self.genome.color, genes=new_genome),
                          self.storage)
                self.storage.add_item(bot)
                bot.move_bot(nearby_bots, num_purpose)
            else:
                bot = Bot(self.pos,
                          self.bitmap,
                          Genome(color=self.genome.color, genes=self.genome.genes.copy()),
                          self.storage)
                self.storage.add_item(bot)
                bot.move_bot(nearby_bots, num_purpose)
            self.genome.children_left -= 1
            return -self.genome.child_profit
        else:
            return 0

    # searching_nearby_bots---------------------------------------------------------------------------------------------
    def nearby_bots(self):
        coords = {(self.pos.x, self.pos.y - 1) if self.pos.y > 1 else (self.pos.x, self.max_coords.y): 0,
                  (self.pos.x + 1, self.pos.y) if self.pos.x < self.max_coords.x else (1, self.pos.y): 1,
                  (self.pos.x, self.pos.y + 1) if self.pos.y < self.max_coords.y else (self.pos.x, 1): 2,
                  (self.pos.x - 1, self.pos.y) if self.pos.x > 1 else (self.max_coords.x, self.pos.y): 3}
        nearby_bots = list(self.storage.alive.copy().values()) + list(self.storage.dead.copy().values())
        nearby_bots = list(filter(lambda x: x.pos in coords, nearby_bots))
        nearby_bots = {coords[nearby_bots[i].pos]: nearby_bots[i] for i in range(len(nearby_bots))}
        return nearby_bots

    # photosynthesis----------------------------------------------------------------------------------------------------
    def photosynthesis(self):
        return self.genome.photosynthesis_profit

    # eating------------------------------------------------------------------------------------------------------------
    def eat_bot(self, nearby_bots, offset):
        target_bot = nearby_bots.get(offset)
        if target_bot is not None:
            if target_bot in self.storage.alive.values() and self.genome.color == target_bot.genome.color:
                return 0
            else:
                target_bot.delete_bot()
                self.move_bot(nearby_bots, offset)
                return self.genome.food_profit
        else:
            self.move_bot(nearby_bots, offset)
            return -0.1  # you_can_also_use_this -> return self.move_bot(nearby_bots, offset)

    # moving_self-------------------------------------------------------------------------------------------------------
    def move_bot(self, nearby_bots, num_purpose):
        if nearby_bots.get(num_purpose) is None:
            if num_purpose == 0:
                if self.pos.y > 1:
                    self.__move_by_offset(0, -1)
                else:
                    self.__move_by_offset(0, self.max_coords.y - 1)
            elif num_purpose == 1:
                if self.pos.x < self.max_coords.x:
                    self.__move_by_offset(1, 0)
                else:
                    self.__move_by_offset(-self.max_coords.x + 1, 0)
            elif num_purpose == 2:
                if self.pos.y < self.max_coords.y:
                    self.__move_by_offset(0, 1)
                else:
                    self.__move_by_offset(0, -self.max_coords.y + 1)
            else:
                if self.pos.x > 1:
                    self.__move_by_offset(-1, 0)
                else:
                    self.__move_by_offset(self.max_coords.x - 1, 0)
            return -self.genome.move_profit
        else:
            return 0

    def __move_by_offset(self, offset_x, offset_y):
        self.pos = Coordinates(self.pos.x + offset_x, self.pos.y + offset_y)
        self.bitmap.move(self.id, self.bot_size.x * offset_x, self.bot_size.y * offset_y)

    # killing_self------------------------------------------------------------------------------------------------------
    def kill_bot(self):
        self.bitmap.delete(self.id)
        old_key = self.id
        self.id = self.bitmap.create_rectangle(self.pos.x * self.bot_size.x - (self.bot_size.x // 2 - 3),
                                               self.pos.y * self.bot_size.y - (self.bot_size.y // 2 - 3),
                                               self.pos.x * self.bot_size.x + (self.bot_size.x // 2 - 3),
                                               self.pos.y * self.bot_size.y + (self.bot_size.y // 2 - 3),
                                               fill=self.genome.die_color, outline=self.genome.die_color)
        self.storage.move_to_dead(old_key, self.id)

    # deleting_self-----------------------------------------------------------------------------------------------------
    def delete_bot(self):
        self.bitmap.delete(self.id)
        self.storage.delete_item(self)
        del self
