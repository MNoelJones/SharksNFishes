import pygame
import sys
from random import randint
from functools import cache
from collections import Counter

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)


class CreatureFontError(Exception):
    pass


class Creature:
    def __init__(self, x, y):
        self.x, self.y = (x, y)
        self.next_x, self.next_y = (None, None)
        self.font = None

    @property
    def loc(self):
        return (self.x, self.y)

    @property
    def next_loc(self):
        return (self.next_x, self.next_y)

    @cache
    def get_font(self, blocksize):
        fontsize = self.fontsize
        for fontsize in range(self.fontsize, 0, -1):
            font = pygame.font.SysFont("Calibri", fontsize)
            surface_size = font.size(self.identifier)
            if surface_size[0] < (blocksize - 2) and surface_size[1] < (blocksize - 2):
                break
        else:
            raise CreatureFontError()
        return font

    def get_surface(self, blocksize):
        font = self.get_font(blocksize)
        creature_surface = font.render(self.identifier, False, WHITE)
        return creature_surface

    def move(self, visible_grid):
        pass

    def can_eat(self, creature):
        return False

    def breed(self, visible_grid):
        pass


class Shark(Creature):
    identifier = "S"
    name = "Shark"

    def __init__(self, x, y):
        super().__init__(x, y)
        self.fontsize = 35

    def move(self, visible_grid):
        for loc, creature in visible_grid.items():
            if isinstance(creature, Fish):
                self.next_x = self.x + loc[0]
                self.next_y = self.y + loc[1]
                print(f"Eating fish at ({self.next_x}, {self.next_y})")
                break
        else:
            self.next_x = self.x + randint(-1, 1)
            self.next_y = self.y + randint(-1, 1)

    def can_eat(self, creature):
        return isinstance(creature, Fish)


class Fish(Creature):
    identifier = "F"
    name = "Fish"

    def __init__(self, x, y):
        super().__init__(x, y)
        self.fontsize = 35

    def move(self, _):
        self.next_x = self.x + randint(-1, 1)
        self.next_y = self.y + randint(-1, 1)

    def breed(self, visible_grid):
        pass


class Grid(dict):
    def __init__(self, width, height, parent=None, x_offset=0, y_offset=0):
        self.width = width
        self.height = height
        self.parent = parent
        # Offset from the parent grid, if any
        self.x_offset = x_offset
        self.y_offset = y_offset

    def add(self, creature, at=None):
        if at is None:
            self[creature.loc] = creature
        else:
            self[at] = creature

    def creature_counter(self):
        return Counter([x.__class__.__name__ for x in self.values()])

    def get_window(self, x_centre, y_centre, width, height):
        visible_grid = Grid(
            width, height, parent=self, x_offset=x_centre, y_offset=y_centre
        )
        for x_offset in (-width // 2, 0, width // 2):
            for y_offset in (-height // 2, 0, height // 2):
                loc = (
                    x_centre + x_offset % self.width,
                    y_centre + y_offset % self.height,
                )
                if loc in self:
                    visible_grid.add(self[loc], at=(x_offset, y_offset))
        return visible_grid


class SharksNFishes:
    def __init__(self, width, height, sharks, fish):
        self.initial_fishes = fish
        self.initial_sharks = sharks
        self.width = width
        self.height = height
        self.num_fish = 0
        self.num_sharks = 0
        self.blocksize = 20
        self.grid = Grid(self.width, self.height)
        self.rects = {}

        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode(
            (self.width * self.blocksize, self.height * self.blocksize)
        )
        self.clock = pygame.time.Clock()
        self.screen.fill(BLACK)
        self.initialise_fish()
        self.initialise_sharks()

    def _initialise_creatures(self, creature_class, num_creatures):
        while self.grid.creature_counter()[creature_class.__name__] < num_creatures:
            trial_grid = (randint(0, self.width - 1), randint(0, self.height - 1))
            if trial_grid not in self.grid:
                self.grid.add(creature_class(*trial_grid))

    def initialise_sharks(self):
        self._initialise_creatures(Shark, self.initial_sharks)

    def initialise_fish(self):
        self._initialise_creatures(Fish, self.initial_fishes)

    def drawGrid(self):
        self.screen.fill(BLACK)
        for x in range(0, self.width):
            for y in range(0, self.height):
                rect = pygame.Rect(
                    x * self.blocksize,
                    y * self.blocksize,
                    self.blocksize,
                    self.blocksize,
                )
                pygame.draw.rect(self.screen, WHITE, rect, 1)
                self.rects[(x, y)] = self.screen.subsurface(rect)

    def draw_creatures(self):
        for location, creature in self.grid.items():
            creature_surface = creature.get_surface(self.blocksize)
            self.rects[location].blit(creature_surface, (2, 2))

    def get_visible(self, x, y):
        return self.grid.get_window(x, y, 3, 3)

    def update_creatures(self):
        for creature in self.grid.values():
            creature.move(self.get_visible(creature.x, creature.y))

    def update_grid(self):
        new_grid = Grid(self.width, self.height)
        for loc, creature in self.grid.items():
            new_loc = (creature.next_x, creature.next_y)
            if all([coord is not None for coord in new_loc]):
                new_loc = (new_loc[0] % self.width, new_loc[1] % self.height)
                if (
                    new_loc not in self.grid or creature.can_eat(self.grid[new_loc])
                ) and (new_loc not in new_grid or creature.can_eat(new_grid[new_loc])):
                    creature.x, creature.y = new_loc
                    new_grid.add(creature)
                    print(f"{creature.name} moving from {loc} to {new_loc}")
                else:
                    new_grid.add(creature)
                    creature.next_x, creature.next_y = (None, None)
            else:
                new_grid.add(creature)
        self.grid = new_grid

    def run_updates(self):
        self.update_creatures()
        self.update_grid()
        print(self.grid.creature_counter())

    def run_one_tick(self):
        self.drawGrid()
        self.draw_creatures()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        self.run_updates()
        pygame.time.delay(100)

    def run(self):
        while True:
            self.run_one_tick()


def main():
    snf = SharksNFishes(5, 5, sharks=5, fish=20)
    snf.run()


if __name__ == '__main__':
    main()
