import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group 
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard

def run_game():
    pygame.init()
    ai_sets=Settings()
    screen=pygame.display.set_mode((ai_sets.screen_width,ai_sets.screen_height))
    pygame.display.set_caption("Alien Invasion")
    play_button=Button(ai_sets,screen,"Play")
    ship=Ship(ai_sets,screen)
    bullets=Group()
    aliens=Group()
    gf.create_fleet(ai_sets,screen,ship,aliens)
    stats=GameStats(ai_sets)
    sb=ScoreBoard(ai_sets,screen,stats)
    while True:
        gf.check_events(ai_sets,screen,stats,sb,play_button,ship,aliens,bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_sets,screen,stats,sb,ship,aliens,bullets) 
            gf.update_aliens(ai_sets,screen,stats,sb,ship,aliens,bullets)
        gf.update_screen(ai_sets,screen,stats,sb,ship,bullets,aliens,play_button)

run_game()