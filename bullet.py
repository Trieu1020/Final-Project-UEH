import pygame
from pygame.sprite import Sprite

class Bullets(Sprite):

    def __init__(self,mygame):
        super().__init__()
        self.screen = mygame.screen
        self.settings = mygame.settings
        self.color = self.settings.bullet_color 

        self.rect = pygame.Rect(0,0,self.settings.bullet_width,self.settings.bullet_height)
        self.rect.midtop = mygame.ship.rect.midtop

        float(self.rect.y)

    def update(self):
        self.rect.y -= self.settings.bullet_speed 
        
    def drawbullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)