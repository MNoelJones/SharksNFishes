import pygame
import sys
from random import randint
from functools import cache

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)


class CreatureFontError(Exception):
    pass


class Creature:
    def __init__(self, x, y):
        self.x, self.y = (x, y)
        self.font = None

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


class Shark(Creature):
    identifier = "S"

    def __init__(self, x, y):
        super().__init__(x, y)
        self.fontsize = 35


class Fish(Creature):
    identifier = "F"

    def __init__(self, x, y):
        super().__init__(x, y)
        self.fontsize = 35


class SharksNFishes:
    def __init__(self, width, height, initial_sharks, initial_fishes):
        self.initial_fishes = initial_fishes
        self.initial_sharks = initial_sharks
        self.width = width
        self.height = height
        self.num_fish = 0
        self.num_sharks = 0
        self.blocksize = 20
        self.grid = {}
        self.rects = {}

        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((self.width * self.blocksize, self.height * self.blocksize))
        self.clock = pygame.time.Clock()
        self.screen.fill(BLACK)
        self.initialise_fish()
        self.initialise_sharks()

    def _initialise_creatures(self, creature_class, num_creatures):
        creatures = []
        while len(creatures) < num_creatures:
            trial_grid = (randint(0, self.width - 1), randint(0, self.height - 1))
            if trial_grid not in self.grid:
                creatures.append(trial_grid)
                self.grid[trial_grid] = creature_class(*trial_grid)

    def initialise_sharks(self):
        self._initialise_creatures(Shark, self.initial_sharks)

    def initialise_fish(self):
        self._initialise_creatures(Fish, self.initial_fishes)

    def drawGrid(self):
        for x in range(0, self.width):
            for y in range(0, self.height):
                rect = pygame.Rect(x * self.blocksize, y * self.blocksize, self.blocksize, self.blocksize)
                pygame.draw.rect(self.screen, WHITE, rect, 1)
                self.rects[(x, y)] = self.screen.subsurface(rect)

    def draw_creatures(self):
        for location, creature in self.grid.items():
            creature_surface = creature.get_surface(self.blocksize)
            self.rects[location].blit(creature_surface, (2, 2))

    def run(self):
        while True:
            self.drawGrid()
            self.draw_creatures()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()


def main():
    snf = SharksNFishes(20, 20, 10, 20)
    snf.run()


if __name__ == '__main__':
    main()
