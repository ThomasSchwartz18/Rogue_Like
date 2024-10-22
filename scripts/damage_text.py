import pygame

class DamageText:
    def __init__(self, x, y, damage, duration=60):
        self.x = x
        self.y = y
        self.damage = damage
        self.color = (255, 0, 0)  # Red color for the damage text
        self.font = pygame.font.Font(None, 24)  # Font size 24
        self.duration = duration  # Duration the text remains on the screen
        self.alpha = 255  # Full opacity to start

    def update(self):
        # Decrease the duration and move the text upward slightly
        self.duration -= 1
        self.y -= 1
        self.alpha = max(0, self.alpha - 4)  # Fade out the text

    def draw(self, screen, camera):
        if self.duration > 0:
            # Adjust position based on the camera's offset
            adjusted_x = self.x - camera.camera.x
            adjusted_y = self.y - camera.camera.y

            text_surface = self.font.render(str(self.damage), True, self.color)
            text_surface.set_alpha(self.alpha)  # Apply the fading effect
            screen.blit(text_surface, (adjusted_x, adjusted_y))

    def is_expired(self):
        return self.duration <= 0
