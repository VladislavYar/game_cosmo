

class Score():
    """Класс, который выводит информацию."""

    def __init__(self, ai_game):
        """Инициализация атрибутов подсчёта очков."""
        self.screen = ai_game.screen
        self.ai_game = ai_game
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
