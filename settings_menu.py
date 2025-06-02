import json
import pygame

SETTINGS = "settings.json"

def load_settings():
    with open(SETTINGS, "r") as f:
        return json.load(f)
    
def save_settings(settings):
    with open(SETTINGS, "w") as f:
        json.dump(settings, f, indent = 4)
        
pygame.font.init()

pygame.display.set_caption("EchoRun")
settings = load_settings()

gosettings = True
gomenu = False
gogame = False

def gameconfig(config, config_key = None, theme_key = False, window_key = None):
    
    current_window_mode = config["current_window_mode"]

    if config_key:
        if config_key in config["resolution"]:
            config["current_resolution"] = config_key
            
            font_key = f"f{config_key}"
            button_key = f"b{config_key}"
                    
            if font_key in config["font_size"]:
                config["font_resolution"] = font_key
            
            if button_key in config["button_size"]:
                config["button_WuH"] = button_key
                
        new_resolution = config["resolution"][config["current_resolution"]]
        
        if current_window_mode == "fullscreen":
            pygame.display.set_mode(new_resolution, pygame.FULLSCREEN)
        elif current_window_mode == "borderless":
            pygame.display.set_mode(new_resolution, pygame.NOFRAME)
        elif current_window_mode == "windowed":
            pygame.display.set_mode(new_resolution, pygame.RESIZABLE)

        
    if theme_key:
        themes = list(config["themes"].keys())
        current_theme = themes.index(config["theme"])
        next_current_theme = (current_theme + 1) % len(themes)
        config["theme"] = themes[next_current_theme]
        
    if window_key:
        modes = list(config["window_mode"].keys())
        current_mode = modes.index(config["current_window_mode"])
        next_mode = (current_mode + 1) % len(modes)
        new_mode = modes[next_mode]
        config["current_window_mode"] = new_mode
        
        new_resolution = config["resolution"][config["current_resolution"]]
        
        if new_mode == "fullscreen":
            pygame.display.set_mode(config["resolution"][config["current_resolution"]], pygame.FULLSCREEN)
        elif new_mode == "borderless":
            pygame.display.set_mode(config["resolution"][config["current_resolution"]], pygame.NOFRAME)
        elif new_mode == "windowed":
            pygame.display.set_mode(config["resolution"][config["current_resolution"]], pygame.RESIZABLE)
            
    
    return config
        
