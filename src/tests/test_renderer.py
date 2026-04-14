import unittest
import pygame
from enemy import Enemy
from renderer import Renderer


class TestRenderer(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.scale = 20
        self.screen = pygame.Surface((self.scale * 2, self.scale * 2))

        self.images = [
            pygame.Surface((self.scale, self.scale)),
            pygame.Surface((self.scale, self.scale))
        ]

        self.images[0].fill((10, 10, 10))
        self.images[1].fill((200, 200, 200))

    def tearDown(self):
        pygame.quit()

    def test_tiles_are_drawn(self):
        renderer = Renderer(self.screen, self.scale, [[0, 1], [1, 0]], self.images)
        renderer.draw_game([], 2, 2)

        color = self.screen.get_at((5, 5))[:3]
        self.assertEqual(color, (10, 10, 10))

    def test_enemy_is_drawn(self):
        renderer = Renderer(self.screen, self.scale, [[0, 0], [0, 0]], self.images)

        enemy = Enemy(0, 1)
        renderer.draw_game([enemy], 2, 2)

        center = (
            int(enemy.x * self.scale + self.scale // 2),
            int(enemy.y * self.scale + self.scale // 2)
        )

        color = self.screen.get_at(center)[:3]
        self.assertEqual(color, (255, 0, 0))


if __name__ == "__main__":
    unittest.main()
