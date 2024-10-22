import pygame

class Movement:
    def __init__(self, rect, map_width, map_height):
        self.rect = rect  # Reference to the character's position (rect)
        self.speed = 5  # Regular movement speed
        self.dash_speed = 15  # Dash movement speed
        self.dash_distance = 100  # Distance for dash to cover
        self.is_dashing = False  # Dash state
        self.dash_traveled = 0  # Distance traveled in the dash
        self.dash_direction = pygame.Vector2(0, 0)  # Direction of the dash
        self.space_released = True  # Tracks if SPACE has been released
        self.map_width = map_width
        self.map_height = map_height
        self.bullets = []  # Store all bullets
        
        # Laser properties
        self.laser_active = False  # Whether the laser is active
        self.laser_end = None  # Current or last mouse position for the laser
        self.laser_color = (255, 0, 0)  # Red laser color
        self.laser_damage = 25  # Amount of damage dealt by the laser per frame

    def handle_keys(self, character):
        keys = pygame.key.get_pressed()
        move_direction = pygame.Vector2(0, 0)

        # Move left or right
        if keys[pygame.K_a]:  # Left
            move_direction.x = -1
        if keys[pygame.K_d]:  # Right
            move_direction.x = 1
        if keys[pygame.K_w]:  # Up
            move_direction.y = -1
        if keys[pygame.K_s]:  # Down
            move_direction.y = 1

        # Normalize the movement vector to prevent diagonal speed boost
        if move_direction.length() > 0:
            move_direction = move_direction.normalize()

        # Apply regular movement if not dashing
        if not self.is_dashing:
            new_x = self.rect.x + move_direction.x * self.speed
            new_y = self.rect.y + move_direction.y * self.speed

            # Restrict movement to stay within the map boundaries
            self.rect.x = max(0, min(new_x, self.map_width - self.rect.width))
            self.rect.y = max(0, min(new_y, self.map_height - self.rect.height))

        # Only allow dashing if there is movement
        if keys[pygame.K_SPACE] and not self.is_dashing and self.space_released and move_direction.length() > 0:
            if character.dash():  # Call character.dash() to check if they have enough stamina
                self.is_dashing = True
                self.dash_direction = move_direction
                self.dash_traveled = 0  # Reset dash distance traveled
            self.space_released = False  # Mark SPACE as pressed

        # Ensure SPACE must be released before another dash
        if not keys[pygame.K_SPACE]:
            self.space_released = True  # Reset when SPACE is released

        # Handle laser logic when mouse1 is pressed
        if pygame.mouse.get_pressed()[0]:  # Left mouse button (mouse1)
            self.laser_active = True
            self.laser_end = pygame.mouse.get_pos()  # The laser ends at the current mouse position
        else:
            self.laser_active = False  # Deactivate the laser when mouse1 is released



    def apply_dash(self):
        if self.is_dashing:
            # Move in the dash direction and track the distance traveled
            dash_step_x = self.dash_direction.x * self.dash_speed
            dash_step_y = self.dash_direction.y * self.dash_speed
            new_x = self.rect.x + dash_step_x
            new_y = self.rect.y + dash_step_y

            # Restrict dashing to stay within the map boundaries
            self.rect.x = max(0, min(new_x, self.map_width - self.rect.width))
            self.rect.y = max(0, min(new_y, self.map_height - self.rect.height))

            self.dash_traveled += abs(dash_step_x) + abs(dash_step_y)

            # Stop dashing when the traveled distance reaches the dash limit
            if self.dash_traveled >= self.dash_distance:
                self.is_dashing = False  # Stop dashing

    def draw_laser(self, screen, camera, enemy_squares):
        if self.laser_active and self.laser_end:
            # Get the player's world position (not adjusted for camera)
            laser_start = self.rect.center  # Get the exact center of the player in world coordinates

            # Get the laser end position in world coordinates (adjusting the mouse position for camera movement)
            laser_end = (self.laser_end[0] + camera.camera.x, self.laser_end[1] + camera.camera.y)

            # Draw the laser line from the player to the mouse in screen coordinates (for visual purposes)
            laser_start_screen = self.rect.move(-camera.camera.x, -camera.camera.y).center
            pygame.draw.line(screen, self.laser_color, laser_start_screen, self.laser_end, 5)

            # Check if the laser intersects with any enemy squares in world coordinates
            for enemy in enemy_squares[:]:
                # Check if the world-space laser intersects with the world-space enemy rect
                if enemy.rect.clipline(laser_start, laser_end):
                    print(f"Laser hit enemy at position: {enemy.rect.topleft}")  # Print the collision details

                    # Deal continuous damage while the laser intersects the square
                    if enemy.take_damage(self.laser_damage):
                        enemy_squares.remove(enemy)  # Remove enemy if health <= 0



