import unittest
from entities.tower import Tower
from entities.enemy import Enemy


class TestTower(unittest.TestCase):

    def test_tower_hits_enemy_in_range_and_sets_cooldown(self):
        tower = Tower(0, 0)
        enemy = Enemy(1, 1)

        tower.update([enemy])

        self.assertEqual(enemy.health, 2)
        self.assertEqual(tower.cooldown, tower.fire_rate)


if __name__ == "__main__":
    unittest.main()
