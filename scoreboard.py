import pygame.font

class Scoreboard:
    """Una clase para dar informacion de la puntuacion"""

    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        #configuracion de fuente para la informacion de lapuntuacion
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        



      #Prepara la imagen de la puntuacion Inicial.
        self.prep_score()
        self.prep_high_score()


    def prep_score(self):
        """Convierte la puntuacion en una imagen renderizada"""
        rounded_score = round(self.stats.score, -1)
        score_str ="{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True,self.text_color, self.settings.bg_color)

        #muestra la puntuacion en la parte superior derecha de la pantalla
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """Dibuja la puntuacion en la pantalla"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)

    def prep_high_score(self):
        """Convierte la puntuacion mas alta en una imagen renderizada"""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

        #centra la puntuacion mas alta en la parte superior de la pantalla
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        """COmprueba si hay una nueva puntuacion mas alta"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
