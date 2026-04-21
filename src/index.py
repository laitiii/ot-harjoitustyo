import sys
import os
import pygame
from enemy import Enemy
from tower import Tower
from renderer import Renderer

class PyTD:
    TILE_SIZE = 64

    def __init__(self):
        pygame.init()

        self.base_dir = os.path.dirname(__file__)
        self.assets_dir = os.path.join(self.base_dir, "assets")

        self.state = "menu"
        self.new_game()
        self.towers = []
        self.enemies = []
        self.lives = 10
        self.money = 0

        self.height = len(self.level_map)
        self.width = len(self.level_map[0])
        self.scale = self.TILE_SIZE

        screen_height = self.scale * self.height
        screen_width = self.scale * self.width
        self.screen = pygame.display.set_mode((screen_width, screen_height))

        pygame.display.set_caption("PyTD")

        self.load_images()

        self.renderer = Renderer(
            self.screen,
            self.scale,
            self.level_map,
            self.images
        )

    def load_images(self):
        self.images = []
        for name in ["grass", "path", "turret"]:
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
        ]

    def place_tower(self, mouse_pos):
        mx, my = mouse_pos

        grid_x = mx // self.TILE_SIZE
        grid_y = my // self.TILE_SIZE

        # bounds check
        if grid_y < 0 or grid_y >= self.height:
            return
        if grid_x < 0 or grid_x >= self.width:
            return

        # prevent placement on path
        if self.level_map[grid_y][grid_x] == 1:
            return

        # prevent tower stacking
        for tower in self.towers:
            if int(tower.x) == grid_x and int(tower.y) == grid_y:
                return

        tower = Tower(grid_x, grid_y)
        self.towers.append(tower)

        print(f"Tower placed at {grid_x}, {grid_y}")

    def game_loop(self):
        clock = pygame.time.Clock()

        while True:
            self.event_handler()
            self.draw()
            self.update()
            clock.tick(60)

    def update(self):
        if self.state == "game":
            despawn_list = []

            for enemy in self.enemies:
                enemy.move(self.path)

                if enemy.is_finished(self.path):
                    despawn_list.append(enemy)
                    self.lives -= 1

            for enemy in despawn_list:
                self.enemies.remove(enemy)

            for tower in self.towers:
                tower.update(self.enemies)

            dead_enemies = []

            for enemy in self.enemies:
                if enemy.health <= 0:
                    dead_enemies.append(enemy)
                    self.money += enemy.reward

            for enemy in dead_enemies:
                self.enemies.remove(enemy)

        if self.state == "game" and self.lives <= 0:
            self.state = "menu"
            print("Game Over")

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if self.state == "game":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.place_tower(pygame.mouse.get_pos())

            if event.type != pygame.KEYDOWN:
                continue

            if self.state == "menu":
                if event.key == pygame.K_SPACE:
                    self.new_game()
                    self.enemies = []
                    self.towers = []
                    self.lives = 10
                    self.money = 0
                    self.state = "game"
                    print("Game started")
                continue

            if self.state == "game":
                if event.key == pygame.K_SPACE:
                    enemy = Enemy(0, 1)
                    self.enemies.append(enemy)
                    print("Enemy spawned")

    def run(self):
        self.game_loop()

    def draw(self):
        self.screen.fill((0, 0, 0))

        if self.state == "menu":
            self.renderer.draw_menu()
        elif self.state == "game":
            self.renderer.draw_game(self.enemies, self.height, self.width)
            self.renderer.draw_towers(self.towers)

            font = pygame.font.SysFont(None, 36)
            text = font.render(f"Lives: {self.lives}  Money: {self.money}", True, (255, 255, 255))
            self.screen.blit(text, (10, 10))

        pygame.display.flip()


if __name__ == "__main__":
    game = PyTD()
    game.run()
