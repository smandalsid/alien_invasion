class GameStats():
    def __init__(self,ai_sets):
        self.ai_sets=ai_sets
        self.reset_stats()
        self.game_active=False
        self.high_score=0

    def reset_stats(self):
        self.ships_left=self.ai_sets.ship_limit
        self.score=0
        self.level=1