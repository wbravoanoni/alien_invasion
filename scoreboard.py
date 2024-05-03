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


    def prep_score(self):
        """Convierte la puntuacion en una imagen renderizada"""
        score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True,self.text_color, self.settings.bg_color)

        #muestra la puntuacion en la parte superior derecha de la pantalla
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """Dibuja la puntuacion en la pantalla"""
        self.screen.blit(self.score_image, self.score_rect)