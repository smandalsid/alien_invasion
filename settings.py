class Settings():
    def __init__(self):
        #screen settings
        self.screen_width=1200
        self.screen_height=650
        self.bg_color=(230,230,230)
        #ship settings
        self.ship_limit=3
        #bullet settings
        self.bullet_width=3
        self.bullet_height=15
        self.bullet_color=(255,153,0)
        #self.bullets_allowed=3
        #alien settings
        self.fleet_drop_speed=20
        self.speedup_scale=1.1
        self.score_scale=1.5
        self.initialise_dynamic_settings()
        #scoring
        self.alien_points=50

    def initialise_dynamic_settings(self):
        self.ship_speed_factor=1.5
        self.bullet_speed_factor=3
        self.alien_speed_factor=1
        self.fleet_direction=1

    def increase_speed(self):
        self.ship_speed_factor*=self.speedup_scale
        self.bullet_speed_factor*=self.speedup_scale
        self.alien_speed_factor*=self.speedup_scale
        self.alien_points=int(self.alien_points*self.score_scale)