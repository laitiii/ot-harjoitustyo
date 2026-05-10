import pygame

class WaveManager:
    """Manage enemy waves and spawn timing."""

    def __init__(
        self,
        base_enemies,
        enemies_per_wave,
        spawn_interval,
        min_spawn_interval,
        spawn_interval_decrease,
    ):
        self.base_enemies = base_enemies
        self.enemies_per_wave = enemies_per_wave
        self.spawn_interval_base = spawn_interval
        self.min_spawn_interval = min_spawn_interval
        self.spawn_interval_decrease = spawn_interval_decrease

        self.wave_enemies_pending = 0
        self.next_spawn_time = 0
        self.spawn_interval = spawn_interval

    def reset(self):
        """Reset wave timing and pending enemy counts."""
        self.wave_enemies_pending = 0
        self.next_spawn_time = 0
        self.spawn_interval = self.spawn_interval_base

    def start_wave(self, wave, spawn_position):
        """Begin a new wave and return the first spawned enemy."""
        enemy_count = self.base_enemies + (wave - 1) * self.enemies_per_wave
        self.spawn_interval = max(
            self.min_spawn_interval,
            self.spawn_interval_base - (wave - 1) * self.spawn_interval_decrease,
        )
        self.wave_enemies_pending = max(0, enemy_count - 1)
        self.next_spawn_time = pygame.time.get_ticks() + self.spawn_interval

        if enemy_count > 0:
            return [spawn_position]

        self.next_spawn_time = 0
        return []

    def spawn_pending_enemy(self, current_time, spawn_position):
        """Spawn the next queued enemy when its spawn time is reached."""
        if self.wave_enemies_pending > 0 and current_time >= self.next_spawn_time:
            self.wave_enemies_pending -= 1
            self.next_spawn_time = current_time + self.spawn_interval
            return spawn_position

        return None
