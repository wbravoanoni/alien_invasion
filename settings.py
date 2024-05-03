class Settings:
    def __init__(self):
        """Inicializa las configuraciones estaticas del juego"""
        #Configuracion de pantala
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230,230)

        #configuracion de la nave
        self.ship_limit = 3

        #configuracion de las balas
        self.bullet_width = 300
        self.bullet_height = 15
        self.bullet_color= (60, 60 , 60)
        self.bullets_allowed = 10

        #configuracion de los aliens
        self.fleet_drop_speed = 10

        #rapidez con la que se acelera el juego
        self.speedup_scale = 1.1

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Inicializa las configuraciones que cambian durante el juego"""
        self.ship_speed = 1.5
        self.bullet_speed = 1.5
        self.alien_speed = 1.0

        #fleet_direction de 1 representa derecha; -1 representa izquiera
        self.fleet_direction = 1

    def increase_speed(self):
        """Incrementa las configuraciones de velocidad"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        
