import pygame
from pygame.sprite import Sprite
import random

class Alien(Sprite):

    def __init__(self,mygame):
        super().__init__()
        self.screen = mygame.screen
        self.settings = mygame.settings

        alien_images = [
            'images/alien1.png',
            'images/alien2.png',
            'images/alien3.png',
            'images/alien4.png',
            'images/alien5.png',
            'images/alien6.png'
        ]
        selected_image = random.choice(alien_images)
        self.image = pygame.image.load(selected_image).convert_alpha()
        self.image = pygame.transform.scale(self.image,(80,80))
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.health = 10
        self.damage = 10
        self.exploding = False

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
    
        # Hiệu ứng nổ
        self.exploding = False
        self.explosion_images = []

        # Kích thước mới (ví dụ 50x50)
        new_size = (50, 50)

        # Tải và scale các hình ảnh
        for image_path in ['images/explosion1.png', 'images/explosion2.png', 'images/explosion3.png']:
            image = pygame.image.load(image_path).convert_alpha()
            scaled_image = pygame.transform.scale(image, new_size)  # Scale lại ảnh
            self.explosion_images.append(scaled_image)

        self.speed_x = self.settings.alien_speed
        self.speed_y = 0
            
        self.explosion_index = 0
        self.explosion_speed = 100  # Thời gian mỗi khung hình (ms)
        self.explosion_timer = pygame.time.get_ticks()

    def checkedges(self):
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)
    
    def take_damage(self):
        """Giảm số máu của Boss khi bị tấn công"""
        self.health -= self.damage
        if self.health <= 0 and not self.exploding:
            self.start_explosion()

    def start_explosion(self):
        """Kích hoạt hiệu ứng nổ"""
        self.exploding = True
        self.explosion_start_time = pygame.time.get_ticks()  # Lưu thời gian bắt đầu
        self.explosion_index = 0
        self.image = self.explosion_images[self.explosion_index]


    def update(self):
        if self.exploding:
            # Xử lý hoạt ảnh nổ
            current_time = pygame.time.get_ticks()
            if current_time - self.explosion_timer >= self.explosion_speed:
                self.explosion_timer = current_time
                if self.explosion_index < len(self.explosion_images) - 1:
                    self.explosion_index += 1
                    self.image = self.explosion_images[self.explosion_index]
                else:
                    # Nếu hết khung hình và đã đủ 2 giây, xóa alien
                    if current_time - self.explosion_start_time >= 100:  # 2000ms = 2 giây
                        self.kill()
        else:
            # Di chuyển theo trục ngang (X)
            self.rect.x += self.settings.alien_speed * self.settings.fleet_direction
    
    def draw(self):
        self.screen.blit(self.image, self.rect)
