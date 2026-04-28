import sys
import os
import pygame
from entities.enemy import Enemy
from entities.tower import Tower
from renderer import Renderer

class PyTD:
    TILE_SIZE = 64
    SPAWN_INTERVAL = 1000

    def __init__(self):
        pygame.init()

        self.base_dir = os.path.dirname(__file__)
        self.assets_dir = os.path.join(self.base_dir, "assets")

        self.state = "menu"
        self.wave = 1
        self.wave_enemies_pending = 0
        self.next_spawn_time = 0
        self.new_game()
        self.towers: list[Tower] = []
        self.enemies: list[Enemy] = []
        self.lives = 10
        self.money = 100

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
        self.wave = 1
        self.wave_enemies_pending = 0
        self.next_spawn_time = 0

    def spawn_wave(self):
        enemy_count = self.wave * 2

        if enemy_count > 0:
            self.enemies = [Enemy(0, 1)]
            self.wave_enemies_pending = enemy_count - 1
            self.next_spawn_time = pygame.time.get_ticks() + self.SPAWN_INTERVAL
        else:
            self.enemies = []
            self.wave_enemies_pending = 0
            self.next_spawn_time = 0

        print(f"Wave {self.wave} started with {enemy_count} enemies")

    def place_tower(self, mouse_pos):
        mx, my = mouse_pos

        grid_x = mx // self.TILE_SIZE
        grid_y = my // self.TILE_SIZE

        # money check
        if self.money < Tower.COST:
            print("Not enough money")
            return

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
        self.money -= Tower.COST

        print(f"Tower placed at {grid_x}, {grid_y}")

    def game_loop(self):
        clock = pygame.time.Clock()

        while True:
            self.event_handler()
            self.draw()
            self.update()
            clock.tick(60)

    def update(self):
        if self.state != "game":
            return

        self.spawn_pending_enemy()
        self.move_enemies()
        self.update_towers()
        self.cleanup_dead_enemies()
        self.check_wave_state()

    def spawn_pending_enemy(self):
        current_time = pygame.time.get_ticks()
        if self.wave_enemies_pending > 0 and current_time >= self.next_spawn_time:
            self.enemies.append(Enemy(0, 1))
            self.wave_enemies_pending -= 1
            self.next_spawn_time = current_time + self.SPAWN_INTERVAL

    def move_enemies(self):
        despawn_list = []
        for enemy in self.enemies:
            enemy.move(self.path)
            if enemy.is_finished(self.path):
                despawn_list.append(enemy)
                self.lives -= 1

        for enemy in despawn_list:
            self.enemies.remove(enemy)

    def update_towers(self):
        for tower in self.towers:
            tower.update(self.enemies)

    def cleanup_dead_enemies(self):
        dead_enemies = []
        for enemy in self.enemies:
            if enemy.health <= 0:
                dead_enemies.append(enemy)
                self.money += enemy.reward

        for enemy in dead_enemies:
            self.enemies.remove(enemy)

    def check_wave_state(self):
        if self.lives <= 0:
            self.state = "menu"
            print("Game Over")
            return

        if not self.enemies and self.wave_enemies_pending == 0:
            self.state = "build"
            self.wave += 1
            print(f"Wave {self.wave - 1} completed")

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if self.state in ("game", "build"):
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
                    self.money = 100
                    self.state = "build"
                    print("Build phase started")
                continue

            if self.state == "build":
                if event.key == pygame.K_SPACE:
                    self.spawn_wave()
                    self.state = "game"
                return

    def run(self):
        self.game_loop()

    def draw(self):
        self.screen.fill((0, 0, 0))

        if self.state == "menu":
            self.renderer.draw_menu()
        elif self.state == "build":
            self.renderer.draw_build(self.towers, self.height, self.width)
            self.renderer.draw_status_bar(
                f"Lives: {self.lives}  Money: {self.money}",
                f"Build phase · Wave {self.wave}"
            )
        elif self.state == "game":
            self.renderer.draw_game(self.enemies, self.height, self.width)
            self.renderer.draw_towers(self.towers)
            self.renderer.draw_status_bar(
                f"Lives: {self.lives}  Money: {self.money}",
                f"Wave: {self.wave}"
            )

        pygame.display.flip()


if __name__ == "__main__":
    game = PyTD()
    game.run()
