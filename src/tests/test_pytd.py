import unittest
import pygame
from entities.enemy import Enemy
from index import PyTD


class TestPyTD(unittest.TestCase):

    def test_can_create_game(self):
        game = PyTD()
        self.assertIsNotNone(game)

    def test_level_map_size(self):
        game = PyTD()
        self.assertEqual(len(game.level_map), 10)
        self.assertEqual(len(game.level_map[0]), 10)

    def test_place_tower_reduces_money_and_adds_tower(self):
        game = PyTD()
        initial_money = game.money
        game.state = "game"

        game.place_tower((0, 0))

        self.assertEqual(len(game.towers), 1)
        self.assertEqual(game.money, initial_money - 50)
        self.assertEqual((game.towers[0].x, game.towers[0].y), (0, 0))

    def test_invalid_tower_placement(self):
        game = PyTD()
        initial_money = game.money
        game.state = "game"

        game.place_tower((64, 64))

        self.assertEqual(len(game.towers), 0)
        self.assertEqual(game.money, initial_money)

    def test_new_game_initializes_path_and_level_map(self):
        game = PyTD()
        game.level_map[0][0] = 1
        game.path = []

        game.new_game()

        self.assertEqual(game.path[0], (0, 1))
        self.assertEqual(len(game.level_map), 10)
        self.assertEqual(game.level_map[0][0], 0)

    def test_state_change_on_game_over(self):
        game = PyTD()
        game.state = "game"
        game.lives = 0

        game.update()

        self.assertEqual(game.state, "menu")

    def test_event_handler_starts_new_game(self):
        game = PyTD()
        game.state = "menu"
        game.lives = 5
        game.money = 10
        game.towers = [1]
        game.enemies = [1]

        pygame.event.clear()
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE))
        game.event_handler()

        self.assertEqual(game.state, "build")
        self.assertEqual(game.wave, 1)
        self.assertEqual(game.lives, 10)
        self.assertEqual(game.money, 100)
        self.assertEqual(len(game.towers), 0)
        self.assertEqual(len(game.enemies), 0)

    def test_event_handler_starts_wave_from_build(self):
        game = PyTD()
        game.state = "build"
        game.wave = 1

        pygame.event.clear()
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE))
        game.event_handler()

        self.assertEqual(game.state, "game")
        self.assertEqual(len(game.enemies), 1)
        self.assertEqual(game.wave_enemies_pending, 1)

    def test_update_spawns_pending_enemy_after_interval(self):
        game = PyTD()
        game.state = "game"
        game.enemies = [Enemy(0, 1)]
        game.wave_enemies_pending = 1
        game.next_spawn_time = 0

        game.update()

        self.assertEqual(len(game.enemies), 2)
        self.assertEqual(game.wave_enemies_pending, 0)

    def test_spawn_wave_queues_remaining_enemies(self):
        game = PyTD()
        game.wave = 1
        game.spawn_wave()
        self.assertEqual(len(game.enemies), 1)
        self.assertEqual(game.wave_enemies_pending, 1)

        game.wave = 2
        game.spawn_wave()
        self.assertEqual(len(game.enemies), 1)
        self.assertEqual(game.wave_enemies_pending, 3)

    def test_wave_completion_returns_to_build(self):
        game = PyTD()
        game.state = "game"
        game.wave = 1
        enemy = Enemy(0, 1)
        enemy.health = 0
        game.enemies = [enemy]

        game.update()

        self.assertEqual(game.state, "build")
        self.assertEqual(game.wave, 2)
        self.assertEqual(len(game.enemies), 0)


if __name__ == "__main__":
    unittest.main()
