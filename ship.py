import pygame
from pygame.sprite import Sprite

class Ship(pygame.sprite.Sprite):
    def __init__(self, ai_settings,screen):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        
        #start new ship at the bottom centre of the screen window.
        self.rect.centerx = self.screen_rect.centerx
        # the bottom implies the y-coordinate.
        self.rect.bottom = self.screen_rect.bottom
        self.center = float(self.rect.centerx)
        # movement flag
        self.moving_right = False
        self.moving_left = False
        
    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
            
        # update the ship position from self.center
        self.rect.centerx = self.center
        
    def blitme(self):
        #draw the ship at its current location.
        self.screen.blit(self.image,self.rect)
    
    def center_ship(self):
        # center the ship on the screen
        self.center = self.screen_rect.centerx