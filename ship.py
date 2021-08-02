import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self,ai_sets,screen):
        super(Ship,self).__init__()
        self.screen=screen
        self.ai_sets=ai_sets
        self.image=pygame.image.load('/home/siddharth/Documents/ubuntu_python_work/alien_invasion/images/ship.bmp')
        self.rect=self.image.get_rect()
        self.screen_rect=self.screen.get_rect()
        self.rect.centerx=self.screen_rect.centerx
        self.rect.bottom=self.screen_rect.bottom
        self.center=float(self.rect.centerx)
        self.moving_right=False
        self.moving_left=False

    def update(self):
        if self.moving_right and self.rect.right<self.screen_rect.right:
            self.center+=self.ai_sets.ship_speed_factor
        if self.moving_left and self.rect.left>0:
            self.center-=self.ai_sets.ship_speed_factor
        self.rect.centerx=self.center

    def blitme(self):
        self.screen.blit(self.image,self.rect)

    def center_ship(self):
        self.center=self.screen_rect.centerx