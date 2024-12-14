import sys
from time import sleep
import pygame
from settings import Settings
from gamestat import GameStats
from ship import Ship
from bullet import Bullets
from alien import Alien
from scoreboard import ScoreBoard



class AlienIvasion:
    
    def __init__(self):
        '''Dựng game'''
        pygame.init()   #khởi tạo game
        self.clock = pygame.time.Clock()    
        self.settings = Settings()

        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))    #cài đặt cấu hình máy phù hợp tùy theo từng máy
        pygame.display.set_caption("SPACE WASTE INVADERS")    #đặt tên game
        
        self.stats = GameStats(self)
        self.sb = ScoreBoard(self)

        self.createfleet()

        self.bg_frames = []
        self.current_bg_frame = 0

        # Danh sách các đường dẫn đến frame ảnh
        total_frames = 2
        frame_files = [f"images/frame{i}.png" for i in range(1, total_frames + 1)]

        # Tải các frame nền từ danh sách
        self.load_background_frames(frame_files)

        self.start_screen_image = pygame.image.load('images/sci.png').convert()
        self.start_screen_image = pygame.transform.scale(self.start_screen_image, (self.settings.screen_width, self.settings.screen_height))

        self.ship = Ship(self)  #khởi tạo đối tượng ship từ lớp Ship
        
        self.game_active = False
        self.start_screen_active = True  # Trạng thái màn hình bắt đầu
        self.instruction_screen_active = False
        self.game_over = False

        pygame.mixer.init()

        # Tải file nhạc nền
        pygame.mixer.music.load('images/background_sound.mp3')  # Đường dẫn đến file nhạc nền
        pygame.mixer.music.set_volume(0.2)  # Điều chỉnh âm lượng (0.0 đến 1.0)
        pygame.mixer.music.play(-1)
        self.shoot_sound = pygame.mixer.Sound('images/shooting_sound.mp3')  # Âm thanh khi bắn
        self.explosion_sound = pygame.mixer.Sound('images/explosion_sound.wav')  # Âm thanh khi nổ
        self.lose_sound = pygame.mixer.Sound('images/lose.mp3')
        self.shoot_sound.set_volume(0.2)  # Điều chỉnh âm lượng
        self.explosion_sound.set_volume(0.5)

    def load_background_frames(self, frame_files):
        """Tải các frame nền từ một danh sách các đường dẫn file."""
        for file_path in frame_files:
            frame = pygame.image.load(file_path).convert()
            frame = pygame.transform.scale(frame, (self.settings.screen_width, self.settings.screen_height))
            self.bg_frames.append(frame)

    def show_start_screen(self):
        """Hiển thị màn hình bắt đầu."""
        self.screen.blit(self.start_screen_image, (0, 0))  # Nền màu đen
        font = pygame.font.Font(None, 74)  # Font chữ lớn
        title_text = font.render("SPACE WASTE INVADERS", True, (255, 255, 255))  # Tiêu đề trò chơi
        title_rect = title_text.get_rect(center=(self.settings.screen_width // 2, self.settings.screen_height // 3))
        self.screen.blit(title_text, title_rect)  # Vẽ tiêu đề

        # Thêm hướng dẫn nhấn phím SPACE để bắt đầu
        font = pygame.font.Font(None, 36)
        instructions_text = font.render("Press SPACE to start the game", True, (255, 255, 255))
        instructions_rect = instructions_text.get_rect(center=(self.settings.screen_width // 2, self.settings.screen_height // 2))
        self.screen.blit(instructions_text, instructions_rect)

        pygame.display.flip()  # Cập nhật màn hình

    def show_instruction_screen(self):
        """Hiển thị màn hình hướng dẫn chơi game."""
        self.screen.blit(self.bg_frames[self.current_bg_frame],(0, 0))  # Màu nền đen

        # Tiêu đề hướng dẫn
        font_title = pygame.font.Font(None, 74)
        title_text = font_title.render("How to Play", True, (255, 0, 0))
        title_rect = title_text.get_rect(center=(self.settings.screen_width // 2, self.settings.screen_height // 4))
        self.screen.blit(title_text, title_rect)

        # Nội dung hướng dẫn
        font_content = pygame.font.Font(None, 36)
        instructions = [
            "Use LEFT/RIGHT ARROW KEYS to move the ship.",
            "Press SPACE to shoot.",
            "Avoid colliding with trash.",
            "Destroy all trash to advance to the next level.",
            "Press ENTER to start the game."
        ]

        y_offset = self.settings.screen_height // 3
        for line in instructions:
            text = font_content.render(line, True, (255, 0, 0))
            text_rect = text.get_rect(center=(self.settings.screen_width // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 50  # Khoảng cách giữa các dòng

        pygame.display.flip()  # Cập nhật màn hình

    def show_game_over_screen(self):
        """Hiển thị màn hình thua"""
        self.lose_sound.play(loops=0)
        self.screen.fill((0, 0, 0))  # Màu nền đen
        font = pygame.font.Font(None, 74)  # Font chữ lớn
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))  # Dòng chữ Game Over
        game_over_rect = game_over_text.get_rect(center=(self.settings.screen_width // 2, self.settings.screen_height // 3))
        self.screen.blit(game_over_text, game_over_rect)  # Hiển thị dòng chữ Game Over

        # Hướng dẫn chơi lại hoặc thoát game
        font_small = pygame.font.Font(None, 36)
        instructions_text = font_small.render("Press R to restart or ESC to quit", True, (255, 255, 255))
        instructions_rect = instructions_text.get_rect(center=(self.settings.screen_width // 2, self.settings.screen_height // 2))
        self.screen.blit(instructions_text, instructions_rect)

        pygame.display.flip()

    def checkevents_instruction_screen(self):
        """Xử lý sự kiện trong màn hình hướng dẫn."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Nhấn phím ENTER để bắt đầu chơi
                    self.instruction_screen_active = False
                    self.game_active = True
                    pygame.mouse.set_visible(False)

    def checkevents_start_screen(self):
        """Xử lý sự kiện trong màn hình bắt đầu."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Nhấn phím SPACE để vào màn hình hướng dẫn
                    self.start_screen_active = False
                    self.instruction_screen_active = True

    def checkevents_game_over(self):
        """Xử lý sự kiện trên màn hình Game Over"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Nhấn R để chơi lại
                    self.reset_game()
                elif event.key == pygame.K_ESCAPE:  # Nhấn ESC để thoát
                    pygame.quit()
                    sys.exit()

    def reset_game(self):
        """Khởi động lại trò chơi"""
        self.stats.reset_stats()  # Reset thống kê game (mạng, điểm, cấp độ)
        self.settings.initialize_dynamic_settings()  # Reset các cài đặt động
        self.bullets.empty()  # Xóa tất cả đạn
        self.aliens.empty()  # Xóa tất cả alien

        self.createfleet()  # Tạo lại đội hình alien
        self.ship.center_ship()  # Đưa tàu về vị trí giữa

        self.sb.reset_score()  # Reset lại các giá trị trên ScoreBoard
        self.game_active = True  # Bật trạng thái chơi game
        self.game_over = False  # Tắt trạng thái game over
        pygame.mouse.set_visible(False)

    def run_game(self):
        while True:
            if self.start_screen_active:
                self.show_start_screen()
                self.checkevents_start_screen()
            elif self.instruction_screen_active:
                self.show_instruction_screen()
                self.checkevents_instruction_screen()
            elif self.game_over:  # Kiểm tra trạng thái Game Over
                self.show_game_over_screen()
                self.checkevents_game_over()
            else:
                self.checkevents()  # Kiểm tra các sự kiện
                if self.game_active:
                    self.ship.update()
                    self.updatebullets()
                    self.updatealiens()
                    self.bullets_and_aliens_collide()
                self.updatescreen()  # Cập nhật các sự kiện trên màn hình
            self.clock.tick(120)    #cài đặt số tick mặc định
            
    def createfleet(self):
        alien = Alien(self)
        self.aliens.add(alien)
        alien_width, alien_height = alien.rect.size
        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 9 * alien_height):
            while current_x < (self.settings.screen_width - 1.5 * alien_width):
                self.createalien(current_x, current_y)
                current_x += 1.5 * alien_width
            current_x = alien_width
            current_y += 1.5 * alien_height

    def createalien(self, xposition,yposition):
        new_alien = Alien(self)
        new_alien.x = xposition
        new_alien.rect.x = xposition
        new_alien.rect.y = yposition
        self.aliens.add(new_alien)
        
    def checkfleetedges(self):
        for alien in self.aliens.sprites():
            if alien.checkedges():
                self.change_fleet_direction()
                break
    
    def change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    
    def shiphit(self):
        # collisions = pygame.sprite.groupcollide(self.ship, self.aliens, True, True)
        # if collisions:
            if self.stats.ship_left > 0:
                self.stats.ship_left -= 1
                self.bullets.empty()
                self.aliens.empty()
                self.createfleet()
                self.sb.prep_ships()
                self.ship.center_ship()
                sleep(0.5)
            else:
                self.game_active = False
                self.game_over = True
                pygame.mouse.set_visible(True)
    
    def aliens_hit_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self.shiphit()
                break

    def updatealiens(self):
        self.checkfleetedges()
        for alien in self.aliens.sprites():
            alien.update()  # Cập nhật vị trí và trạng thái nổ của alien
        self.aliens_hit_bottom()
    
    def checkevents(self):
        '''Kiểm tra khi các sự kiện diễn ra'''       
        for event in pygame.event.get():    #Tạo vòng lập các event khi chạy game 
            #Điều kiện để thoát game
            if event.type == pygame.QUIT:#sys.exit()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self.check_keyup_events(event)
    
    def check_keydown_events(self,event):
        '''Phản ứng khi ấn phím'''
        if event.key == pygame.K_RIGHT:   #tàu di chuyển qua phải
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self.firebullet()

    def check_keyup_events(self,event):
        '''Phản ứng khi nhả phím'''            
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
    
    def firebullet(self):
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullets(self)
            self.bullets.add(new_bullet)
            self.shoot_sound.play()
    
    def updatebullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
    
    def bullets_and_aliens_collide(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, False)
        if not self.aliens:
            self.bullets.empty()
            self.stats.level += 1
            self.createfleet()
            self.settings.increase_speed()
            self.sb.prep_ships()
            self.sb.prep_level()
             
        elif collisions:
            for aliens in collisions.values():
                for alien in aliens:
                    alien.take_damage()
                    self.explosion_sound.play()
                    self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.prep_high_score()
   
    def updatescreen(self):
        '''Cập nhật màn hình khi có các sự kiện diễn ra'''
        self.screen.blit(self.bg_frames[self.current_bg_frame], (0, 0))
        self.current_bg_frame = (self.current_bg_frame + 1) % len(self.bg_frames)
      
        for bullet in self.bullets.sprites():
            bullet.drawbullet()
        self.ship.displayship() #xuất ảnh ship lên ra màn hình
        for alien in self.aliens.sprites():
            alien.draw()
        self.sb.show_score()
        pygame.display.flip()   #màn hình game luôn được đưa lên đầu khi chạy
        
if __name__ =='__main__':
    mygame = AlienIvasion()
    mygame.run_game()
