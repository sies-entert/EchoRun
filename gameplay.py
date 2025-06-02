import pygame
import time
import os
import random
import pygame.mixer
from menu import Menu

class Game():
    def __init__(self, screen, config, music_file):
        self.screen = screen
        self.config = config
        self.gogame = True
        self.player_pos = [self.screen.get_width() // 2, int(self.screen.get_height() // 1.7)]
        self.walls = []
        self.score = 0
        self.charge = 0
        self.max_charge = 100 
        self.paused = False 
        self.player_radius = 15  
        self.wall_speed = 5  
        self.wall_width = 100 
        self.wall_height = 20  
        self.gap = 50  
        self.spawn_rate = 1000 
        self.last_spawn = pygame.time.get_ticks() 
        self.flash_alpha = 0    
        self.wall_outline_alpha = 255 
        self.music_file = music_file 
        self.load_music()

    def load_music(self):

        pygame.mixer.music.load(os.path.join("Music", self.music_file))
        pygame.mixer.music.play(-1) 

    def save_high_score(self):
        high_score = self.load_high_score()
        if self.score > high_score:
            with open("highscore.txt", "w") as f:
                f.write(str(self.score))

    def load_high_score(self):
        if os.path.exists("highscore.txt"):
            with open("highscore.txt", "r") as f:
                return int(f.read())
        return 0

    def spawn_wall(self):
        player_x = self.player_pos[0]
        min_x = max(0, player_x - self.wall_width * 2) 
        max_x = min(self.screen.get_width() - self.wall_width * 3 - self.gap * 2, player_x + self.wall_width * 2) 

        wall_x = random.randint(min_x, max_x) 
        for i in range(3):
            self.walls.append(pygame.Rect(wall_x, -self.wall_height, self.wall_width, self.wall_height))
            wall_x += self.wall_width + self.gap

    def update(self):
        if self.paused:
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn > self.spawn_rate:
            self.spawn_wall()
            self.last_spawn = current_time

        for wall in self.walls:
            wall.y += self.wall_speed
            if wall.y > self.screen.get_height():
                self.walls.remove(wall)
                self.score += 1
                self.charge += 10  
                if self.charge > self.max_charge:
                    self.charge = self.max_charge

        if self.score % 10 == 0 and self.score > 0:
            self.wall_speed += 0.5 
            self.spawn_rate = max(500, self.spawn_rate - 50) 
        player_rect = pygame.Rect(self.player_pos[0] - self.player_radius, self.player_pos[1] - self.player_radius,
                                  self.player_radius * 2, self.player_radius * 2)
        for wall in self.walls:
            if player_rect.colliderect(wall):
                self.game_over()

        if self.wall_outline_alpha > 100:
            self.wall_outline_alpha -= 1

        if self.flash_alpha > 0:
            self.flash_alpha -= 5

    def draw(self):
        self.screen.fill((0, 0, 0)) 

        if self.flash_alpha > 0:
            flash_surface = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
            flash_surface.set_alpha(self.flash_alpha)
            flash_surface.fill((255, 255, 255))
            self.screen.blit(flash_surface, (0, 0))

        for wall in self.walls:
            pygame.draw.rect(self.screen, (0, 0, 0), wall) 
            outline_color = (255, 255, 255, self.wall_outline_alpha)  
            pygame.draw.rect(self.screen, outline_color, wall, 2)

        pygame.draw.circle(self.screen, (0, 0, 0), self.player_pos, self.player_radius) 
        pygame.draw.circle(self.screen, (255, 255, 255), self.player_pos, self.player_radius, 2) 

        font = pygame.font.Font(None, 36)
        charge_text = font.render(f"Charge: {self.charge}/{self.max_charge}", True, (255, 255, 255))
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(charge_text, (10, 10))
        self.screen.blit(score_text, (10, 50))


        if self.paused:
            pause_font = pygame.font.Font(None, 72)
            pause_text = pause_font.render("Paused", True, (255, 255, 255))
            pause_rect = pause_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
            self.screen.blit(pause_text, pause_rect)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player_pos[0] = max(self.player_radius, self.player_pos[0] - 5)
        if keys[pygame.K_RIGHT]:
            self.player_pos[0] = min(self.screen.get_width() - self.player_radius, self.player_pos[0] + 5)
        if keys[pygame.K_SPACE] and self.charge >= self.max_charge:
            self.break_wall()

        # Пауза
        if keys[pygame.K_ESCAPE]:
            self.paused = not self.paused
            if self.paused:
                pygame.mixer.music.pause() 
            else:
                pygame.mixer.music.unpause() 

    def break_wall(self):
        if self.walls:
            self.walls.pop(0)
            self.charge = 0
            self.flash_alpha = 100  
            self.wall_outline_alpha = 255  

    def game_over(self):
        self.save_high_score()  

        game_over_font = pygame.font.Font(None, 72)
        game_over_text = game_over_font.render("Game Over", True, (255, 255, 255))
        game_over_rect = game_over_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(game_over_text, game_over_rect)

        score_font = pygame.font.Font(None, 48)
        score_text = score_font.render(f"Final Score: {self.score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 50))
        self.screen.blit(score_text, score_rect)

        hint_font = pygame.font.Font(None, 36)
        hint_text = hint_font.render("Press ESC or ENTER to return to the menu", True, (255, 255, 255))
        hint_rect = hint_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 100))
        self.screen.blit(hint_text, hint_rect)

        pygame.display.flip()

        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:  # ESC или ENTER
                        waiting_for_input = False
                        self.gogame = False

    def run(self):
        clock = pygame.time.Clock()
        while self.gogame:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.save_high_score()  
                    self.gogame = False

            self.handle_input()
            self.update()
            self.draw()
            pygame.display.flip()
            clock.tick(60)