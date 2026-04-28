import math

class Tower:
    """Tower that attacks enemies within range."""
    COST = 50

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.range = 2.5
        self.fire_rate = 60
        self.cooldown = 0

    def in_range(self, enemy):
        """Return True if the enemy is within the tower's attack radius."""
        dx = enemy.x - self.x
        dy = enemy.y - self.y
        return math.hypot(dx, dy) <= self.range

    def update(self, enemies):
        """Attempt to attack the first enemy within range.

        Applies cooldown before the next shot is allowed.
        """
        if self.cooldown > 0:
            self.cooldown -= 1
            return

        for enemy in enemies:
            if self.in_range(enemy):
                enemy.health -= 1
                print(f"Enemy hit, health left: {enemy.health}")
                self.cooldown = self.fire_rate
                break
