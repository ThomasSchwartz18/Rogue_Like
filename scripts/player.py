import pygame
import os
from projectile import Projectile

class Player:
    def __init__(self, x, y):
        # Load all animations from your folder structure
        self.animations = {
            'idle': self.load_images('../assets/images/PNG/idle'),
            'run': self.load_images('../assets/images/PNG/run'),
            '1_atk': self.load_images('../assets/images/PNG/1_atk'),
            '2_atk': self.load_images('../assets/images/PNG/2_atk'),
            '3_atk': self.load_images('../assets/images/PNG/3_atk'),
            'jump_up': self.load_images('../assets/images/PNG/jump_up'),
            'jump_down': self.load_images('../assets/images/PNG/jump_down'),
            'jump_full': self.load_images('../assets/images/PNG/jump_full'),
            'air_atk': self.load_images('../assets/images/PNG/air_atk'),
            'roll': self.load_images('../assets/images/PNG/roll'),
            'slide': self.load_images('../assets/images/PNG/slide'),
            'slide_loop': self.load_images('../assets/images/PNG/slide_loop'),
            'defend': self.load_images('../assets/images/PNG/defend'),
            'defend_pose': self.load_images('../assets/images/PNG/defend_pose'),
            'take_hit': self.load_images('../assets/images/PNG/take_hit'),
            'sp_atk': self.load_images('../assets/images/PNG/sp_atk'),
            'death': self.load_images('../assets/images/PNG/death'),
            # Add more animations as needed
        }

        self.index = 0  # To track the current frame in the animation
        self.current_animation = 'idle'  # Default to the idle animation
        self.image = self.animations[self.current_animation][self.index]
            # Set the dimensions of the smaller hitbox (adjust 30, 40 as needed)
        hitbox_width = 30
        hitbox_height = 45
        
        # Center the hitbox on the bottom of the player
        self.rect = pygame.Rect(
            x - hitbox_width // 2,  # Center horizontally
            y - hitbox_height,      # Align to the bottom of the player
            hitbox_width,           # Set the width of the hitbox
            hitbox_height           # Set the height of the hitbox
        )
        self.rect.topleft = (x, y)

        self.speed_x = 5
        self.speed_y = 0
        self.gravity = 1
        self.jump_strength = -15
        self.is_jumping = False
        self.is_falling = False  # Tracks if the player is falling (for jump_down animation)
        self.is_attacking = False  # Track if the player is attacking
        self.facing_right = True  # True if the player is facing right

        # Initialize projectiles and attack damage
        self.projectiles = []  # List to track active projectiles
        self.attack_damage = 10  # Damage value for the player's attacks

        # Animation timing
        self.animation_counter = 0
        self.animation_delay = 2.5  # Adjust this to control animation speed
        self.is_moving = False  # Track if the player is moving

        self.second_arrow_fired = False  # Track whether the second arrow has been fired
        self.attack_start_time = 0  # Track the start time of the attack


    def load_images(self, folder_path):
        """Load all images from the given folder and return them as a list."""
        images = []
        for filename in sorted(os.listdir(folder_path)):
            if filename.endswith('.png'):
                img_path = os.path.join(folder_path, filename)
                images.append(pygame.image.load(img_path))
        return images

    def update(self, ground):
        keys = pygame.key.get_pressed()
        self.is_moving = False  # Assume player is idle unless a movement key is pressed

        # Horizontal movement
        if not self.is_attacking:  # Prevent movement while attacking
            if keys[pygame.K_a]:
                self.rect.x -= self.speed_x
                self.facing_right = False  # Player is facing left
                self.is_moving = True
                if not self.is_jumping and not self.is_falling:
                    self.change_animation('run')  # Only run when not jumping

            elif keys[pygame.K_d]:
                self.rect.x += self.speed_x
                self.facing_right = True  # Player is facing right
                self.is_moving = True
                if not self.is_jumping and not self.is_falling:
                    self.change_animation('run')  # Only run when not jumping

        # Apply gravity
        self.speed_y += self.gravity
        self.rect.y += self.speed_y

        # Check if player is falling (after reaching the peak of the jump)
        if self.speed_y > 0 and self.is_jumping:
            self.is_falling = True
            self.change_animation('jump_down')  # Switch to jump_down animation

        # Ground collision
        if self.rect.colliderect(ground):
            self.rect.y = ground.top - self.rect.height  # Place the player on top of the ground
            self.speed_y = 0
            self.is_jumping = False
            self.is_falling = False  # Reset falling state when on the ground
            if not self.is_moving and not self.is_attacking:
                self.change_animation('idle')

        # Jumping
        if not self.is_attacking:  # Prevent jumping while attacking
            if keys[pygame.K_SPACE] and not self.is_jumping and not self.is_falling:
                self.is_jumping = True
                self.speed_y = self.jump_strength
                self.change_animation('jump_up')  # Switch to jump up animation

        # Attacking with E key (playing the 1_atk animation)
        if keys[pygame.K_e] and not self.is_attacking:  # Start attack only if not already attacking
            self.is_attacking = True
            self.change_animation('1_atk')  # Play 1_atk animation when E is pressed

        # Attacking with Q key (playing the 2_atk animation)
        if keys[pygame.K_q] and not self.is_attacking:  # Start 2_atk only if not already attacking
            self.is_attacking = True
            self.change_animation('2_atk')  # Play 2_atk animation when Q is pressed
            self.fire_projectile()  # Fire the first arrow
            self.attack_start_time = pygame.time.get_ticks()  # Record the time the attack starts
                        
        # Update projectiles
        for projectile in self.projectiles:
            projectile.update()

        # If not moving, attacking, or performing other actions, switch to idle
        if not self.is_moving and not self.is_attacking and not self.is_jumping and not self.is_falling:
            self.change_animation('idle')

        self.animate()

    def fire_projectile(self):
        """Fire an arrow in the direction the player is facing."""
        direction = 1 if self.facing_right else -1  # Determine the direction to fire the arrow

        # Adjust arrow release position relative to the player's hitbox
        if self.facing_right:
            arrow_x = self.rect.centerx - 70  # Offset to the right for right-facing
        else:
            arrow_x = self.rect.centerx - 90  # Offset further to the left for left-facing
        
        arrow_y = self.rect.centery - 70  # Adjust this based on the player sprite

        # Fire an arrow with a custom speed (you can adjust the speed)
        arrow_speed = 50  # Adjust this value to control arrow speed
        new_arrow = Projectile(arrow_x, arrow_y, direction, speed=arrow_speed)
        self.projectiles.append(new_arrow)


    def change_animation(self, animation_name):
        """Change to a different animation."""
        if self.current_animation != animation_name:
            self.current_animation = animation_name
            self.index = 0  # Reset the animation index

    def animate(self):
        # Increment animation counter for a delay
        self.animation_counter += 1
        if self.animation_counter >= self.animation_delay:
            self.index = (self.index + 1) % len(self.animations[self.current_animation])  # Loop through images
            self.animation_counter = 0  # Reset counter

            # Check if attack animation is complete
            if self.current_animation == '1_atk' or self.current_animation == '2_atk':
                if self.index == 0:
                    self.is_attacking = False  # End attack when the animation completes
            if self.current_animation == '2_atk':
                elapsed_time = pygame.time.get_ticks() - self.attack_start_time  # Calculate time since attack started
                
                # Fire the second arrow after 300 milliseconds (adjust this value as needed)
                if elapsed_time > 1250 and not self.second_arrow_fired:
                    self.fire_projectile()  # Fire the second arrow
                    self.second_arrow_fired = True  # Make sure this only happens once
                
                # End the attack animation
                if self.index == 0:
                    self.is_attacking = False
                    self.second_arrow_fired = False  # Reset for the next attack

        # Update the image based on the direction the player is facing
        if self.facing_right:
            self.image = self.animations[self.current_animation][self.index]  # Normal direction
        else:
            self.image = pygame.transform.flip(self.animations[self.current_animation][self.index], True, False)  # Flip image

    def draw(self, screen):
        # Adjust the position to center the player image on the hitbox
        image_x = self.rect.centerx - self.image.get_width() // 2  # Center the image horizontally
        image_y = self.rect.bottom - self.image.get_height()       # Align the image bottom to the rect's bottom

        # Draw the player image
        screen.blit(self.image, (image_x, image_y))

        # Draw the red outline around the player's hitbox (rect)
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)  # Red color with thickness of 2 pixels

        # Draw the projectiles
        for projectile in self.projectiles:
            projectile.draw(screen)  # Make sure each projectile is drawn