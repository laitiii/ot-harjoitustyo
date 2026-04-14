import sys
import os
import pygame
from enemy import Enemy

class PyTD:
    TILE_SIZE = 64

    def __init__(self):
        pygame.init()

        self.base_dir = os.path.dirname(__file__)
        self.assets_dir = os.path.join(self.base_dir, "assets")

        self.state = "menu"
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
            image_path = os.path.join(self.assets_dir, f"{name}.png")
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

        self.path = [
            (0, 1),
            (1, 1),
            (1, 2),
            (1, 3),
            (2, 3),
            (3, 3),
            (3, 2),
            (3, 1),
            (4, 1),
            (5, 1),
            (6, 1),
            (7, 1),
            (7, 2),
            (7, 3),
            (6, 3),
            (5, 3),
            (5, 4),
            (5, 5),
            (4, 5),
            (3, 5),
            (2, 5),
            (1, 5),
            (1, 6),
            (1, 7),
            (1, 8),
            (2, 8),
            (3, 8),
            (4, 8),
            (5, 8),
            (6, 8),
            (7, 8),
            (7, 7),
            (7, 6),
            (8, 6),
            (9, 6),
            (10, 6)
        ]

        self.enemies = []

    def game_loop(self):
        clock = pygame.time.Clock()

        while True:
            self.event_handler()
            self.draw()
            self.update()
            clock.tick(60)

    def update(self):
        despawn_list = []

        for enemy in self.enemies:
            enemy.move(self.path)

            if enemy.is_finished(self.path):
                despawn_list.append(enemy)

        for enemy in despawn_list:
            self.enemies.remove(enemy)

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                enemy = Enemy(0, 1)
                self.enemies.append(enemy)
                print("Enemy spawned")


    def run(self):
        self.game_loop()

    def draw(self):
        self.screen.fill((0, 0, 0))

        for y in range(self.height):
            for x in range(self.width):
                image = self.images[self.level_map[y][x]]
                self.screen.blit(image, (x * self.scale, y * self.scale))

        for enemy in self.enemies:
            pygame.draw.circle(
                self.screen,
                (255, 0, 0),
                (
                    enemy.x * self.scale + self.scale // 2,
                    enemy.y * self.scale + self.scale // 2
                ),
                15
            )

        pygame.display.flip()


if __name__ == "__main__":
    game = PyTD()
    game.run()
