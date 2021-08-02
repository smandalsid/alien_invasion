import pygame
from pygame.sprite import Sprite
class Bullet(Sprite):
    def __init__(self,ai_sets,screen,ship):
        super(Bullet,self).__init__()
        self.screen=screen
        self.ai_sets=ai_sets
        self.ship=ship
        self.rect=pygame.Rect(0,0,ai_sets.bullet_width,ai_sets.bullet_height)
        self.rect.centerx=self.ship.rect.centerx
        self.rect.top=self.ship.rect.top
        self.y=float(self.rect.y)
        self.color=self.ai_sets.bullet_color
        self.speed_factor=self.ai_sets.bullet_speed_factor

    def update(self):
        self.y-=self.speed_factor
        self.rect.y=self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen,self.color,self.rect)