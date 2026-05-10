import os
import sys
import pygame
import constants
from entities.enemy import Enemy
from entities.tower import Tower
from level_data import LEVEL_MAP, PATH
from renderer import Renderer
from wave_manager import WaveManager


class GameController:
    """Main tower defense game controller."""

    def __init__(self):
        pygame.init()

        self.base_dir = os.path.dirname(__file__)
        self.assets_dir = os.path.join(self.base_dir, "assets")

        self.state = "menu"
        self.spawn_position = (0, 1)

        self.wave_manager = WaveManager(
            constants.BASE_ENEMIES,
            constants.ENEMIES_PER_WAVE,
            constants.SPAWN_INTERVAL,
            constants.MIN_SPAWN_INTERVAL,
            constants.SPAWN_INTERVAL_DECREASE,
        )

        self.towers: list[Tower] = []
        self.enemies: list[Enemy] = []
        self.lives = constants.INITIAL_LIVES
        self.money = constants.INITIAL_MONEY

        self.new_game()

        self.height = len(self.level_map)
        self.width = len(self.level_map[0])
        self.scale = constants.TILE_SIZE

        screen_height = self.scale * self.height
        screen_width = self.scale * self.width
        self.screen = pygame.display.set_mode((screen_width, screen_height))

        pygame.display.set_caption("PyTD")

        self.load_images()

        self.renderer = Renderer(
            self.screen,
            self.scale,
            self.level_map,
            self.images,
        )

    def load_images(self):
        """Load the game tile and turret images from disk."""
        self.images = []
        for name in ["grass", "path", "turret"]:
            image_path = os.path.join(self.assets_dir, f"{name}.png")
            self.images.append(pygame.image.load(image_path).convert())

    def new_game(self):
        """Reset the level map, path, and wave progress."""
        self.level_map = LEVEL_MAP
        self.path = PATH
        self.wave = 1
        self.wave_manager.reset()
        self.enemies = []
        self.towers = []
        self.lives = constants.INITIAL_LIVES
        self.money = constants.INITIAL_MONEY

    def start_wave(self):
        """Launch the next enemy wave."""
        spawn_positions = self.wave_manager.start_wave(self.wave, self.spawn_position)
        self.enemies = [Enemy(*pos, self.wave) for pos in spawn_positions]
        print(f"Wave {self.wave} started with {self.wave_manager.base_enemies + (self.wave - 1) * self.wave_manager.enemies_per_wave} enemies")

    def place_tower(self, mouse_pos):
        """Place a tower at the mouse position if placement is valid."""
        mx, my = mouse_pos
        grid_x = mx // self.scale
        grid_y = my // self.scale

        if self.money < Tower.COST:
            print("Not enough money")
            return

        if grid_y < 0 or grid_y >= self.height:
            return
        if grid_x < 0 or grid_x >= self.width:
            return

        if self.level_map[grid_y][grid_x] == 1:
            return

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
        """Update the game state during each frame."""
        if self.state != "game":
            return

        self.spawn_pending_enemy()
        self.move_enemies()
        self.update_towers()
        self.cleanup_dead_enemies()
        self.check_wave_state()

    def spawn_pending_enemy(self):
        """Spawn the next queued enemy when its spawn time is reached."""
        enemy_position = self.wave_manager.spawn_pending_enemy(
            pygame.time.get_ticks(),
            self.spawn_position,
        )

        if enemy_position is not None:
            self.enemies.append(Enemy(*enemy_position, self.wave))

    def move_enemies(self):
        """Move each active enemy along the defined path."""
        despawn_list = []
        for enemy in self.enemies:
            enemy.move(self.path)
            if enemy.is_finished(self.path):
                despawn_list.append(enemy)
                self.lives -= 1

        for enemy in despawn_list:
            self.enemies.remove(enemy)

    def update_towers(self):
        """Update all towers so they can attack visible enemies."""
        for tower in self.towers:
            tower.update(self.enemies)

    def cleanup_dead_enemies(self):
        """Remove enemies with zero health and award the player their reward."""
        dead_enemies = []
        for enemy in self.enemies:
            if enemy.health <= 0:
                dead_enemies.append(enemy)
                self.money += enemy.reward

        for enemy in dead_enemies:
            self.enemies.remove(enemy)

    def check_wave_state(self):
        """Check whether the wave is finished or the game is over."""
        if self.lives <= 0:
            self.state = "game_over"
            print("Game Over")
            return

        if not self.enemies and self.wave_manager.wave_enemies_pending == 0:
            self.state = "build"
            self.wave += 1
            print(f"Wave {self.wave - 1} completed")

    def reset_game(self):
        """Reset game progress and return to the build phase."""
        self.new_game()
        self.state = "build"
        print("Build phase started")

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if self.state in ("game", "build"):
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.place_tower(pygame.mouse.get_pos())

            if event.type != pygame.KEYDOWN:
                continue

            if self.state == "menu":
                if event.key == pygame.K_SPACE:
                    self.reset_game()
                continue

            if self.state == "game_over":
                if event.key == pygame.K_SPACE:
                    self.reset_game()
                return

            if self.state == "build" and event.key == pygame.K_SPACE:
                self.start_wave()
                self.state = "game"
                return

    def draw(self):
        self.screen.fill((0, 0, 0))

        if self.state == "menu":
            self.renderer.draw_menu()
        elif self.state == "build":
            self.renderer.draw_build(self.towers, self.height, self.width)
            self.renderer.draw_status_bar(
                f"Lives: {self.lives}  Money: {self.money}",
                f"Build phase · Wave {self.wave}",
            )
        elif self.state == "game":
            self.renderer.draw_game(self.enemies, self.height, self.width)
            self.renderer.draw_towers(self.towers)
            self.renderer.draw_status_bar(
                f"Lives: {self.lives}  Money: {self.money}",
                f"Wave: {self.wave}",
            )
        elif self.state == "game_over":
            self.renderer.draw_game_over()

        pygame.display.flip()

    def run(self):
        self.game_loop()
