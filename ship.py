from cmath import rect
import pygame
from pygame.sprite import Sprite
import cv2
import numpy as np

class Ship(Sprite):
    
    def __init__(self,mygame):
        '''Dựng đối tượng ship'''
        super().__init__()
        self.screen = mygame.screen #tạo môi trường chơi game
        self.screen_rect = mygame.screen.get_rect()
        self.settings = mygame.settings
        
        new_size = (150,150)
        self.ship_images = []
        for image_path in ['images/ship1.png', 'images/ship2.png', 'images/ship3.png']:
            image = pygame.image.load(image_path).convert_alpha()
            scaled_image = pygame.transform.scale(image, new_size)  # Scale lại ảnh
            self.ship_images.append(scaled_image)

        self.image = self.ship_images[0]
        self.rect = self.image.get_rect()   #lấy thông số của ảnh ship
        self.rect.midbottom = self.screen_rect.midbottom    #set up tọa độ khởi điểm giữa đáy của môi trường của ship
        self.x = float(self.rect.x)
        
        self.moving_right = False
        self.moving_left = False
        self.ship_index = 0
        self.ship_changing_speed = 100  # Thời gian mỗi khung hình (ms)
        self.animation_timer = pygame.time.get_ticks()

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.animation_timer >= self.ship_changing_speed:
            self.animation_timer = current_time
            self.ship_index = (self.ship_index + 1) % len(self.ship_images)  # Quay vòng hoạt ảnh
            self.image = self.ship_images[self.ship_index]
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed 
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed 
        self.rect.x = self.x

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def displayship(self):
        '''Xuất đối tượng ship ra màn hình'''
        self.screen.blit(self.image,self.rect)  #vẽ ship tại tọa độ 