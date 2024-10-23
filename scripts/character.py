import pygame
import os

class Character(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        # Load idle, jump, and run animations
        self.idle_images = self.load_idle_animation()  
        self.jump_images = self.load_jump_animation()  # Load jump animation frames
        self.run_images = self.load_run_animation()    # Load run animation frames
        self.image = self.idle_images[0]  # Start with the first idle frame
        self.rect = self.image.get_rect()

        # Place the character initially in the center of the screen
        self.rect.x = screen_width // 2 - self.rect.width // 2
        self.rect.y = screen_height // 2 - self.rect.height // 2

        self.velocity_y = 0
        self.jump_strength = -15
        self.gravity = 1
        self.on_ground = True  # Start on the ground

        # Animation control variables
        self.idle_frame = 0
        self.run_frame = 0
        self.idle_frame_time = 0
        self.run_frame_time = 0
        self.idle_frame_duration = 300  # Milliseconds per frame for idle animation
        self.run_frame_duration = 150   # Faster animation for running
        self.jump_frame = 0
        self.is_jumping = False  # Track if the character is in a jump state
        self.facing_left = False  # Track if the character is facing left

        # Track spacebar release
        self.space_released = True  # Initially set to True, so the player can jump

        # Load jump4-up and jump4-down images for handling up/down motion
        self.jump4_up = pygame.image.load("assets/jump/jump4-up.png").convert_alpha()
        self.jump4_down = pygame.image.load("assets/jump/jump4-down.png").convert_alpha()

    def load_idle_animation(self):
        # Load all images from the 'assets/idleanimation' folder
        idle_images = []
        idle_folder = "assets/idleanimation"
        for filename in os.listdir(idle_folder):
            if filename.endswith(".png"):
                img = pygame.image.load(os.path.join(idle_folder, filename)).convert_alpha()
                idle_images.append(img)
        return idle_images

    def load_jump_animation(self):
        # Load all images from the 'assets/jump' folder except jump4-up and jump4-down
        jump_images = []
        jump_folder = "assets/jump"
        for filename in sorted(os.listdir(jump_folder)):
            if filename.endswith(".png") and "jump4" not in filename:  # Skip jump4-up and jump4-down
                img = pygame.image.load(os.path.join(jump_folder, filename)).convert_alpha()
                jump_images.append(img)
        return jump_images

    def load_run_animation(self):
        # Load both images from the 'assets/run' folder
        run_images = []
        run_folder = "assets/run"
        for filename in os.listdir(run_folder):
            if filename.endswith(".png"):
                img = pygame.image.load(os.path.join(run_folder, filename)).convert_alpha()
                run_images.append(img)
        return run_images

    def play_run_animation(self):
        """ Play the running animation when moving and on the ground. """
        current_time = pygame.time.get_ticks()
        if current_time - self.run_frame_time > self.run_frame_duration:
            self.run_frame_time = current_time
            self.run_frame = (self.run_frame + 1) % len(self.run_images)  # Loop over run frames
            self.image = self.mirror_image(self.run_images[self.run_frame])  # Mirror the run image
            
    def update(self):
        keys = pygame.key.get_pressed()

        # Handle movement with A/D keys and mirror the image
        moving = False
        if keys[pygame.K_a]:
            self.rect.x -= 5
            self.facing_left = True  # Set facing direction to left
            if self.on_ground == True:
                self.play_run_animation()
            moving = True
        elif keys[pygame.K_d]:
            self.rect.x += 5
            self.facing_left = False  # Set facing direction to right
            if self.on_ground == True:
                self.play_run_animation()
            moving = True

        # Allow jump only if the spacebar was released after the last jump
        if keys[pygame.K_SPACE] and self.on_ground and self.space_released:
            self.velocity_y = self.jump_strength
            self.on_ground = False
            self.is_jumping = True  # Trigger jumping animation
            self.space_released = False  # Block jumping until space is released

        # Check if the spacebar has been released
        if not keys[pygame.K_SPACE]:
            self.space_released = True  # Allow jump when space is released

        # Apply gravity
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        # Check if the character is on the ground
        if self.rect.bottom >= 600:  # Assuming 600 is the bottom of the screen
            self.rect.bottom = 600
            if self.is_jumping:
                self.play_landing_animation()  # Handle landing
            self.on_ground = True
            self.is_jumping = False
        else:
            self.on_ground = False  # The character is in the air

        # Handle animations based on state
        if self.is_jumping:
            self.play_jump_animation()
        elif moving and self.on_ground:
            # Prioritize running animation if moving and on the ground
            self.play_run_animation()  # Call run animation here when moving on the ground
        else:
            # Only play idle animation if the player is not moving and not jumping
            self.play_idle_animation()

    def play_idle_animation(self):
        """ Play the idle animation and mirror based on direction. """
        current_time = pygame.time.get_ticks()
        if current_time - self.idle_frame_time > self.idle_frame_duration:
            self.idle_frame_time = current_time
            self.idle_frame = (self.idle_frame + 1) % len(self.idle_images)  # Loop over frames
            self.image = self.mirror_image(self.idle_images[self.idle_frame])  # Mirror the idle image


    def play_jump_animation(self):
        """ Play the jump animation, and show jump4-up or jump4-down based on vertical velocity. """
        if self.jump_frame < len(self.jump_images) - 1:
            # Loop through jump animation frames until jump4
            self.image = self.mirror_image(self.jump_images[self.jump_frame])
            self.jump_frame += 1
        else:
            # Show jump4-up if moving upward, jump4-down if falling
            if self.velocity_y < 0:
                self.image = self.mirror_image(self.jump4_up)
            else:
                self.image = self.mirror_image(self.jump4_down)

    def play_landing_animation(self):
        """ Play landing animation once the character hits the ground. """
        self.image = self.mirror_image(self.jump_images[-2])  # Play jump3.png on landing
        self.jump_frame = 0  # Reset the jump frame for the next jump

    def mirror_image(self, image):
        """ Mirror the image based on the direction the character is facing. """
        if self.facing_left:
            return pygame.transform.flip(image, True, False)  # Flip horizontally if facing left
        return image  # Return the normal image if facing right

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def land_on_ground(self, ground_top):
        self.rect.bottom = ground_top
        self.velocity_y = 0
        self.on_ground = True
        self.is_jumping = False
