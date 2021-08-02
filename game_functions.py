import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien

def fire_bullet(ai_sets,screen,ship,bullets):
    new_bullet=Bullet(ai_sets,screen,ship)
    bullets.add(new_bullet)

def check_keydown_events(event,ai_sets,screen,ship,bullets):
    if event.key==pygame.K_RIGHT or event.key==pygame.K_d:
        ship.moving_right=True
    elif event.key==pygame.K_LEFT or event.key==pygame.K_a:
        ship.moving_left=True
    elif event.key==pygame.K_SPACE:
        fire_bullet(ai_sets,screen,ship,bullets)
    elif event.key==pygame.K_q:
        sys.exit()

def check_mousebuttondown_events(event,ai_sets,screen,stats,sb,play_button,ship,aliens,bullets):
    mouse_x,mouse_y=pygame.mouse.get_pos()
    if check_play_button(ai_sets,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y):
        stats.game_active=True
        if event.button==pygame.BUTTON_LEFT:
            fire_bullet(ai_sets,screen,ship,bullets)
    if event.button==pygame.BUTTON_LEFT:
        fire_bullet(ai_sets,screen,ship,bullets)

def check_play_button(ai_sets,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y):
    button_clicked=play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        ai_sets.initialise_dynamic_settings()
        stats.reset_stats()
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        aliens.empty()
        bullets.empty()
        create_fleet(ai_sets,screen,ship,aliens)
        ship.center_ship()
        return True

def check_keyup_events(event,ship):
    if event.key==pygame.K_RIGHT or event.key==pygame.K_d:
        ship.moving_right=False
    elif event.key==pygame.K_LEFT or event.key==pygame.K_a:
        ship.moving_left=False

def check_events(ai_sets,screen,stats,sb,play_button,ship,aliens,bullets):
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()

        elif event.type==pygame.KEYDOWN:
            check_keydown_events(event,ai_sets,screen,ship,bullets)

        elif event.type==pygame.KEYUP:
            check_keyup_events(event,ship)

        elif event.type==pygame.MOUSEBUTTONDOWN:
            check_mousebuttondown_events(event,ai_sets,screen,stats,sb,play_button,ship,aliens,bullets)

def update_screen(ai_sets,screen,stats,sb,ship,bullets,aliens,play_button):
    screen.fill(ai_sets.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()

def update_bullets(ai_sets,screen,stats,sb,ship,aliens,bullets):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom<=0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_sets,screen,stats,sb,ship,bullets,aliens)

def check_bullet_alien_collisions(ai_sets,screen,stats,sb,ship,bullets,aliens):
    collisions=pygame.sprite.groupcollide(bullets,aliens,True,True)
    if collisions:
        for aliens in collisions.values():
            stats.score+=ai_sets.alien_points*len(aliens)
            sb.prep_score()
        check_high_score(stats,sb)
    if len(aliens)==0:
        bullets.empty()
        ai_sets.increase_speed()
        stats.level+=1
        sb.prep_level()
        create_fleet(ai_sets,screen,ship,aliens)

def get_number_aliens_x(ai_sets,alien_width):
    available_space_x=ai_sets.screen_width-2*alien_width
    number_aliens_x=int(available_space_x/(2*alien_width))
    return number_aliens_x

def get_number_rows(ai_sets,ship_height,alien_height):
    available_space_y=(ai_sets.screen_height-(4*alien_height)-ship_height)
    number_rows=int(available_space_y/(2*alien_height))
    return number_rows

def create_alien(ai_sets,screen,aliens,alien_number,row_number):
    alien=Alien(ai_sets,screen)
    alien_width=alien.rect.width
    alien.x=alien_width+2*alien_width*alien_number
    alien.rect.x=alien.x
    alien.rect.y=alien.rect.height+2*alien.rect.height*row_number
    aliens.add(alien)

def create_fleet(ai_sets,screen,ship,aliens):
    alien=Alien(ai_sets,screen)
    number_aliens_x=get_number_aliens_x(ai_sets,alien.rect.width)
    number_rows=get_number_rows(ai_sets,ship.rect.height,alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_sets,screen,aliens,alien_number,row_number)

def check_fleet_edges(ai_sets,aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_sets,aliens)
            break

def change_fleet_direction(ai_sets,aliens):
    for alien in aliens.sprites():
        alien.rect.y+=ai_sets.fleet_drop_speed
    ai_sets.fleet_direction*=-1

def ship_hit(ai_sets,screen,stats,sb,ship,aliens,bullets):
    if stats.ships_left>0:
        stats.ships_left-=1
        sb.prep_ships()
        aliens.empty()
        bullets.empty()
        create_fleet(ai_sets,screen,ship,aliens)
        ship.center_ship()

        sleep(0.5)
    else:
        stats.game_active=False

def check_aliens_bottom(ai_sets,screen,stats,sb,ship,aliens,bullets):
    screen_rect=screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom>=screen_rect.bottom:
            ship_hit(ai_sets,screen,stats,sb,ship,aliens,bullets)
            break

def update_aliens(ai_sets,screen,stats,sb,ship,aliens,bullets):
    check_fleet_edges(ai_sets,aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_sets,screen,stats,sb,ship,aliens,bullets)
    check_aliens_bottom(ai_sets,screen,stats,sb,ship,aliens,bullets)

def check_high_score(stats,sb):
    if stats.score>stats.high_score:
        stats.high_score=stats.score
        sb.prep_high_score()