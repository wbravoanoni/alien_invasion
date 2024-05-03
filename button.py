import pygame.font

class Button:
    def __init__(self, ai_game, msg):
        """Inicializa los atributos del boton"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        #configura las dimensiones y propiedades del boton
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        #crea el objeto rect del boton y lo centra
        self.rect = pygame.Rect(0 , 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        
        #solo hay que preparar el mensaje del botón una vez
        self._prep_msg(msg)
    
    def _prep_msg(self, msg):
        """COnvierte msg en una imagen renderizada y centra el texto en el botón"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        #dibuja un boton en blanco y luego el mensaje
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
        