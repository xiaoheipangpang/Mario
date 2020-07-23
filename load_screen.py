import pygame
from SUPERMARIO.source.components import info
from SUPERMARIO.source import tools
from SUPERMARIO.source import constant as c
class Load_screen:
    def start(self,game_info):
        self.game_info = game_info
        self.finished = False
        self.next = 'level'
        self.timer = 0
        self.Duration = 2000
        self.info = info.Info('load_screen',self.game_info)
        self.player()
        self.info.start(self.game_info)
    def player(self):
        self.play = tools.load_image(
            'C:\\Users\\86180\\PycharmProjects\\untitled5\\SUPERMARIO\\resources\\graphics\\mario_bros.png'
            , 178, 32, 12, 16, (0, 0, 0), c.PLAYER_SCALE)
    def update(self,surface,keys):
        self.draw(surface)
        self.current_time = pygame.time.get_ticks()
        if self.timer == 0:
            self.timer = self.current_time
        if self.current_time - self.timer > self.Duration:
            self.timer = 0
            self.finished = True

    def draw(self,surface):
        surface.fill((0,0,0))
        self.info.update(surface,)
        self.info.draw(surface,)
        surface.blit(self.play, (300, 270))
class GameOver(Load_screen):
    def start(self,game_info):
        self.game_info = game_info
        self.finished = False
        self.next = 'main_menu'
        self.info = info.Info('game_over',self.game_info)
        self.Duration = 4000
        self.timer = 0
    def draw(self,surface):
        surface.fill((0,0,0))
        self.info.update(surface)
        self.info.draw(surface)
