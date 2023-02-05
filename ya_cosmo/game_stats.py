import json


class GameStats():
    """Отслеживание статистики для игры YaCosmo."""

    def __init__(self, ai_game):
        """Инициализирует статитстику."""
        self.settings = ai_game.settings
        self.reset_stats()

        # загрузка рекорда
        try:
            with open('data/record_score.json', 'r') as record_score:
                record_score = json.loads(record_score.read())
                if record_score:
                    self.high_score = max(record_score.values())
                else:
                    self.high_score = 0

        except FileNotFoundError:
            with open('data/record_score.json', 'w') as record_score:
                record_score_dump = {}
                json.dump(record_score_dump, record_score)
                self.high_score = 0

        # игра запускается в неактивном состоянии
        self.game_active = False

    def reset_stats(self):
        """Инициализирует статистику, изменяющуюся в ходе игры."""
        self.score = 0
        self.level = 1

    def save_record(self, player):
        """Сохранение рекорда."""
        if player:
            with open('data/record_score.json', 'r') as record_score:
                record_score = json.loads(record_score.read())
                if player in record_score:
                    old_score = record_score[player]
                    if old_score < self.score:
                        record_score[player] = self.score
                else:
                    record_score[player] = self.score

            with open('data/record_score.json', 'w') as record_score_dump:
                json.dump(record_score, record_score_dump)

    def read_record(self):
        """Загрузка и сортировка таблицы очков."""
        sorted_record_score = {}
        names = []
        score = []
        names_score = []
        with open('data/record_score.json', 'r') as record_score:
            record_score = json.loads(record_score.read())
            for key in sorted(record_score, key=record_score.get,
                              reverse=True):
                sorted_record_score[key] = record_score[key]

        for name, record in sorted_record_score.items():
            names.append(name)
            score.append(record)

        names_score.append(names)
        names_score.append(score)
        return names_score
