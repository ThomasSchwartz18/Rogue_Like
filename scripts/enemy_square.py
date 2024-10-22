import pygame
import random
from scripts.damage_text import DamageText

class EnemySquare:
    def __init__(self, x, y, target_rect, speed=3, health=100, damage_interval=10, max_health=100):
        self.rect = pygame.Rect(x, y, 40, 40)  # Size of the enemy square (40x40)
        self.color = (0, 255, 0)  # Green color for the enemy square
        self.target_rect = target_rect  # The player's rect (target to follow)
        self.speed = speed  # Speed at which the square moves toward the player
        self.health = health  # Health of the enemy
        self.max_health = max_health
        self.damage_texts = []  # List to hold floating damage texts
        self.damage_cooldown = 0  # Cooldown timer to control damage frequency
        self.damage_interval = damage_interval  # Number of frames between damage ticks


    def take_damage(self, damage):
        # Only deal damage if the cooldown has expired
        if self.damage_cooldown <= 0:
            self.health -= damage
            # Create a damage text above the enemy square when it takes damage
            damage_text = DamageText(self.rect.centerx, self.rect.top - 10, damage)
            self.damage_texts.append(damage_text)

            # Reset the damage cooldown
            self.damage_cooldown = self.damage_interval

        if self.health <= 0:
            return True  # Enemy is dead
        return False
    
    def update(self):
        # Decrease the damage cooldown timer
        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1

        # Calculate the direction vector from the enemy square to the player
        direction = pygame.Vector2(self.target_rect.centerx - self.rect.centerx, self.target_rect.centery - self.rect.centery)

        if direction.length() > 0:
            direction = direction.normalize()

        # Move the enemy square in the direction of the player
        self.rect.x += direction.x * self.speed
        self.rect.y += direction.y * self.speed

        # Update the damage texts
        for text in self.damage_texts[:]:
            text.update()
            if text.is_expired():
                self.damage_texts.remove(text)

    def draw(self, screen, camera):
        # Draw the enemy square relative to the camera's position
        screen_rect = self.rect.move(-camera.camera.x, -camera.camera.y)
        pygame.draw.rect(screen, self.color, screen_rect)
        
        # Draw the health bar
        self.draw_health_bar(screen, screen_rect)

        # Draw the damage texts (adjust for camera position)
        for text in self.damage_texts:
            text.draw(screen, camera)

    def draw_health_bar(self, screen, screen_rect):
        # Calculate the width of the health bar based on the current health
        health_bar_width = int(screen_rect.width * (self.health / self.max_health))
        health_bar_height = 5  # Set height of the health bar

        # Adjust the position of the health bar to be below the enemy square
        health_bar_rect = pygame.Rect(screen_rect.left, screen_rect.bottom + 2, health_bar_width, health_bar_height)

        # Draw the background of the health bar (red for missing health)
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(screen_rect.left, screen_rect.bottom + 2, screen_rect.width, health_bar_height))  # Red background
        # Draw the current health (green bar)
        pygame.draw.rect(screen, (0, 255, 0), health_bar_rect)  # Green health
