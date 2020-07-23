import pygame
from SUPERMARIO.source import setup
from SUPERMARIO.source import tools
from SUPERMARIO.source import constant as c
import json
import os#操作系统文件夹
class Player(pygame.sprite.Sprite):
    def __init__(self, name):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.load_data()  # 初始化下载数据方法
        self.setup_states()
        self.setup_velocities()
        self.setup_timers()
        self.load_images()
        self.anti_gravity = c.ANTI_GRAVITY


    def load_data(self):
        file_name = self.name + '.json'  # 拼文件名
        file_path = os.path.join('C:\\Users\\86180\\PycharmProjects\\untitled5\\SUPERMARIO\\source\\data\\player',
                                 file_name)  # 拼路径
        with open(file_path) as f:  # 打开文件
            self.player_data = json.load(f)  # 下载储存数据

    def setup_states(self):
        self.face_right = True
        self.dead = False
        self.big = False
        self.state = 'stand'

    def setup_velocities(self):
        speed = self.player_data['speed']
        self.x_vel = 0
        self.y_vel = 0
        self.max_walk_vel = speed['max_walk_speed']
        self.max_run_vel = speed['max_run_speed']
        self.max_y_vel = speed['max_y_velocity']
        self.jump_vel = speed['jump_velocity']
        self.walk_accel = speed['walk_accel']
        self.run_accel = speed['run_accel']
        self.turn_accel = speed['turn_accel']
        self.gravity = c.GRAVITY
        self.max_x_vel = self.max_walk_vel
        self.x_accel = self.walk_accel


    def setup_timers(self):
        self.walking_timer = 0
        self.transition_time = 0

    def load_images(self):

        frame_rects = self.player_data['image_frames']

        # 建立帧库

        self.right_small_normal_frames = []
        self.right_big_normal_frames = []
        self.right_big_fire_frames = []
        self.left_small_normal_frames = []
        self.left_big_normal_frames = []
        self.left_big_fire_frames = []

        self.small_normal_frames = [self.right_small_normal_frames, self.left_small_normal_frames]
        self.big_normal_frames = [self.right_big_normal_frames, self.left_big_normal_frames]
        self.big_fire_frames = [self.right_big_fire_frames, self.left_big_fire_frames]

        self.all_frames = [
            self.right_small_normal_frames,
            self.right_big_normal_frames,
            self.right_big_fire_frames,
            self.left_small_normal_frames,
            self.left_big_normal_frames,
            self.left_big_fire_frames
            ]

        self.right_frames = self.right_small_normal_frames
        self.left_frames = self.left_small_normal_frames

        for group, group_frame_rects in frame_rects.items():
            for frame_rect in group_frame_rects:
                right_image = tools.load_image('C:\\Users\\86180\\PycharmProjects\\untitled5\\SUPERMARIO\\resources\\graphics\\mario_bros.png',
                                               frame_rect['x'],frame_rect['y'],frame_rect['width'],frame_rect['height'],(0,0,0),c.PLAYER_SCALE)
                left_image = pygame.transform.flip(right_image,True,False)
                if group == 'right_small_normal':
                    self.right_small_normal_frames.append(right_image)
                    self.left_small_normal_frames.append(left_image)
                elif group == 'right_big_normal':
                    self.right_big_normal_frames.append(right_image)
                    self.left_big_normal_frames.append(left_image)
                elif group == 'right_big_fire':
                    self.right_big_fire_frames.append(right_image)
                    self.left_big_fire_frames.append(left_image)

        self.frame_index = 0
        self.frames = self.right_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()

    def update(self,surface,keys):
        self.current_time = pygame.time.get_ticks()  # 设置计时器实现帧的循环
        self.handle_states(keys)

    def handle_states(self,keys):

        self.can_jump_or_not(keys)
        if self.state == 'stand':
            self.stand(keys)
        elif self.state == 'walk':
            self.walk(keys)
        elif self.state == 'jump':
            self.jump(keys)
        elif self.state == 'fall':
            self.fall()
        elif self.state == 'die':
            self.die()

        if self.face_right:
            self.image = self.right_frames[self.frame_index]
            m = self.image.get_rect()
            self.rect.w = m.w
            self.rect.h = m.h


        else:
            self.image = self.left_frames[self.frame_index]
            m = self.image.get_rect()
            self.rect.w = m.w
            self.rect.h = m.h

    def can_jump_or_not(self,keys):
        if not keys[pygame.K_a]:
            self.can_jump = True

    def stand(self,keys):
        self.frame_index = 0
        self.x_vel = 0
        self.v_vel = 0
        if keys[pygame.K_RIGHT]:
            self.face_right = True
            self.state = 'walk'
        elif keys[pygame.K_LEFT]:
            self.face_right = False
            self.state = 'walk'
        elif keys[pygame.K_a] and self.can_jump:
            self.state = 'jump'
            self.y_vel = self.jump_vel

    def walk(self, keys):
        if keys[pygame.K_s]:
            self.max_x_vel = self.max_run_vel
            self.x_accel = self.run_accel
        else:
            self.max_x_vel = self.max_walk_vel
            self.x_accel = self.walk_accel

        if keys[pygame.K_a] and self.can_jump:
            self.state = 'jump'
            self.y_vel = self.jump_vel

        if self.current_time - self.walking_timer > self.clac_frame_duration():
            if self.frame_index <= 3:
                self.frame_index += 1
            else:
                self.frame_index = 1
            self.walking_timer = self.current_time
        if keys[pygame.K_RIGHT]:
            self.face_right = True
            if self.x_vel < 0:
                self.frame_index = 5#刹车帧
                self.accel= self.turn_accel
            self.x_vel = self.calc_vel(self.x_vel,self.x_accel,self.max_x_vel,True)
        elif keys[pygame.K_LEFT]:
            self.face_right = False
            if self.x_vel > 0:
                self.frame_index = 5#刹车帧
                self.accel= self.turn_accel
            self.x_vel = self.calc_vel(self.x_vel,self.x_accel,self.max_x_vel,False)
        else:#走着走着停下来
            if self.face_right:
                self.x_vel -= self.x_accel
                if self.x_vel < 0:
                    self.x_vel = 0
                    self.state = 'stand'
            else:
                self.x_vel +=self.x_accel
                if self.x_vel > 0:
                    self.x_vel = 0
                    self.state = 'stand'



    def jump(self,keys):
        self.frame_index = 4
        self.y_vel += self.anti_gravity
        self.can_jump = False

        if self.y_vel >= 0:
            self.state = 'fall'

        if keys[pygame.K_RIGHT]:
            self.x_vel = self.calc_vel(self.x_vel, self.x_accel, self.max_x_vel,True)
        elif keys[pygame.K_LEFT]:
            self.x_vel = self.calc_vel(self.x_vel, self.x_accel, self.max_x_vel,False)
        if not keys[pygame.K_a]:
            self.state = 'fall'

    def fall(self):
        self.y_vel = self.calc_vel(self.y_vel,self.gravity,self.max_y_vel)
    def die(self):
        self.rect.y += self.y_vel
        self.y_vel += self.anti_gravity
    def go_die(self):
        self.dead = True
        self.y_vel = self.jump_vel
        self.frame_index = 6
        self.state = 'die'
        self.death_timer = self.current_time
    def calc_vel(selfself,vel,accel,max_vel,is_positive = True):#自动计算当前应该有的速度
        if is_positive:
            return min(vel + accel,max_vel)
        else:
            return max(vel - accel, -max_vel)
    def clac_frame_duration(self):
        duration = -60 / self.max_run_vel*abs(self.x_vel) + 80
        return duration
