import math

class Enemy:
    """Game enemy that follows a predefined path."""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.target_index = 1
        self.speed = 0.05
        self.reward = 5
        self.health = 3

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
