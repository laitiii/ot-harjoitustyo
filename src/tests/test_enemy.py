import unittest
from enemy import Enemy


class TestEnemy(unittest.TestCase):

    def test_move_moves_toward_next_tile(self):
        enemy = Enemy(0, 1)
        path = [(0, 1), (1, 1)]

        enemy.move(path)

        self.assertGreater(enemy.x, 0)
        self.assertEqual(enemy.y, 1)
        self.assertFalse(enemy.is_finished(path))

    def test_already_at_position(self):
        enemy = Enemy(0, 1)
        path = [(0, 1), (0, 1)]

        enemy.move(path)

        self.assertEqual(enemy.x, 0)
        self.assertEqual(enemy.y, 1)
        self.assertTrue(enemy.is_finished(path))

    def test_path_finished(self):
        enemy = Enemy(0, 1)
        enemy.target_index = 2
        path = [(0, 1), (1, 1)]

        enemy.move(path)

        self.assertEqual(enemy.x, 0)
        self.assertEqual(enemy.y, 1)
        self.assertEqual(enemy.target_index, 2)

if __name__ == "__main__":
    unittest.main()
