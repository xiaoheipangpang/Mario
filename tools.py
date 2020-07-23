import pygame
import random
class Game:
    def __init__(self,name,state_dict,state):
        self.screen=pygame.display.get_surface()
        pygame.display.set_caption(name)
        self.clock=pygame.time.Clock()#初始化时间对象
        #三个对象Surface（窗口图像）Rect Clock时间对象
        self.keys = pygame.key.get_pressed()
        self.state_dict = state_dict
        self.state = self.state_dict[state]
    def update(self):
        if self.state.finished:
            game_info = self.state.game_info
            self.state.finished = False
            next = self.state.next
            self.state = self.state_dict[next]
            self.state.start(game_info)
        self.state.update(self.screen,self.keys)#给各个模块的更新传入参数
        pygame.display.update()
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    self.keys = pygame.key.get_pressed()#接受一个列表，按下的键的位置为1
                if event.type == pygame.KEYUP:
                    self.keys = pygame.key.get_pressed()
            self.clock.tick(60)
            self.update()
def load_image(path,x,y,width,height,colorkey,scale,rgb=(0,0,0)):
    img = pygame.Surface((width,height))#创建Surface对象与抠图对象大小相同，默认黑色
    img.fill(rgb)
    image = pygame.image.load(path)#导入大图
    img.blit(image,(0,0),(x,y,width,height))#单独把要抠图的小图放在背景上
    img.set_colorkey(colorkey)#把某种颜色的区域变透明colorkey针对colorkey对应颜色调整
    img = pygame.transform.scale(img,(int(width*scale),int(height*scale)))
    return img#接收一个变量名，把抠出来的图存到内存里面