def settings_menu(screen, config):

    global gosettings, gomenu, gogame
    
    while gosettings and not gomenu:
        theme = config["theme"]
        theme_settings = config["themes"][theme]
        SCREENBACKGROUND = theme_settings["SCREENBACKGROUND"]
        MENUBACKGROUND = theme_settings["MENUBACKGROUND"]
        FONTCOLOR = theme_settings["FONTCOLOR"]
        BUTTONBACK = theme_settings["BUTTONBACK"]
        BUTTONOUTLINE = theme_settings["BUTTONOUTLINE"]
        
        screen.fill(SCREENBACKGROUND)
        
        font_size = config["font_size"][config["font_resolution"]] 
        font = pygame.font.SysFont("comic-sans", font_size // 2)
        
        Bu_W, Bu_H = config["button_size"][config["button_WuH"]]
        
        sb_W, sb_H = screen.get_width() // 1.75, screen.get_height() // 1.5
        sb_X = screen.get_width() // 20
        sb_Y = screen.get_height() // 20
        
        pygame.draw.rect(
            screen, 
            BUTTONOUTLINE,
            pygame.Rect(sb_X - 2, sb_Y - 2, sb_W + 4, sb_H + 4)
        )
        settingsbackground = pygame.Rect(sb_X, sb_Y, sb_W, sb_H)
        pygame.draw.rect(screen, MENUBACKGROUND, settingsbackground)
        
        WmBu_W, WmBu_H = Bu_W, Bu_H
        WmBu_X = screen.get_width() // 6 + WmBu_W // 2
        WmBu_Y = screen.get_height() // 5 - WmBu_H // 2 
        
        ThBu_W, ThBu_H = Bu_W, Bu_H
        ThBu_X = screen.get_width() // 6 + ThBu_W // 2
        ThBu_Y = screen.get_height() // 2.15 - ThBu_H // 2
        
        RNBu_W, RNBu_H = Bu_W, Bu_H
        RNBu_X = screen.get_width() // 6 + RNBu_W // 2
        RNBu_Y = screen.get_height() // 3 - RNBu_H // 2
        
        BaMe_W, BaMe_H = Bu_W, Bu_H
        BaMe_X = screen.get_width() // 1.4 + BaMe_W // 2
        BaMe_Y = screen.get_height() // 5 - BaMe_H // 2
        
        AccMe_W, AccMe_H = Bu_W, Bu_H
        AccMe_X = screen.get_width() // 1.4 + AccMe_W // 2
        AccMe_Y = screen.get_height() // 3 - AccMe_H // 2
        
        pygame.draw.rect(
            screen,
            BUTTONOUTLINE,
            pygame.Rect(WmBu_X - 2, WmBu_Y - 2, WmBu_W + 4, WmBu_H + 4)
        )
        WmButton = pygame.Rect(WmBu_X, WmBu_Y, WmBu_W, WmBu_H)
        pygame.draw.rect(screen, BUTTONBACK, WmButton)
        WmText = font.render("Mode", True, FONTCOLOR)
        screen.blit(WmText, WmText.get_rect(center = WmButton.center))
        
        pygame.draw.rect(
            screen,
            BUTTONOUTLINE,
            pygame.Rect(ThBu_X - 2, ThBu_Y - 2, ThBu_W + 4, ThBu_H + 4)
        )
        ThButton = pygame.Rect(ThBu_X, ThBu_Y, ThBu_W, ThBu_H)
        pygame.draw.rect(screen, BUTTONBACK, ThButton)
        ThText = font.render("Theme", True ,FONTCOLOR)
        screen.blit(ThText, ThText.get_rect(center = ThButton.center))
        
        pygame.draw.rect(
            screen,
            BUTTONOUTLINE,
            pygame.Rect(RNBu_X - 2, RNBu_Y - 2, RNBu_W + 4, RNBu_H + 4)
        )
        RNButton = pygame.Rect(RNBu_X, RNBu_Y, RNBu_W, RNBu_H)
        pygame.draw.rect(screen, BUTTONBACK, RNButton)
        RNBText = font.render("Resolution", True ,FONTCOLOR)
        screen.blit(RNBText, RNBText.get_rect(center = RNButton.center))
        
        pygame.draw.rect(
            screen,
            BUTTONOUTLINE,
            pygame.Rect(BaMe_X - 2, BaMe_Y - 2, BaMe_W + 4, BaMe_H + 4)
        )
        BaMeButton = pygame.Rect(BaMe_X, BaMe_Y, BaMe_W, BaMe_H)
        pygame.draw.rect(screen, BUTTONBACK, BaMeButton)
        BaMeText = font.render("Back to Menu", True, FONTCOLOR)
        screen.blit(BaMeText, BaMeText.get_rect(center = BaMeButton.center))
        
        pygame.draw.rect(
            screen,
            BUTTONOUTLINE,
            pygame.Rect(AccMe_X - 2, AccMe_Y - 2, AccMe_W + 4, AccMe_H + 4)
        )
        AccButton = pygame.Rect(AccMe_X, AccMe_Y, AccMe_W, AccMe_H)
        pygame.draw.rect(screen, BUTTONBACK, AccButton)
        AccText = font.render("Accept", True, FONTCOLOR)
        screen.blit(AccText, AccText.get_rect(center = AccButton.center))
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gosettings = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if ThButton.collidepoint(event.pos):
                    config = gameconfig(config, theme_key = True)
                elif RNButton.collidepoint(event.pos):
                    resolution = list(config["resolution"].keys())
                    current_resolution = resolution.index(config["current_resolution"])
                    next_resolution = (current_resolution + 1) % len(resolution)
                    config = gameconfig(config, config_key = resolution[next_resolution])
                elif WmButton.collidepoint(event.pos):
                    config = gameconfig(config, window_key = True)
                elif AccButton.collidepoint(event.pos):
                    save_settings(settings)
                elif BaMeButton.collidepoint(event.pos):
                    gosettings = False
                    gomenu = True
        
        pygame.display.flip()
            
    return config, gomenu

if __name__ == "__main__":
    pygame.init()
    settings = load_settings()

    # Получаем текущие размеры экрана
    current_resolution = settings["resolution"][settings["current_resolution"]]
    screen = pygame.display.set_mode(current_resolution)

    # Открываем меню настроек
    settings, gomenu = settings_menu(screen, settings)

    pygame.quit()