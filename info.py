import pygame
from SUPERMARIO.source import constant as c
from SUPERMARIO.source.components import coin
pygame.font.init()
class Info:
    def __init__(self,state,game_info):
        self.state = state
        self.flash_coin = coin.Flashcoin(280,58)
        self.state_label = []
        self.info_label = []

    def start(self,game_info):
        self.game_info = game_info
        self.creat_info_labels()
        self.creat_state_labels()

    def creat_info_labels(self):

        if self.state == 'main_menu':
            self.state_label.append((self.creat_labels('1 PLAYER GAME'),(272,360)))
            self.state_label.append((self.creat_labels('2 PLAYER GAME'), (272,405)))
            self.state_label.append((self.creat_labels('TOP -'), (310,450)))
            self.state_label.append((self.creat_labels('000000'), (420,450)))
        elif self.state == 'load_screen':
            self.state_label.append((self.creat_labels('WORLD',),(280,220)))
            self.state_label.append((self.creat_labels('1 - 1',), (430,220)))
            self.state_label.append((self.creat_labels('X   {}'.format(self.game_info['lives']),30), (380,280)))
        elif self.state == 'level':
            pass
        elif self.state == 'game_over':
            self.state_label.append((self.creat_labels('GAME OVER',30),(300,280)))


    def creat_state_labels(self):

        self.info_label.append((self.creat_labels('MARIO'), (75,30)))
        self.info_label.append((self.creat_labels('WORLD'), (450,30)))
        self.info_label.append((self.creat_labels('TIME'), (625, 30)))
        self.info_label.append((self.creat_labels('000000'), (75, 55)))
        self.info_label.append((self.creat_labels('X   {}'.format(self.game_info['coin'])), (300, 55)))
        self.info_label.append((self.creat_labels('1 - 1'), (480, 55)))


    def creat_labels(self,label,size = 40,width_scale = 1.25,height_scale = 1):
        font = pygame.font.SysFont(c.Font,size)
        label_image = font.render(label,1,(255,255,255))#把文字渲染成图片，1抗锯齿
        m = label_image.get_rect()
        label_image = pygame.transform.scale(label_image,(int(m.width*width_scale),
                                                          int(m.height*height_scale)))
        return label_image
    def draw(self,surface):
        for label in self.state_label:
            surface.blit(label[0],label[1])
        for labels in self.info_label:
            surface.blit(labels[0],labels[1])
        surface.blit(self.flash_coin.image,self.flash_coin.rect)#画出金币
    def update(self,surface):
        self.flash_coin.update()


