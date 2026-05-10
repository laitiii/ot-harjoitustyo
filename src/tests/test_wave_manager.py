import unittest
import pygame
from entities.enemy import Enemy
from index import PyTD


class TestWaveManager(unittest.TestCase):

    def test_event_handler_starts_wave_from_build(self):
        game = PyTD()
        game.state = "build"
        game.wave = 1

        pygame.event.clear()
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE))
        game.event_handler()

        self.assertEqual(game.state, "game")
        self.assertEqual(len(game.enemies), 1)
        self.assertEqual(game.wave_manager.wave_enemies_pending, 2)

    def test_update_spawns_pending_enemy_after_interval(self):
        game = PyTD()
        game.state = "game"
        game.enemies = [Enemy(0, 1)]
        game.wave_manager.wave_enemies_pending = 1
        game.wave_manager.next_spawn_time = 0

        game.update()

        self.assertEqual(len(game.enemies), 2)
        self.assertEqual(game.wave_manager.wave_enemies_pending, 0)

    def test_spawn_wave_queues_remaining_enemies(self):
        game = PyTD()
        game.wave = 1
        game.start_wave()
        self.assertEqual(len(game.enemies), 1)
        self.assertEqual(game.wave_manager.wave_enemies_pending, 2)

        game.wave = 2
        game.start_wave()
        self.assertEqual(len(game.enemies), 1)
        self.assertEqual(game.wave_manager.wave_enemies_pending, 4)

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
