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
            'arrow_shower_effect': self.load_images('../assets/images/PNG/projectiles_and_effects/arrow_shower_effect'),
        }

        self.index = 0  # To track the current frame in the animation
        
        self.arrow_effect_index = 0  # Separate index for the arrow shower effect
        
        self.current_animation = 'idle'  # Default to the idle animation
        self.image = self.animations[self.current_animation][self.index]
        
        # Set the dimensions of the hitbox (adjust 30, 40 as needed)
        hitbox_width = 30
        hitbox_height = 45
        self.rect = pygame.Rect(x - hitbox_width // 2, y - hitbox_height, hitbox_width, hitbox_height)

        self.speed_x = 5
        self.speed_y = 0
        self.roll_speed = 10  # Roll speed boost
        self.base_speed_x = self.speed_x  # Store base speed for reset after roll
        self.roll_duration = 0  # Track how long the roll lasts
        self.roll_duration_max = 20  # Max duration for the roll in frames
        self.is_rolling = False  # Track whether the player is rolling

        self.gravity = 1
        self.jump_strength = -15
        self.is_jumping = False
        self.is_falling = False  # Tracks if the player is falling (for jump_down animation)
        self.is_attacking = False  # Track if the player is attacking
        self.facing_right = True  # True if the player is facing right
        
        self.is_freeze_for_click = False  # New flag to freeze at halfway point
        self.attack_halfway_reached = False  # Tracks if halfway point is reached
        self.arrow_shower_active = False  # Flag for arrow shower animation
        self.arrow_shower_pos = None  # Store position of the mouse click for the effect

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

    def update(self, ground, screen):
        keys = pygame.key.get_pressed()
        self.is_moving = False

        # Handle rolling (Left Shift) - Priority over all actions
        if keys[pygame.K_LSHIFT] and not self.is_rolling:
            self.start_roll()

        # Smooth roll movement
        if self.is_rolling:
            self.perform_roll()  # Handle the smooth roll movement
            self.animate()  # Ensure that the animation frames update
            return  # Skip other actions while rolling

        # Horizontal movement
        if not self.is_attacking and not self.is_freeze_for_click:
            if keys[pygame.K_a]:
                self.rect.x -= self.speed_x
                self.facing_right = False
                self.is_moving = True
                if not self.is_jumping and not self.is_falling:
                    self.change_animation('run')

            elif keys[pygame.K_d]:
                self.rect.x += self.speed_x
                self.facing_right = True
                self.is_moving = True
                if not self.is_jumping and not self.is_falling:
                    self.change_animation('run')

        # Apply gravity
        self.speed_y += self.gravity
        self.rect.y += self.speed_y

        # Check if the player is falling
        if self.speed_y > 0 and self.is_jumping:
            self.is_falling = True
            self.change_animation('jump_down')

        # Ground collision
        if self.rect.colliderect(ground):
            self.rect.y = ground.top - self.rect.height
            self.speed_y = 0
            self.is_jumping = False
            self.is_falling = False
            if not self.is_moving and not self.is_attacking and not self.is_freeze_for_click and not self.is_rolling:
                self.change_animation('idle')

        # Jumping
        if not self.is_attacking and not self.is_freeze_for_click:
            if keys[pygame.K_SPACE] and not self.is_jumping and not self.is_falling:
                self.is_jumping = True
                self.speed_y = self.jump_strength
                self.change_animation('jump_up')

        # Attacks
        if keys[pygame.K_e] and not self.is_attacking and not self.is_freeze_for_click and not self.is_rolling:
            self.is_attacking = True
            self.change_animation('1_atk')

        if keys[pygame.K_q] and not self.is_attacking and not self.is_freeze_for_click and not self.is_rolling:
            self.is_attacking = True
            self.change_animation('2_atk')
            self.fire_projectile()
            self.attack_start_time = pygame.time.get_ticks()

        if keys[pygame.K_c] and not self.is_attacking and not self.is_freeze_for_click and not self.is_rolling:
            self.is_attacking = True
            self.change_animation('3_atk')

        # Arrow shower trigger
        if self.is_freeze_for_click:
            if pygame.mouse.get_pressed()[0]:
                self.arrow_shower_pos = pygame.mouse.get_pos()
                self.arrow_shower_active = True
                self.is_freeze_for_click = False

        # Update projectiles
        for projectile in self.projectiles:
            projectile.update()

        # If not moving, attacking, or performing other actions, switch to idle
        if not self.is_moving and not self.is_attacking and not self.is_jumping and not self.is_falling and not self.is_freeze_for_click and not self.is_rolling:
            self.change_animation('idle')

        # Animate player
        self.animate()

        # Play arrow shower effect
        if self.arrow_shower_active:
            self.play_arrow_shower_effect(screen)

    def start_roll(self):
        """Initiate the rolling action."""
        self.is_rolling = True
        self.roll_duration = 0
        self.change_animation('roll')

    def perform_roll(self):
        """Perform the roll, incrementing movement for a set duration."""
        self.roll_duration += 1
        if self.facing_right:
            self.rect.x += self.roll_speed
        else:
            self.rect.x -= self.roll_speed

        # Update roll animation
        self.animate()

        # End roll after the maximum duration
        if self.roll_duration >= self.roll_duration_max:
            self.is_rolling = False
            self.change_animation('idle')

    def animate(self):
        """Handle the animation updates and freezing logic."""
        if self.is_freeze_for_click:
            return

        self.animation_counter += 1
        if self.animation_counter >= self.animation_delay:
            self.index = (self.index + 1) % len(self.animations[self.current_animation])
            self.animation_counter = 0

            # Check halfway point in 3_atk animation
            if self.current_animation == '3_atk' and not self.attack_halfway_reached:
                halfway_frame = len(self.animations['3_atk']) // 2
                if self.index == halfway_frame:
                    self.is_freeze_for_click = True
                    self.attack_halfway_reached = True
                    return

            # Fire the second arrow during the 2_atk animation after a delay
            if self.current_animation == '2_atk':
                elapsed_time = pygame.time.get_ticks() - self.attack_start_time
                if elapsed_time > 1490 and not self.second_arrow_fired:
                    self.fire_projectile()
                    self.second_arrow_fired = True

            # Reset attacking state when the attack animation completes
            if self.current_animation == '1_atk' and self.index == 0:
                self.is_attacking = False
                self.change_animation('idle')

            if self.current_animation == '2_atk' and self.index == 0:
                self.is_attacking = False
                self.second_arrow_fired = False
                self.change_animation('idle')

            if self.current_animation == '3_atk' and self.index == 0 and not self.is_freeze_for_click:
                self.is_attacking = False
                self.attack_halfway_reached = False

            # Reset roll state when the roll animation completes
            if self.current_animation == 'roll' and self.index == 0:
                self.is_rolling = False
                self.change_animation('idle')

        # Update the image based on the direction the player is facing
        if self.facing_right:
            self.image = self.animations[self.current_animation][self.index]
        else:
            self.image = pygame.transform.flip(self.animations[self.current_animation][self.index], True, False)

    def fire_projectile(self):
        """Fire an arrow in the direction the player is facing."""
        direction = 1 if self.facing_right else -1
        arrow_x = self.rect.centerx - 70 if self.facing_right else self.rect.centerx - 90
        arrow_y = self.rect.centery - 70

        arrow_speed = 50
        new_arrow = Projectile(arrow_x, arrow_y, direction, speed=arrow_speed)
        self.projectiles.append(new_arrow)

    def change_animation(self, animation_name):
        """Change to a different animation."""
        if self.current_animation != animation_name:
            self.current_animation = animation_name
            self.index = 0

        if self.facing_right:
            self.image = self.animations[self.current_animation][self.index]
        else:
            self.image = pygame.transform.flip(self.animations[self.current_animation][self.index], True, False)

    def draw(self, screen):
        # Adjust the position to center the player image on the hitbox
        image_x = self.rect.centerx - self.image.get_width() // 2
        image_y = self.rect.bottom - self.image.get_height()
        screen.blit(self.image, (image_x, image_y))

        # Draw projectiles
        for projectile in self.projectiles:
            projectile.draw(screen)
