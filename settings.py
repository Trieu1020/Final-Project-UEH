import screeninfo

class Settings:
    
    def __init__(self):
        '''Dựng settings của game'''
        screen = screeninfo.get_monitors()[0]   #lấy thông tin cấu hình của người dùng
        self.screen_height = screen.height  
        self.screen_width = screen.width
        self.bg_color = (25,0,51)   

        self.ship_speed = 2
        self.ship_limit = 3

        self.bullet_speed = 6
        self.bullet_height = 15
        self.bullet_width = 5
        self.bullet_color = (255,153,51)
        self.bullet_allowed = 7

        self.alien_speed = 1.5
        self.fleet_drop_speed = 20
        self.fleet_direction = 1

        self.alien_score = 50

        self.speedup_scale = 1.5
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 2
        self.alien_speed = 1
        self.bullet_speed = 3
        self.fleet_direction = 1
        self.alien_points = 50

    def increase_speed(self):
        self.ship_speed += self.speedup_scale
        self.alien_speed += self.speedup_scale
        self.bullet_speed += self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)