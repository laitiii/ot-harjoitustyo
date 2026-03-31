import unittest
from index import PyTD

class TestPyTD(unittest.TestCase):

    def test_can_create_game(self):
        game = PyTD()
        self.assertIsNotNone(game)

    def test_level_map_size(self):
        game = PyTD()
        self.assertEqual(len(game.level_map), 10)
        self.assertEqual(len(game.level_map[0]), 10)

if __name__ == "__main__":
    unittest.main()