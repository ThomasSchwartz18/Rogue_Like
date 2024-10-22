import pygame
from scripts.movement import Movement

class Character:
    def __init__(self, x, y, map_width, map_height):
        self.radius = 25  # Radius of the character circle
        self.rect = pygame.Rect(x - self.radius, y - self.radius, self.radius * 2, self.radius * 2)  # Position and size
        self.color = (255, 255, 255)  # Character's color (white)
        self.outline_color = (0, 0, 0)  # Black outline color
        self.outline_thickness = 3  # Thickness for the outline
        self.movement = Movement(self.rect, map_width, map_height)  # Pass map dimensions to Movement

        # Character's health
        self.health = 100
        self.max_health = 100

        # Stamina attributes
        self.max_stamina = 3  # Max stamina sections (3)
        self.stamina = self.max_stamina  # Current stamina
        self.stamina_recharge_rate = 120  # Frames it takes to recharge one section (2 seconds at 60 FPS)
        self.stamina_recharge_timer = 0  # Timer to track recharge

        # Damage cooldown
        self.damage_cooldown = 0  # Cooldown timer for taking damage

    def update(self):
        self.movement.handle_keys(self)  # Pass the character instance to handle_keys()
        self.movement.apply_dash()  # Apply dash logic if active

        # Reduce the damage cooldown timer
        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1

        # Recharge stamina
        self.recharge_stamina()

    def dash(self):
        """Handle stamina usage for dashing."""
        if self.stamina > 0:  # Can dash only if stamina is available
            self.stamina -= 1  # Use one stamina section
            print(f"Character dashed! Remaining stamina: {self.stamina}")
            # Apply dash movement logic here
            return True
        else:
            print("No stamina left to dash!")
            return False

    def recharge_stamina(self):
        """Recharge stamina over time."""
        if self.stamina < self.max_stamina:
            self.stamina_recharge_timer += 1
            if self.stamina_recharge_timer >= self.stamina_recharge_rate:
                self.stamina += 1  # Recharge one section of stamina
                self.stamina_recharge_timer = 0  # Reset timer
                print(f"Stamina recharged: {self.stamina}/{self.max_stamina}")

    def take_damage(self, damage):
        if self.damage_cooldown <= 0:
            self.health -= damage
            print(f"Character took {damage} damage! Current health: {self.health}")
            self.damage_cooldown = 60  # Set cooldown to 1 second at 60 FPS

    def draw(self, screen, position, camera, enemy_squares):
        # Draw the black outline first
        pygame.draw.circle(screen, self.outline_color, position.center, self.radius + self.outline_thickness)

        # Draw the player as a circle on top of the outline
        pygame.draw.circle(screen, self.color, position.center, self.radius)

        # Draw the laser if active, passing the camera and enemy_squares
        self.movement.draw_laser(screen, camera, enemy_squares)

        # Draw the character's health and stamina bars
        self.draw_health_bar(screen)
        self.draw_stamina_bar(screen)

    def draw_health_bar(self, screen):
        # Define health bar dimensions and position in the top left of the screen
        health_bar_width = 200
        health_bar_height = 20
        health_bar_x = 20  # Distance from the left of the screen
        health_bar_y = 20  # Distance from the top of the screen

        # Calculate current health bar width based on the character's current health
        current_health_width = int(health_bar_width * (self.health / self.max_health))

        # Draw the health bar background (red)
        pygame.draw.rect(screen, (255, 0, 0), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))

        # Draw the current health (green)
        pygame.draw.rect(screen, (0, 255, 0), (health_bar_x, health_bar_y, current_health_width, health_bar_height))

        # Optionally, draw a border around the health bar
        pygame.draw.rect(screen, (0, 0, 0), (health_bar_x, health_bar_y, health_bar_width, health_bar_height), 2)  # Black border

    def draw_stamina_bar(self, screen):
        # Stamina bar below the health bar
        stamina_bar_width = 200
        stamina_bar_height = 10
        stamina_bar_x = 20
        stamina_bar_y = 50  # Below the health bar

        # Dark green color for the stamina bar
        dark_green = (0, 100, 0)

        # Calculate width of each stamina section
        section_width = stamina_bar_width // self.max_stamina

        # Draw each section of the stamina bar
        for i in range(self.max_stamina):
            if i < self.stamina:
                # Filled section (dark green)
                pygame.draw.rect(screen, dark_green, (stamina_bar_x + i * section_width, stamina_bar_y, section_width, stamina_bar_height))
            else:
                # Empty section (red)
                pygame.draw.rect(screen, (255, 0, 0), (stamina_bar_x + i * section_width, stamina_bar_y, section_width, stamina_bar_height))

        # Optionally, draw a border around the stamina bar
        pygame.draw.rect(screen, (0, 0, 0), (stamina_bar_x, stamina_bar_y, stamina_bar_width, stamina_bar_height), 2)  # Black border
