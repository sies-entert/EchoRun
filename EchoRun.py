import pygame
from settings import Config
from menu import Menu
from gameplay import Game

def main():
    pygame.init()
    
    config = Config()
    screen_size = config.settings["resolution"][config.settings["current_resolution"]]

    screen = pygame.display.set_mode(tuple(screen_size), pygame.RESIZABLE)

    menu = Menu(screen)
    game = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        if menu.gomenu:
            menu.main_menu()
        elif menu.gosettings:
            menu.settings_menu()
        elif menu.gomusic:
            menu.music_menu()
            if menu.selected_music: 
                game = Game(screen, config, menu.selected_music)
                menu.selected_music = None 

        if game and game.gogame:
            game.run()

        pygame.display.flip()

if __name__ == "__main__":
    main()