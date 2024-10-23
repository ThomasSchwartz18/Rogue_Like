import pygame

class Box(pygame.sprite.Sprite):
    def __init__(self, x, y, ground_level):
        super().__init__()
        # Load the box image from assets
        self.original_image = pygame.image.load("assets/ingame_assets/box.png").convert_alpha()
        
        # Resize the box (increase size by 1.5 times)
        self.image = pygame.transform.scale(self.original_image, (int(self.original_image.get_width() * 1.5), int(self.original_image.get_height() * 1.5)))
        
        self.rect = self.image.get_rect()
        
        # Set the position of the box on the ground
        self.rect.x = x
        self.rect.y = ground_level - self.rect.height  # Ensure the box's bottom aligns with the ground

    def draw(self, screen):
        # Draw the box on the screen
        screen.blit(self.image, self.rect)
