import math

class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.range = 2.5
        self.fire_rate = 60
        self.cooldown = 0

    def in_range(self, enemy):
        dx = enemy.x - self.x
        dy = enemy.y - self.y
        return math.hypot(dx, dy) <= self.range

    def update(self, enemies):
        if self.cooldown > 0:
            self.cooldown -= 1
            return

        for enemy in enemies:
            if self.in_range(enemy):
                # placeholder: "shoot"
                print("Tower hits enemy")
                self.cooldown = self.fire_rate
                break
