from Structures import Coordinates


class Background:
    def __init__(self, bitmap):
        self.bitmap = bitmap
        self.max_coordinates = Coordinates(int(bitmap['width']), int(bitmap['height']))
        self.bot_size = Coordinates(self.max_coordinates.x // 100, self.max_coordinates.y // 100)
        self.__draw_background()

    def __draw_background(self):
        for item in range(self.bot_size.x // 2,
                          self.max_coordinates.x - self.bot_size.x // 2 + self.bot_size.x,
                          self.bot_size.x):
            self.bitmap.create_line(item,
                                    self.bot_size.y // 2,
                                    item,
                                    self.max_coordinates.y - self.bot_size.y // 2,
                                    fill='lightgrey')
        for item in range(self.bot_size.y // 2,
                          self.max_coordinates.y - self.bot_size.y // 2 + self.bot_size.y,
                          self.bot_size.y):
            self.bitmap.create_line(self.bot_size.x // 2,
                                    item,
                                    self.max_coordinates.x - self.bot_size.x // 2,
                                    item,
                                    fill='lightgrey')
