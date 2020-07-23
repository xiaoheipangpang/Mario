import pygame
from SUPERMARIO.source import tools
from SUPERMARIO.source import constant as c
from SUPERMARIO.source.components import player,stuff,brick,info,box,enemy,coin
from SUPERMARIO.source import setup
import json
import os#操作系统文件夹
class Level:
    def start(self,game_info):
        self.game_info = game_info
        self.finished = False
        self.next = 'game_over'
        self.setup_background()  # 初始化背景
        self.info = info.Info('level',self.game_info)
        self.setup_player()
        self.load_map_data()
        self.setup_start_positions()
        self.setup_ground_items()
        self.setup_bricks()
        self.setup_boxs()
        self.setup_enemies()
        self.setup_checkpoints()
        self.setup_coin()
        self.checkpoint_timer = 0
    def load_map_data(self):
        file_name = 'level_1.json'
        file_path = os.path.join('C:\\Users\\86180\\PycharmProjects\\untitled5\\SUPERMARIO\\source\\data\\maps'
                                 ,file_name)
        with open(file_path) as f:  # 打开文件
            self.map_data = json.load(f)
    def setup_background(self):
        self.BG = pygame.image.load(
            'C:\\Users\\86180\\PycharmProjects\\untitled5\\SUPERMARIO\\resources\\graphics\\level_1.png')
        w, h = self.BG.get_size()
        self.BG = pygame.transform.scale(self.BG, (int(w * c.BG_scale), int(h * c.BG_scale)))
        self.view = tools.load_image(
            'C:\\Users\\86180\\PycharmProjects\\untitled5\\SUPERMARIO\\resources\\graphics\\title_screen.png'
            , 1, 60, 176, 88, (225, 0, 220), c.BG_scale)
        self.BG_rect = self.BG.get_rect()
        self.game_window = setup.window.get_rect()#其实是截取矩形的功能
        self.game_ground = pygame.Surface((self.BG_rect.width,self.BG_rect.height))
    def setup_start_positions(self):
        self.positions = []
        for data in self.map_data['maps']:
            self.positions.append((data['start_x'],data['end_x'],data['player_x'],data['player_y']))
        self.start_x ,self.end_x ,self.player_x ,self.player_y = self.positions[0]

    def setup_coin(self):
        self.coin_group = pygame.sprite.Group()
        if 'coin' in self.map_data:
            for coin_data in self.map_data['coin']:
                x,y = coin_data['x'],coin_data['y']
                self.coin_group.add(coin.Levelcoin(x,y))
    def setup_player(self):
        self.player = player.Player('mario')
        self.player.rect.x = 300
        self.player.rect.y = 490
    def setup_ground_items(self):
        self.ground_items_group = pygame.sprite.Group()
        for name in ['ground','pipe','step']:
            for item in self.map_data[name]:
                m = stuff.Item(item['x'], item['y'], item['width'], item['height'], name)
                self.ground_items_group.add(m)

    def update(self,surface,keys):
        self.current_time = pygame.time.get_ticks()
        self.player.update(surface,keys)
        if self.player.dead:
            if self.current_time - self.player.death_timer > 3000:
                self.finished = True
                self.update_game_info()
        else:
            self.update_player_position()
            self.check_checkpoint()
            self.check_if_go_die()
            self.update_game_window()
            self.brick_group.update()
            self.box_group.update()
            self.check_current_time = pygame.time.get_ticks()
            if self.check_current_time - self.checkpoint_timer > 50:
                self.enemy_group.update(self)
            self.dying_group.update(self)
            self.coin_group.update()


        self.draw(surface,keys)
    def check_if_go_die(self):
         if self.player.rect.y > c.SCREEN_H :
             self.player.go_die()

    def update_player_position(self):
        self.player.rect.x += self.player.x_vel
        if self.player.rect.x < self.start_x:
             self.player.rect.x = self.start_x
        elif self.player.rect.right > self.end_x:
             self.player.rect.right = self.end_x
        self.check_x_collisions()
        self.player.rect.y += self.player.y_vel
        self.check_y_collisions()
        self.check_will_fall(self.player)
    def check_x_collisions(self):
        check_group = pygame.sprite.Group(self.ground_items_group, self.brick_group,self.box_group)
        ground_item = pygame.sprite.spritecollideany(self.player, check_group)
        if ground_item:
            self.adjust_player_x(ground_item)
        enemy_a = pygame.sprite.spritecollideany(self.player, self.enemy_group)
        if enemy_a:
            self.player.go_die()

    def check_y_collisions(self):
        self.dying_group = pygame.sprite.Group()
        check_group = pygame.sprite.Group(self.ground_items_group, self.brick_group,self.box_group)
        ground_item = pygame.sprite.spritecollideany(self.player, check_group)
        if ground_item:
            self.adjust_player_y(ground_item)
            self.check_will_fall(self.player)
        enemy_a = pygame.sprite.spritecollideany(self.player,self.enemy_group)
        if enemy_a:
            self.enemy_group.remove(enemy_a)
            self.dying_group.add(enemy_a)
            if self.player.y_vel < 0:
                how = 'bumped'
            else:
                how = 'trumped'
                self.player.state = 'jump'
                self.player.rect.bottom = enemy_a.rect.top
                self.player.y_vel = self.player.jump_vel *0.8
            enemy.Enemy.go_die(enemy,how)
        coin = pygame.sprite.spritecollideany(self.player, self.coin_group)
        if coin :
            coin.kill()
            self.game_info['coin'] += 1



    def adjust_player_x(self, sprite):
        if self.player.rect.x < sprite.rect.x:
            self.player.rect.right = sprite.rect.left
        else:
            self.player.rect.left = sprite.rect.right
        self.player.x_vel = 0
    def adjust_player_y(self,sprite):
        #从下往上
        # if self.player.rect.top > sprite.rect.bottom:
        #     self.player.y_vel = 7
        if self.player.rect.bottom < sprite.rect.bottom:
            self.player.y_vel = 0
            self.player.rect.bottom = sprite.rect.top
            self.player.state = 'walk'
            #print(self.player.rect.bottom)#检测错误
            #print(sprite.rect.bottom)
        else:
            #self.player.y_vel = 7
            self.player.rect.top = sprite.rect.bottom
            self.player.state = 'fall'
            #print(self.player.rect.bottom)
            #print(sprite.rect.bottom)
    def check_will_fall(self,sprite):
        sprite.rect.y += 1
        check_group = pygame.sprite.Group(self.ground_items_group, self.brick_group,self.box_group)
        collided = pygame.sprite.spritecollideany(sprite,check_group)
        if not collided and sprite.state != 'jump':
            sprite.state = 'fall'
        sprite.rect.y -= 1


    def update_game_window(self):#让截取的位置变化
         third = self.game_window.x + self.game_window.width / 3#图片在屏幕（0,0）点的距离图片原点的距离+屏幕三分之一
         if self.player.x_vel > 0 and self.player.rect.centerx > third and self.game_window.right < self.end_x:
            self.game_window.x += self.player.x_vel
            self.start_x = self.game_window.x


    def draw(self,surface,keys):
        self.game_ground.blit(self.BG,self.game_window,self.game_window)#滑动窗口的实现要设置底板，先把现在要用的背景画在底板上
        self.game_ground.blit(self.player.image, self.player.rect)#再把人物画在底板上
        self.brick_group.draw(self.game_ground)
        self.box_group.draw(self.game_ground)
        self.enemy_group.draw(self.game_ground)
        self.coin_group.draw(self.game_ground)
        surface.blit(self.game_ground,(0,0),self.game_window)
        self.info.start(self.game_info)
        self.info.update(surface)
        self.info.draw(surface)
    def update_game_info(self):
        if self.player.dead:
            self.game_info['lives'] -= 1
        if self.game_info['lives'] == 0:
            self.next = 'game_over'
        else:
            self.next = 'load_screen'
    def setup_bricks(self):
        self.brick_group = pygame.sprite.Group()
        if 'brick' in self.map_data:
            for brick_data in self.map_data['brick']:
                x,y = brick_data['x'],brick_data['y']
                brick_type = brick_data['type']
                if 'brick_num' in brick_data:
                    pass
                else:
                    self.brick_group.add(brick.Brick(x,y,brick_type))
    def setup_boxs(self):
        self.box_group = pygame.sprite.Group()
        if 'box' in self.map_data:
            for box_data in self.map_data['box']:
                x,y = box_data['x'],box_data['y']
                box_type = box_data['type']
                self.box_group.add(box.Box(x,y,box_type))
    def setup_enemies(self):
        self.enemy_group = pygame.sprite.Group()
        self.enemy_group_dict = {}
        for enemy_group_data in self.map_data['enemy']:
            enemy_group = pygame.sprite.Group()
            for enemy_group_id,enemy_list in enemy_group_data.items():#键值对
                for enemy_data in enemy_list:
                    enemy_group.add(enemy.create_enemy(enemy_data))#把实例化对象加到精灵组里面
                self.enemy_group_dict[enemy_group_id] = enemy_group
    def setup_checkpoints(self):
        self.checkpoint_group = pygame.sprite.Group()
        for item in self.map_data['checkpoint']:
            x,y,w,h = item['x'],item['y'],item['width'],item['height']
            checkpoint_type = item['type']
            enemy_groupid = item.get('enemy_groupid')
            self.checkpoint_group.add(stuff.Checkpoint(x,y,w,h,checkpoint_type,enemy_groupid))
    def check_checkpoint(self):
        checkpoint = pygame.sprite.spritecollideany(self.player,self.checkpoint_group)
        if checkpoint:
            if checkpoint.checkpoint_type == 0:
                self.enemy_group.add(self.enemy_group_dict[str(checkpoint.enemy_groupid)])#把敌人组的序号变成字符串，符合字典的键的数据类型
                self.checkpoint_timer = pygame.time.get_ticks()

            checkpoint.kill()









