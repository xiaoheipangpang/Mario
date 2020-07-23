import pygame
from SUPERMARIO.source import tools
from SUPERMARIO.source import constant as c
from SUPERMARIO.source.components import info
class Window:
    def __init__(self):
        game_info = {
            'score' : 0,
            'coin' : 0,
            'lives' : 3,
            'play_state' : 'small'
        }
        self.start(game_info)
    def start(self,game_info):
        self.game_info = game_info
        self.setup_background()#初始化背景
        self.setup_player()#调用自己的功能，初始化执行这些功能
        self.setup_cursor()
        self.info = info.Info('main_menu',self.game_info)#文字类实例化，最初执行好了下面不需要再调用
        self.finished = False
        self.next = 'load_screen'
        self.info.start(self.game_info)

    def setup_background(self):
        self.BG = pygame.image.load('C:\\Users\\86180\\PycharmProjects\\untitled5\\SUPERMARIO\\resources\\graphics\\level_1.png')
        w,h = self.BG.get_size()
        self.BG = pygame.transform.scale(self.BG, (int(w * c.BG_scale), int(h * c.BG_scale)))
        self.view = tools.load_image('C:\\Users\\86180\\PycharmProjects\\untitled5\\SUPERMARIO\\resources\\graphics\\title_screen.png'
                           , 1,60, 176, 88, (225,0,220),c.BG_scale)
    def setup_player(self):
        self.player = tools.load_image('C:\\Users\\86180\\PycharmProjects\\untitled5\\SUPERMARIO\\resources\\graphics\\mario_bros.png'
            , 178, 32, 12, 16, (0, 0, 0), c.PLAYER_SCALE)
    def setup_cursor(self):
        self.cursor =pygame.sprite.Sprite()
        self.cursor.image = tools.load_image('C:\\Users\\86180\\PycharmProjects\\untitled5\\SUPERMARIO\\resources\\graphics\\item_objects.png'
            , 25, 160, 8, 8, (0, 0, 0), c.PLAYER_SCALE)
        rect = self.cursor.image.get_rect()#获取rect
        rect.x,rect.y = (220,360)
        self.cursor.rect = rect
        self.cursor.state = '1 P'#状态机
    def update_cursor(self,keys):
         if keys[pygame.K_UP]:
             self.cursor.state = '1 P'
             self.cursor.rect.y =360
         elif  keys[pygame.K_DOWN]:
             self.cursor.state = '2 P'
             self.cursor.rect.y =405
         elif keys[pygame.K_RETURN]:#小键盘的回车是enter
            self.reset_game_info()
            if self.cursor.state == '1 P':
                self.finished = True
            if self.cursor.state == '2 P':
                self.finished = True


    def update(self,surface,keys):
        self.update_cursor(keys)
        surface.blit(self.BG,(0,0))
        surface.blit(self.view, (170,100))
        surface.blit(self.player, (110,490))
        surface.blit(self.cursor.image,self.cursor.rect)

        self.info.update(surface)
        self.info.draw(surface)
    def reset_game_info(self):
        self.game_info.update({
            'score':0,
            'coin':0,
            'lives':3,
            'player_state':'small'
            })

