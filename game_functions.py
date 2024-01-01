import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien

def check_keydown_events(event, ship, ai_settings, screen, bullets):
    if event.key == pygame.K_RIGHT:
        #move the ship to right/left.
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
        
def check_keyup_events(event,ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings,screen,stats, sb, play_button, ship, aliens, bullets):
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                check_keydown_events(event,ship,ai_settings,screen,bullets)
            elif event.type == pygame.KEYUP:
                check_keyup_events(event,ship)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x,mouse_y = pygame.mouse.get_pos()
                check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)
                
def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    # start a new game when the player clicks on "play" button
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        # reset game settings
        ai_settings.initialize_dynamic_settings()
        # hide the mouse cursor
        pygame.mouse.set_visible(False)
        # reset game statistics
        stats.reset_stats()
        stats.game_active = True
        
        # reset the scoreboard images.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()
    
def fire_bullet(ai_settings, screen, ship, bullets):
    # fire a bullet if limit is not reached yet.
    #create a new bullet and add it to the bullets group
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings,screen,ship)
        bullets.add(new_bullet)

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    # redraw screen during each pass through the loop.
    screen.fill(ai_settings.bg_color)
    #redraw all bullets behind ship and aliens.
    for each_bullet in bullets.sprites():
        each_bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    # draw the score information.
    sb.show_score()
    #draw the play button when the game is not active
    if not stats.game_active:
        play_button.draw_button()        
    # make the most recently drawn screen visible.
    pygame.display.flip()
    
def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats,sb)
        
    if len(aliens) == 0:
        # destroy existing bullets and create new fleet and new level.
        bullets.empty()
        ai_settings.increase_speed()
        
        #increse level.
        stats.level += 1
        sb.prep_level()
        
        create_fleet(ai_settings, screen, ship, aliens)

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    #update bullet positions
    bullets.update()
    #get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)    
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)
    
def get_number_aliens_x(ai_settings, alien_width):
    #determine the number of aliens that fit in a row.
    available_space_x = ai_settings.screen_width - (2 * alien_width)
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y/(2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    # create an alien and place it in a row.
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + (2 * alien_width * alien_number)
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + (2 * alien.rect.height * row_number)
    aliens.add(alien)
    
def create_fleet(ai_settings, screen, ship, aliens):
    #create the full fleet of aliens.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    #create the fleet of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)
        
def change_fleet_direction(ai_settings,aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
    
def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def check_aliens_bottom(ai_settings,stats,ship, screen, sb, aliens, bullets):
    # to check if any alien have reached the bottom of the screen.
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings,stats, screen,ship, sb, aliens, bullets)
            break

def update_aliens(ai_settings,stats, sb, screen,ship,aliens, bullets):
    # check if the fleet is at the edge, and then update the positions of all the aliens.
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    # looking for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings, stats, sb, screen, ship,aliens,bullets)
    # looking for aliens hittng the bottom of the screen.
    check_aliens_bottom(ai_settings,stats, screen, sb, ship,aliens, bullets)
    
def ship_hit(ai_settings, stats, screen, sb, ship,aliens,bullets):
    if stats.ship_left > 0:
        # decrement ships left
        stats.ship_left -= 1
        # update the scoreboard.
        sb.prep_ships()
        
        aliens.empty()
        bullets.empty()
        # create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        # pause the game for a while
        sleep(1)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
        
def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()