import pygame
import os
from settings import Config

class Menu():
    def __init__(self, screen):
        pygame.init()
        self.screen = screen
        self.config = Config()
        self.gomenu = True
        self.gosettings = False
        self.gomusic = False
        self.speedmake = self.config.settings
        self.themes = self.config.settings["themes"]
        self.theme = self.config.settings["theme"]
        self.font_size = self.config.settings["font_size"][self.config.settings["font_resolution"]]
        self.label_color = self.themes[self.theme]["FONTCOLOR"]
        self.music_files = self.load_music_files()
        self.selected_music = None
        self.high_score = self.load_high_score() 
        
    def load_high_score(self):
        if os.path.exists("highscore.txt"):
            with open("highscore.txt", "r") as f:
                return int(f.read())
        return 0

    def load_music_files(self):
        music_dir = "Music"
        if not os.path.exists(music_dir):
            os.makedirs(music_dir)
        return [f for f in os.listdir(music_dir) if f.endswith(('.mp3', '.wav'))]

    def draw_button(self, text, x, y, width, height, back, outline):
        button_font = pygame.font.Font("Fonts\Tourney-ExtraBold.ttf", int(self.font_size // 1.5))
        buttons = pygame.Rect(x, y, width, height)
        
        pygame.draw.rect(self.screen, outline, buttons.inflate(4, 4))
        pygame.draw.rect(self.screen, back, buttons)
        
        buttonlabels = button_font.render(text, True, self.label_color)
        textrect = buttonlabels.get_rect(center=buttons.center)
        self.screen.blit(buttonlabels, textrect)     
        
        return buttons  

    def draw_music_line(self, text, lx, ly, lw, lh, lback, loutline):
        music_line = pygame.Rect(lx, ly, lw, lh)
        pygame.draw.rect(self.screen, loutline, music_line.inflate(4, 4))
        pygame.draw.rect(self.screen, lback, music_line)

        font = pygame.font.Font(None, int(self.font_size // 1.5))
        label = font.render(text, True, self.label_color)
        label_rect = label.get_rect(center=music_line.center)
        self.screen.blit(label, label_rect)

        return music_line

    def main_menu(self):
        screen_color = self.themes[self.theme]["SCREENBACKGROUND"]
        bu_out = self.themes[self.theme]["BUTTONOUTLINE"]
        bu_back = self.themes[self.theme]["BUTTONBACK"]
        self.screen.fill(screen_color)

        gamename_font = pygame.font.Font("Fonts\Tourney-Regular.ttf", int(self.font_size * 1.5))
        madeby_font = pygame.font.Font("Fonts\Tourney-Black.ttf", int(self.font_size // 1.8))
        self.screen.fill(screen_color)

        menuband_w, menuband_h = self.screen.get_width() // 4, self.screen.get_height() // 1.1
        menuband_x = self.screen.get_width() // 2 - menuband_w // 2
        menuband_y = self.screen.get_height() // 2 - menuband_h // 2

        menuband = pygame.Rect(menuband_x, menuband_y, menuband_w, menuband_h)

        pygame.draw.rect(self.screen, bu_out, menuband.inflate(4, 4))
        pygame.draw.rect(self.screen, bu_back, menuband)

        gamename = gamename_font.render("EchoRun", True, self.label_color)
        gamenamerect = gamename.get_rect(center=(menuband_x + menuband_w // 2, int(self.screen.get_height() // 6)))
        self.screen.blit(gamename, gamenamerect)

        madeby = madeby_font.render("Nazarii Kostiukovych", True, self.label_color)
        madebyrect = madeby.get_rect(center=(menuband_x + menuband_w // 2, int(self.screen.get_height() // 1.17)))
        self.screen.blit(madeby, madebyrect)

        classby = madeby_font.render("ITA 23-1", True, self.label_color)
        classbyrect = classby.get_rect(center=(menuband_x + menuband_w // 2, int(self.screen.get_height() // 1.11)))
        self.screen.blit(classby, classbyrect)

        hs_font = pygame.font.Font("Fonts\Tourney-black.ttf", int(self.font_size // 1.5))
        hs_text = hs_font.render(f"High Score: {self.high_score}", True, self.label_color)
        hs_rect = hs_text.get_rect(center=(menuband_x + menuband_w // 2, int(self.screen.get_height() // 2.5)))
        self.screen.blit(hs_text, hs_rect)

        bu_w, bu_h = self.speedmake["button_size"][self.speedmake["button_WuH"]]
        bu_x = self.screen.get_width() // 2 - bu_w // 2
        bu_y = self.screen.get_height() // 2 - bu_h // 2
        bu_space = 30

        st_button = self.draw_button("Start", bu_x, bu_y, bu_w, bu_h, bu_back, bu_out)
        set_button = self.draw_button("Settings", bu_x, bu_y + bu_space * 3, bu_w, bu_h, bu_back, bu_out)
        ex_button = self.draw_button("Exit", bu_x, bu_y + bu_space * 6, bu_w, bu_h, bu_back, bu_out)

        pygame.display.flip()

        while self.gomenu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if st_button.collidepoint(event.pos):
                        self.gomenu = False
                        self.gomusic = True
                    elif set_button.collidepoint(event.pos):
                        self.gomenu = False
                        self.gosettings = True
                        return "settings"
                    elif ex_button.collidepoint(event.pos):
                        pygame.quit()
                        return

            pygame.display.flip()

    def settings_menu(self):
        menu_color = self.themes[self.theme]["MENUBACKGROUND"]
        screen_color = self.themes[self.theme]["SCREENBACKGROUND"]
        bu_out = self.themes[self.theme]["BUTTONOUTLINE"]
        bu_back = self.themes[self.theme]["BUTTONBACK"]    
        self.screen.fill(screen_color)

        setrect_w, setrect_h = self.screen.get_width() // 1.6, self.screen.get_height()
        setrect_x = self.screen.get_width() // 4 - setrect_w // 4
        setrect_y = self.screen.get_height() // 2 - setrect_h // 1.5

        setrect = pygame.Rect(setrect_x, setrect_y, setrect_w, setrect_h)

        pygame.draw.rect(self.screen, bu_out, setrect.inflate(4, 4))
        pygame.draw.rect(self.screen, menu_color, setrect)

        bu_w, bu_h = self.speedmake["button_size"][self.speedmake["button_WuH"]]
        bu_x = self.screen.get_width() // 4 - bu_w // 2
        bu_y = self.screen.get_height() // 7 - bu_h // 2
        bu_space = 80

        conf_font = pygame.font.Font("Fonts\Tourney-Black.ttf", int(self.font_size // 1.8))

        def draw_current_settings():
            cur_res = self.speedmake["current_resolution"]
            cur_theme = self.speedmake["theme"]

            res_text = f" {cur_res}"
            theme_text = f" {cur_theme}"

            res_label = conf_font.render(res_text, True, self.label_color)
            theme_label = conf_font.render(theme_text, True, self.label_color)

            self.screen.blit(res_label, (bu_x + bu_space * 5, bu_y + bu_space // 1.6))
            self.screen.blit(theme_label, (bu_x + bu_space * 5, bu_y + bu_space * 3.4))

        draw_current_settings()

        res_button = self.draw_button("Resolution", bu_x, bu_y + bu_space // 3, bu_w, bu_h, bu_back, bu_out)
        th_button = self.draw_button("Thema", bu_x, bu_y + bu_space * 3, bu_w, bu_h, bu_back, bu_out)
        bam_button = self.draw_button("Zurück", self.screen.get_width() // 1.3, bu_y, bu_w, bu_h, bu_back, bu_out)

        while self.gosettings:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if res_button.collidepoint(event.pos):
                        self.change_resolution()
                        new_resolution = self.speedmake["resolution"][self.speedmake["current_resolution"]]
                        pygame.display.set_mode(tuple(new_resolution), pygame.RESIZABLE) 
                        self.settings_menu() 
                        pygame.display.flip()
                    elif th_button.collidepoint(event.pos):
                        self.change_theme()
                        self.settings_menu() 
                        draw_current_settings()
                        self.screen.fill(self.themes[self.theme]["SCREENBACKGROUND"])
                        draw_current_settings()
                        self.settings_menu() 
                        pygame.display.flip()
                    elif bam_button.collidepoint(event.pos):
                        self.gosettings = False
                        self.gomenu = True
                        return

            pygame.display.flip()

    def change_resolution(self):
        resos = list(self.speedmake["resolution"].keys())
        cur_res = self.speedmake["current_resolution"]

        new_index = (resos.index(cur_res) + 1) % len(resos)
        new_resos = resos[new_index]

        self.speedmake["current_resolution"] = new_resos
        self.speedmake["font_resolution"] = f"f{new_resos}"
        self.speedmake["button_WuH"] = f"b{new_resos}"
        self.speedmake["line_WuH"] = f"l{new_resos}" 

        self.font_size = self.speedmake["font_size"][self.speedmake["font_resolution"]]

        self.config.save_config()

        return self.speedmake["resolution"][new_resos]

    def change_theme(self):
        themes = list(self.speedmake["themes"].keys())
        current_theme = self.speedmake["theme"]
        new_index = (themes.index(current_theme) + 1) % len(themes) 
        new_theme = themes[new_index]

        self.speedmake["theme"] = new_theme
        self.theme = new_theme 
        self.label_color = self.themes[self.theme]["FONTCOLOR"] 
        self.config.save_config()

        self.screen.fill(self.themes[self.theme]["SCREENBACKGROUND"]) 

    def music_menu(self):
        screen_color = self.themes[self.theme]["SCREENBACKGROUND"]
        bu_out = self.themes[self.theme]["BUTTONOUTLINE"]
        bu_back = self.themes[self.theme]["BUTTONBACK"]
        self.screen.fill(screen_color)

        line_w, line_h = self.speedmake["line_size"][self.speedmake["line_WuH"]]

        start_x = self.screen.get_width() // 2 - line_w // 2
        start_y = self.screen.get_height() // 4
        line_spacing = 20

        music_lines = []
        for i, music_file in enumerate(self.music_files):
            line_y = start_y + (line_h + line_spacing) * i
            music_line = self.draw_music_line(music_file, start_x, line_y, line_w, line_h, bu_back, bu_out)
            music_lines.append((music_line, music_file))

        back_button = self.draw_button("Zurück", start_x, self.screen.get_height() - line_h * 3 , line_w, line_h, bu_back, bu_out)

        while self.gomusic:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for music_line, music_file in music_lines:
                        if music_line.collidepoint(event.pos):
                            self.selected_music = music_file
                            self.gomusic = False
                            self.gogame = True 
                            return

                    if back_button.collidepoint(event.pos):
                        self.gomusic = False
                        self.gomenu = True
                        return

                if event.type == pygame.MOUSEMOTION:
                    for music_line, music_file in music_lines:
                        if music_line.collidepoint(event.pos):
                            play_button = self.draw_button("Play", music_line.x + music_line.width + 10, music_line.y, 100, line_h, bu_back, bu_out)
                            pygame.display.flip()
                        elif not music_line.collidepoint(event.pos):
                            play_button = None
                            pygame.display.flip()
                        

            pygame.display.flip()