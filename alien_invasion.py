import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button     
from ship import Ship
from alien import Alien
import game_functions as gf
from pygame.sprite import Group

def run_game():
    # initialize the game.
    pygame.init()
    ai_settings = Settings()
    # i will create a screen object.
    # 1200 pixels X 800 pixels window.
    screen =  pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    
    # make the play button
    play_button = Button(ai_settings, screen, "PLAY")
    
    # create an instance to store game statstics and create a scoreboard.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    
    #setting background color
    bg_color = (230,230,230)
    
    # make a ship
    ship = Ship(ai_settings,screen)
    # make a group which store bullets inside it.
    bullets = Group()
    # make a group which store aliens inside it.
    aliens = Group()
    
    # creating a bunch of aliens on the screen
    gf.create_fleet(ai_settings,screen, ship, aliens)
    
    # main loop
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
        
        if stats.game_active:   
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)
          

run_game()
