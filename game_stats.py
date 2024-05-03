class GameStats:
    """Sigue las estadisticas de Alien Invasion"""
    def __init__(self, ai_game):
        """Inicializa las estadisticas"""
        self.settings = ai_game.settings
        self.reset_stats()

    def reset_stats(self):
        """Inicializa las estadisticas que pueden cambiar duramte el juego"""
        self.ships_left = self.settings.ship_limit
