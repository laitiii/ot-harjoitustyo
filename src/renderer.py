import pygame

class Renderer:
    """Render game visuals on the Pygame screen."""

    def __init__(self, screen, scale, level_map, images):
        self.screen = screen
        self.scale = scale
        self.level_map = level_map
        self.images = images

    def draw_tiles(self, height, width):
        """Draw the level tiles for the given map dimensions."""
        for y in range(height):
            for x in range(width):
                image = self.images[self.level_map[y][x]]
                self.screen.blit(image, (x * self.scale, y * self.scale))

    def draw_game(self, enemies, height, width):
        """Draw the current game map and all active enemies."""
        self.draw_tiles(height, width)

        for enemy in enemies:
            pygame.draw.circle(
                self.screen,
                (255, 0, 0),
                (
                    int(enemy.x * self.scale + self.scale // 2),
                    int(enemy.y * self.scale + self.scale // 2)
                ),
                15
            )

    def draw_build(self, towers, height, width):
        """Draw the build phase map and placed towers."""
        self.draw_tiles(height, width)
        self.draw_towers(towers)

        font = pygame.font.SysFont(None, 36)
        instructions = font.render(
            "Press SPACE to launch the next wave",
            True,
            (255, 255, 255),
        )
        self.screen.blit(instructions, (10, 10))

    def draw_status_bar(self, stats_text, wave_text=None):
        """Draw a bottom status bar with game stats and wave information."""
        width = self.scale * len(self.level_map[0])
        height = self.scale * len(self.level_map)
        bar_height = 60
        bar_rect = pygame.Rect(0, height - bar_height, width, bar_height)

        pygame.draw.rect(self.screen, (0, 0, 0), bar_rect)
        pygame.draw.line(
            self.screen,
            (255, 255, 255),
            (0, height - bar_height),
            (width, height - bar_height),
            2,
        )

        font = pygame.font.SysFont(None, 26)
        stats = font.render(stats_text, True, (255, 255, 255))
        self.screen.blit(stats, (10, height - bar_height + 10))

        if wave_text:
            wave_label = font.render(wave_text, True, (255, 255, 255))
            self.screen.blit(wave_label, (10, height - bar_height + 32))

    def draw_menu(self):
        """Draw the main menu prompt screen."""
        font = pygame.font.SysFont(None, 60)
        text = font.render("Press SPACE to start", True, (255, 255, 255))
        self.screen.blit(text, (100, 200))

    def draw_towers(self, towers):
        """Render all placed towers on the current map."""
        for tower in towers:
            x = int(tower.x * self.scale)
            y = int(tower.y * self.scale)

            self.screen.blit(self.images[2], (x, y))
