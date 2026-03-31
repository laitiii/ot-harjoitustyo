import pygame
import sys
import os

class PyTD:
    TILE_SIZE = 64

    def __init__(self):
        pygame.init()

        self.BASE_DIR = os.path.dirname(__file__)
        self.ASSETS_DIR = os.path.join(self.BASE_DIR, "assets")

        self.new_game()

        self.height = len(self.level_map)
        self.width = len(self.level_map[0])
        self.scale = self.TILE_SIZE

        screen_height = self.scale * self.height
        screen_width = self.scale * self.width
        self.screen = pygame.display.set_mode((screen_width, screen_height))

        pygame.display.set_caption("PyTD")

        self.load_images()

    def load_images(self):
        self.images = []
        for name in ["grass", "path"]:
            image_path = os.path.join(self.ASSETS_DIR, f"{name}.png")
            self.images.append(pygame.image.load(image_path).convert())

    def new_game(self):
        self.level_map = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 1, 1, 1, 1, 1, 0, 0],
            [0, 1, 0, 1, 0, 0, 0, 1, 0, 0],
            [0, 1, 1, 1, 0, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 1, 1, 1],
            [0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

    def game_loop(self):
        while True:
            self.event_handler()
            self.draw()

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def run(self):
        self.game_loop()

    def draw(self):
        self.screen.fill((0, 0, 0))

        for y in range(self.height):
            for x in range(self.width):
                image = self.images[self.level_map[y][x]]
                self.screen.blit(image, (x * self.scale, y * self.scale))

        pygame.display.flip()

if __name__ == "__main__":
    game = PyTD()
    game.run()