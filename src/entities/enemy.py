import math

class Enemy:
    """Game enemy that follows a predefined path."""

    BASE_HEALTH = 3
    HEALTH_PER_WAVE = 1

    def __init__(self, x, y, wave=1):
        self.x = x
        self.y = y
        self.target_index = 1
        self.speed = 0.05
        self.reward = 10
        self.health = self.BASE_HEALTH + ((wave - 1) // 2) * self.HEALTH_PER_WAVE

    def move(self, path):
        """Move the enemy toward the next path waypoint."""
        if self.target_index >= len(path):
            return

        target_x, target_y = path[self.target_index]

        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.hypot(dx, dy)

        if dist < self.speed:
            self.x = target_x
            self.y = target_y
            self.target_index += 1
        else:
            self.x += self.speed * dx / dist
            self.y += self.speed * dy / dist

    def is_finished(self, path):
        """Return True if the enemy has reached the end of the path."""
        return self.target_index >= len(path)
