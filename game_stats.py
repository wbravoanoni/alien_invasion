class GameStats:
    """Sigue las estadisticas de Alien Invasion"""
    def __init__(self, ai_game):
        """Inicializa las estadisticas"""
        self.settings = ai_game.settings
        self.reset_stats()

        #inicia alien Invasion en estado inactivo
        self.game_active = False

        #la puntuacion más alta no deberia restablecerse nunca.
        self.high_score = 0

    def reset_stats(self):
        """Inicializa las estadisticas que pueden cambiar duramte el juego"""
        self.ships_left = self.settings.ship_limit
        self.score = 0

