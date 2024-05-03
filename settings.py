class Settings:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230,230)
        self.ship_speed = 1.5
        self.ship_limit = 3
        #configuracion de las balas
        self.bullet_speed = 1.5
        self.bullet_width = 300
        self.bullet_height = 15
        self.bullet_color= (60, 60 , 60)
        self.bullets_allowed = 10
        self.alien_speed = 2.0
        self.fleet_drop_speed = 10
        #fleet_direction de 1 representa derecha; -1 representa izquiera
        self.fleet_direction = 1
        
