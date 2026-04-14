"""
飞机大战 Airplane Battle v3.1 - 双模式章节Boss版
Airplane Battle v3.1 - Dual-Mode Chapter Boss Edition
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
v3.1 重大更新：
  ✅ 章节解锁系统：初始仅第1章可玩，击败Boss解锁下一章（进度自动保存）
  ✅ 双模式系统：故事模式（章节解锁推进）+ 挑战模式（无限Boss）
  ✅ 修复 Enemy.__init__ enemy_imgs 引用问题
  ✅ Boss入场提前警告提示（60%距离时HUD提示）
  ✅ 每章Boss颜色专属星空背景

故事模式章节Boss设计：
  第1章 - 红色尖兵Boss：十字交叉弹幕     触发：800m  [初始解锁]
  第2章 - 紫色利刃Boss：旋转螺旋弹幕     触发：1500m [击败CH1解锁]
  第3章 - 棕色重甲Boss：3方向散射弹幕     触发：2500m [击败CH2解锁]
  第4章 - 绿色精英Boss：追踪弹+散布弹     触发：4000m [击败CH3解锁]
  第5章 - 黄金终焉Boss：全屏乱射+激光预警 触发：6000m [击败CH4解锁]

挑战模式Boss触发：每1800m一波，随机章节Boss

前置依赖：pip install pygame
作者：阿爪 🦞 | 2026-04
"""

import pygame
import random
import math
import sys
import json
import os
from datetime import datetime

# ======================== 初始化 ========================
pygame.init()
try:
    pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=2048)
except Exception:
    pass

SCREEN_WIDTH = 540
SCREEN_HEIGHT = 780
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("飞机大战 v3.1 - 双模式章节Boss版")
clock = pygame.time.Clock()

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LEADERBOARD_FILE = os.path.join(_SCRIPT_DIR, "leaderboard3.json")
PROGRESS_FILE = os.path.join(_SCRIPT_DIR, "chapter_progress.json")

# ======================== 颜色 ========================
WHITE = (255, 255, 255); BLACK = (0, 0, 0)
RED = (255, 60, 60); DARK_RED = (180, 30, 30)
GREEN = (50, 255, 100); DARK_GREEN = (20, 120, 40)
BLUE = (60, 140, 255); DARK_BLUE = (8, 15, 35)
NAVY = (12, 24, 52)
YELLOW = (255, 230, 0); ORANGE = (255, 160, 0)
CYAN = (0, 220, 255); LIGHT_CYAN = (120, 240, 255)
PURPLE = (180, 70, 255); MAGENTA = (255, 80, 180)
GOLD = (255, 215, 0); SILVER = (200, 210, 220)
GRAY = (100, 100, 110); LIGHT_GRAY = (150, 155, 165)
BROWN = (160, 90, 45); IVORY = (255, 250, 240)

# 章节主题配色
CHAPTER_THEMES = {
    1: {'bg_r': 8,   'bg_g': 15,  'bg_b': 35,  'accent': RED},
    2: {'bg_r': 12,  'bg_g': 8,   'bg_b': 28,  'accent': PURPLE},
    3: {'bg_r': 18,  'bg_g': 10,  'bg_b': 20,  'accent': BROWN},
    4: {'bg_r': 5,   'bg_g': 20,  'bg_b': 10,  'accent': GREEN},
    5: {'bg_r': 20,  'bg_g': 15,  'bg_b': 5,   'accent': GOLD},
}

def gradient_color(c1, c2, ratio):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * ratio) for i in range(3))

# ======================== 字体 ========================
try:
    font_tiny    = pygame.font.SysFont("simhei", 16)
    font_small   = pygame.font.SysFont("simhei", 22)
    font_medium  = pygame.font.SysFont("simhei", 30)
    font_large   = pygame.font.SysFont("simhei", 48)
    font_title   = pygame.font.SysFont("simhei", 62)
except:
    font_tiny    = pygame.font.Font(None, 18)
    font_small   = pygame.font.Font(None, 24)
    font_medium  = pygame.font.Font(None, 34)
    font_large   = pygame.font.Font(None, 52)
    font_title   = pygame.font.Font(None, 68)

# ======================== 玩家飞机 ========================
def create_player_surface():
    surf = pygame.Surface((56, 68), pygame.SRCALPHA)
    body_pts = [(28,0),(34,14),(40,26),(36,38),(32,54),(28,58),(24,54),(20,38),(16,26),(22,14)]
    pygame.draw.polygon(surf, CYAN, body_pts)
    pygame.draw.polygon(surf, WHITE, body_pts, 2)
    pygame.draw.lines(surf, LIGHT_CYAN, False, [(27,2),(32,13),(37,24),(33,36),(29,50)], 2)
    pygame.draw.polygon(surf, (40,160,220), [(16,26),(2,38),(6,40),(18,36)])
    pygame.draw.polygon(surf, (40,160,220), [(40,26),(54,38),(50,40),(38,36)])
    pygame.draw.polygon(surf, LIGHT_CYAN, [(16,26),(2,38),(6,40),(18,36)], 1)
    pygame.draw.polygon(surf, LIGHT_CYAN, [(40,26),(54,38),(50,40),(38,36)], 1)
    pygame.draw.circle(surf, RED, (5,39), 3); pygame.draw.circle(surf, RED, (51,39), 3)
    cockpit_outer = [(25,10),(31,10),(33,20),(29,28),(23,20)]
    pygame.draw.polygon(surf, (30,80,150), cockpit_outer)
    pygame.draw.polygon(surf, (100,180,230), [(26,12),(30,12),(31,19),(28,25),(24,19)])
    pygame.draw.circle(surf, (200,220,255), (28,18), 4)
    wing_t = [(12,36),(4,50),(10,52),(18,44)]; wing_b = [(44,36),(52,50),(46,52),(38,44)]
    pygame.draw.polygon(surf, (20,120,180), wing_t); pygame.draw.polygon(surf, (20,120,180), wing_b)
    pygame.draw.polygon(surf, LIGHT_CYAN, wing_t, 1); pygame.draw.polygon(surf, LIGHT_CYAN, wing_b, 1)
    for i,(x,y) in enumerate([(7,46),(11,52),(49,46),(45,52)]):
        col = ORANGE if i%2==0 else YELLOW
        pygame.draw.circle(surf, col, (x,y), 4)
        pygame.draw.circle(surf, WHITE, (x,y), 2)
    pygame.draw.circle(surf, CYAN, (28,16), 2)
    return surf

# ======================== 敌机造型 ========================
def create_enemy_surface(enemy_type, chapter=1):
    w, h = (44,52) if enemy_type=='small' else ((60,70) if enemy_type=='medium' else (80,90))
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    cx, cy = w//2, h//2
    colors = CHAPTER_THEMES[chapter]
    accent = colors['accent']
    dark_accent = tuple(max(0, c-60) for c in accent)
    if enemy_type == 'small':
        body = [(cx,2),(cx+8,12),(cx+14,26),(cx+10,40),(cx+6,50),(cx-6,50),(cx-10,40),(cx-14,26),(cx-8,12)]
        pygame.draw.polygon(surf, accent, body)
        pygame.draw.polygon(surf, WHITE, body, 1)
        pygame.draw.polygon(surf, dark_accent, [(cx,4),(cx+6,12),(cx+11,25),(cx+8,37),(cx+4,47),(cx-4,47),(cx-8,37),(cx-11,25),(cx-6,12)])
        wing_l = [(2,h-12),(cx-14,cy+2),(cx-10,h-6)]; wing_r = [(w-2,h-12),(cx+14,cy+2),(cx+10,h-6)]
        pygame.draw.polygon(surf, dark_accent, wing_l); pygame.draw.polygon(surf, dark_accent, wing_r)
        pygame.draw.circle(surf, WHITE, (cx,h//4), 4)
    elif enemy_type == 'medium':
        body = [(cx,4),(cx+12,16),(cx+20,32),(cx+16,50),(cx+8,66),(cx-8,66),(cx-16,50),(cx-20,32),(cx-12,16)]
        pygame.draw.polygon(surf, accent, body)
        pygame.draw.polygon(surf, WHITE, body, 1)
        pygame.draw.polygon(surf, dark_accent, [(cx,6),(cx+10,16),(cx+17,31),(cx+13,47),(cx+7,62),(cx-7,62),(cx-13,47),(cx-17,31),(cx-10,16)])
        wing_l = [(4,h-14),(cx-16,cy+4),(cx-12,h-8)]; wing_r = [(w-4,h-14),(cx+16,cy+4),(cx+12,h-8)]
        pygame.draw.polygon(surf, accent, wing_l, 1); pygame.draw.polygon(surf, accent, wing_r, 1)
        pygame.draw.circle(surf, WHITE, (cx,h//4+4), 5); pygame.draw.circle(surf, accent, (cx,h//4+4), 3)
    else:
        body = [(cx,6),(cx+16,22),(cx+28,44),(cx+22,68),(cx+10,86),(cx-10,86),(cx-22,68),(cx-28,44),(cx-16,22)]
        pygame.draw.polygon(surf, accent, body)
        pygame.draw.polygon(surf, WHITE, body, 2)
        mid = [(cx,10),(cx+14,22),(cx+24,42),(cx+18,64),(cx+8,82),(cx-8,82),(cx-18,64),(cx-24,42),(cx-14,22)]
        pygame.draw.polygon(surf, dark_accent, mid)
        wing_l = [(6,h-18),(cx-20,cy+6),(cx-14,h-10)]; wing_r = [(w-6,h-18),(cx+20,cy+6),(cx+14,h-10)]
        pygame.draw.polygon(surf, accent, wing_l); pygame.draw.polygon(surf, accent, wing_r)
        pygame.draw.circle(surf, WHITE, (cx,h//4+6), 7)
        pygame.draw.circle(surf, accent, (cx,h//4+6), 4)
    return surf

# ======================== Boss绘制 ========================
def create_boss_surface(chapter):
    surf = pygame.Surface((200, 140), pygame.SRCALPHA)
    cx, cy = 100, 70
    colors_map = {1: (RED, ORANGE, DARK_RED),
                  2: (PURPLE, MAGENTA, (100,30,160)),
                  3: (BROWN, ORANGE, (90,50,20)),
                  4: (GREEN, CYAN, (20,120,40)),
                  5: (GOLD, YELLOW, (180,150,0))}
    main_c, light_c, dark_c = colors_map.get(chapter, (RED,ORANGE,DARK_RED))
    # 主体
    body = [(cx,6),(cx+22,18),(cx+38,36),(cx+44,58),(cx+40,82),(cx+30,100),(cx+16,118),(cx-16,118),(cx-30,100),(cx-40,82),(cx-44,58),(cx-38,36),(cx-22,18)]
    pygame.draw.polygon(surf, main_c, body)
    pygame.draw.polygon(surf, WHITE, body, 2)
    mid = [(cx,14),(cx+18,22),(cx+32,38),(cx+37,58),(cx+33,78),(cx+24,94),(cx+12,110),(cx-12,110),(cx-24,94),(cx-33,78),(cx-37,58),(cx-32,38),(cx-18,22)]
    pygame.draw.polygon(surf, dark_c, mid)
    # 机翼
    for x_dir in [1, -1]:
        wx = cx + x_dir*50
        wing = [(cx+x_dir*32,58),(wx,40),(wx+4,50),(wx+8,72),(cx+x_dir*34,80)]
        pygame.draw.polygon(surf, main_c, wing)
        pygame.draw.polygon(surf, light_c, wing, 1)
        sub_wing = [(cx+x_dir*36,68),(wx+4,52),(wx+6,60),(wx+10,78),(cx+x_dir*38,82)]
        pygame.draw.polygon(surf, dark_c, sub_wing)
    # 驾驶舱
    pygame.draw.ellipse(surf, (30,80,160), (cx-12,12,24,22))
    pygame.draw.ellipse(surf, (100,180,240), (cx-8,14,16,16))
    pygame.draw.circle(surf, WHITE, (cx,22), 4)
    # 发动机
    for i,(bx,by) in enumerate([(cx-28,108),(cx-10,116),(cx+10,116),(cx+28,108)]):
        col = ORANGE if i%2==0 else YELLOW
        pygame.draw.circle(surf, dark_c, (bx,by), 8); pygame.draw.circle(surf, col, (bx,by), 5)
        pygame.draw.circle(surf, WHITE, (bx,by), 2)
    # 装饰线
    for y_off in [30,50,70]:
        pygame.draw.line(surf, dark_c, (cx-35,cy+y_off-20),(cx-20,cy+y_off-10),1)
        pygame.draw.line(surf, dark_c, (cx+20,cy+y_off-10),(cx+35,cy+y_off-20),1)
    # 章节号
    try:
        num_font = pygame.font.SysFont("simhei", 18)
        ch_txt = num_font.render(str(chapter), True, WHITE)
        tr = ch_txt.get_rect(center=(cx, cy-18))
        surf.blit(ch_txt, tr)
    except: pass
    # BOSS字样
    boss_txt = font_tiny.render("BOSS", True, WHITE)
    boss_rect = boss_txt.get_rect(center=(cx, cy-18))
    surf.blit(boss_txt, boss_rect)
    return surf

# ======================== 爆炸效果 ========================
def create_explosion_frames(count=8, size=48, base_color=ORANGE):
    frames=[]
    for i in range(count):
        s=pygame.Surface((size,size),pygame.SRCALPHA); r=int(size*0.5*(i/count)); a=int(255*(1-i/count))
        if r>0: pygame.draw.circle(s,(*base_color,a),(size//2,size//2),r)
        for j in range(8):
            ang=j*math.pi/4+i*0.3; d=r+int(size*0.2*(1-i/count))
            ex=int(size//2+d*math.cos(ang)); ey=int(size//2+d*math.sin(ang))
            if 0<=ex<size and 0<=ey<size: pygame.draw.circle(s,(255,max(0,200-i*20),0,a//2),(ex,ey),max(1,r//6))
        frames.append(s)
    return frames

class Explosion:
    _all_frames={}
    def __init__(self,x,y,scale=1.0,color=None):
        self.x=x; self.y=y; self.scale=scale; self.frame=0
        self.color=color or ORANGE
        key=f"{int(scale*10)}_{self.color}"
        if key not in Explosion._all_frames:
            Explosion._all_frames[key]=create_explosion_frames(8,int(48*scale),self.color)
        self.frames=Explosion._all_frames[key]
        self.max_frame=len(self.frames); self.alive=True
    def update(self):
        self.frame+=1
        if self.frame>=self.max_frame: self.alive=False
    def draw(self,sf):
        if self.alive and self.frame<self.max_frame:
            f=self.frames[self.frame]; r=f.get_rect(center=(int(self.x),int(self.y)))
            sf.blit(f,r)

class Particle:
    _pool={}
    def __init__(self,x,y,color=None,vx=None,vy=None,lifespan=None,size=None):
        self.x=x; self.y=y; self.color=color or random.choice([RED,ORANGE,YELLOW,WHITE])
        self.vx=vx or random.uniform(-3,3); self.vy=vy or random.uniform(-5,1)
        self.lifespan=lifespan or random.randint(20,45); self.age=0; self.alive=True
        self.size=size or random.randint(2,5)
    def update(self):
        self.x+=self.vx; self.y+=self.vy; self.vy+=0.12; self.age+=1
        if self.age>=self.lifespan: self.alive=False
        return self.alive
    def draw(self,sf):
        if self.alive:
            a=int(255*(1-self.age/self.lifespan))
            try:
                col=(*self.color[:3],a) if len(self.color)==4 else self.color
                ps=pygame.Surface((self.size*2,self.size*2),pygame.SRCALPHA)
                pygame.draw.circle(ps,col,(self.size,self.size),self.size)
                sf.blit(ps,(int(self.x)-self.size,int(self.y)-self.size))
            except: pass

class TrailParticle:
    def __init__(self,x,y,color=ORANGE):
        self.x=x; self.y=y; self.color=color; self.life=18; self.age=0; self.alive=True
    def update(self):
        self.y+=1.5; self.age+=1; self.life-=1
        if self.life<=0: self.alive=False
        return self.alive
    def draw(self,sf):
        if self.alive:
            a=int(200*(self.life/18))
            try:
                ps=pygame.Surface((6,6),pygame.SRCALPHA); pygame.draw.circle(ps,(*self.color[:3],a),(3,3),3)
                sf.blit(ps,(int(self.x)-3,int(self.y)-3))
            except: pass

# ======================== 道具系统 ========================
class PowerUp:
    TYPES=['power','heal','bomb','shield','speed','magnet','freeze','score','laser']
    ICONS={}
    @classmethod
    def _gen_icons(cls):
        for t in cls.TYPES:
            s=pygame.Surface((28,28),pygame.SRCALPHA); c=cls._color_map()[t]
            pygame.draw.circle(s,c,(14,14),13); pygame.draw.circle(s,WHITE,(14,14),13,2)
            txt=font_tiny.render(cls._label_map()[t],True,WHITE); tr=txt.get_rect(center=(14,14))
            s.blit(txt,tr); cls.ICONS[t]=s
    @staticmethod
    def _color_map():
        return {'power':CYAN,'heal':GREEN,'bomb':RED,'shield':BLUE,'speed':YELLOW,'magnet':MAGENTA,'freeze':LIGHT_CYAN,'score':GOLD,'laser':PURPLE}
    @staticmethod
    def _label_map():
        return {'power':'P','heal':'H','bomb':'B','shield':'S','speed':'★','magnet':'M','freeze':'❄','score':'$','laser':'L'}
    def __init__(self,x,y):
        if not PowerUp.ICONS: PowerUp._gen_icons()
        self.x=x; self.y=y; self.type=random.choice(self.TYPES)
        self.rect=pygame.Rect(int(x)-14,int(y)-14,28,28); self.alive=True
    def update(self):
        self.y+=2; self.rect.y=int(self.y)
        if self.y>SCREEN_HEIGHT+30: self.alive=False
        return self.alive
    def draw(self,sf):
        if self.alive and self.type in PowerUp.ICONS:
            sf.blit(PowerUp.ICONS[self.type],self.rect)
    def apply(self,player,game=None):
        p=player
        if self.type=='power': p.power_level=min(p.power_level+1,5)
        elif self.type=='heal':
            if p.hp<p.max_hp: p.hp=min(p.hp+1,p.max_hp)
        elif self.type=='bomb':
            if game: game.bombs_available=min(game.bombs_available+1,5)
        elif self.type=='shield': p.shield_timer=300
        elif self.type=='speed': p.speed_boost_timer=300
        elif self.type=='magnet': p.magnet_active=True; p.magnet_timer=300
        elif self.type=='freeze':
            if game: game.freeze_timer=120
        elif self.type=='score': pass
        elif self.type=='laser': p.laser_active=True; p.laser_timer=180

# ======================== 障碍物 ========================
class Obstacle:
    _asteroid_surf=None; _barrier_surf=None
    @classmethod
    def _init_surfaces(cls):
        if cls._asteroid_surf is None:
            s=pygame.Surface((50,50),pygame.SRCALPHA)
            pygame.draw.circle(s,GRAY,(25,25),24)
            for _ in range(6):
                cx2=random.randint(5,45); cy2=random.randint(5,45); r=random.randint(4,10)
                pygame.draw.circle(s,DARK_BLUE,(cx2,cy2),r)
            pygame.draw.circle(s,(*GRAY[:3],150),(25,25),24,3)
            cls._asteroid_surf=s
    def __init__(self):
        self.type='asteroid'; Obstacle._init_surfaces()
        self.x=random.randint(30,SCREEN_WIDTH-30); self.y=-60
        self.vy=random.uniform(1.5,3.5); self.vx=random.uniform(-1,1)
        self.size=random.randint(18,28); self.angle=0; self.spin=random.uniform(-3,3)
        self.rect=pygame.Rect(int(self.x)-self.size,int(self.y)-self.size,self.size*2,self.size*2)
        self.alive=True; self.score=80; self.damage=1
    def update(self):
        self.y+=self.vy; self.x+=self.vx; self.angle+=self.spin
        self.rect.center=(int(self.x),int(self.y))
        if self.y>SCREEN_HEIGHT+60: self.alive=False
        return self.alive
    def draw(self,sf):
        if self.alive:
            s=pygame.transform.rotate(Obstacle._asteroid_surf,self.angle)
            sr=s.get_rect(center=(int(self.x),int(self.y)))
            sf.blit(s,sr)

# ======================== 星空背景 ========================
class StarField:
    def __init__(self):
        self.stars=[pygame.math.Vector2(random.uniform(0,SCREEN_WIDTH),random.uniform(0,SCREEN_HEIGHT))
                    for _ in range(160)]
        self.speeds=[random.uniform(0.8,4) for _ in self.stars]
        self.sizes=[random.randint(1,3) for _ in self.stars]
        self.bright=[random.randint(150,255) for _ in self.stars]
    def update(self):
        for i,s in enumerate(self.stars):
            s.y+=self.speeds[i]
            if s.y>SCREEN_HEIGHT: s.y=0; s.x=random.uniform(0,SCREEN_WIDTH)
    def draw(self,sf):
        for i,s in enumerate(self.stars):
            try: pygame.draw.circle(sf,(self.bright[i],self.bright[i],min(255,self.bright[i]+20)),(int(s.x),int(s.y)),self.sizes[i])
            except: pass

# ======================== 玩家飞机类 ========================
class Player:
    def __init__(self):
        self.x=SCREEN_WIDTH//2; self.y=SCREEN_HEIGHT-100
        self.image=create_player_surface(); self.rect=self.image.get_rect(center=(self.x,self.y))
        self.speed=5; self.hp=3; self.max_hp=3; self.alive=True
        self.power_level=1; self.invincible_timer=0; self.shield_timer=0
        self.speed_boost_timer=0; self.magnet_active=False; self.magnet_timer=0
        self.laser_active=False; self.laser_timer=0; self.engine_flicker=0
        self._hp_surf_cache=None
    @property
    def speed_boost(self):
        return self.speed_boost_timer > 0
    def update(self,keys):
        cs=self.speed*(1.5 if self.speed_boost_timer>0 else 1)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: self.rect.x-=cs
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: self.rect.x+=cs
        if keys[pygame.K_UP] or keys[pygame.K_w]: self.rect.y-=cs
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: self.rect.y+=cs
        self.rect.clamp_ip(pygame.Rect(0,0,SCREEN_WIDTH,SCREEN_HEIGHT))
        if self.invincible_timer>0: self.invincible_timer-=1
        if self.shield_timer>0: self.shield_timer-=1
        if self.speed_boost_timer>0: self.speed_boost_timer-=1
        if self.magnet_timer>0: self.magnet_timer-=1
        else: self.magnet_active=False
        if self.laser_timer>0: self.laser_timer-=1
        else: self.laser_active=False
        self.engine_flicker=(self.engine_flicker+1)%4
    def shoot(self):
        bullets=[]
        if self.laser_timer>0:
            bullets.append(Bullet(self.rect.centerx,self.rect.top-10,0,-14,'player_laser'))
            return bullets
        levels={1:[(self.rect.centerx,self.rect.top)],2:[(self.rect.centerx-10,self.rect.top),(self.rect.centerx+10,self.rect.top)],
                3:[(self.rect.centerx,self.rect.top),(self.rect.centerx-14,self.rect.top+8),(self.rect.centerx+14,self.rect.top+8)],
                4:[(self.rect.centerx,self.rect.top),(self.rect.centerx-14,self.rect.top+8),(self.rect.centerx+14,self.rect.top+8),(self.rect.centerx-20,self.rect.top+16)],
                5:[(self.rect.centerx,self.rect.top),(self.rect.centerx-10,self.rect.top+6),(self.rect.centerx+10,self.rect.top+6),(self.rect.centerx-18,self.rect.top+12),(self.rect.centerx+18,self.rect.top+12)]}
        for bx,by in levels.get(self.power_level,levels[1]):
            bullets.append(Bullet(bx,by,0,-12,'player'))
        return bullets
    def hit(self):
        if self.invincible_timer>0 or self.shield_timer>0: return False
        self.hp-=1; self.invincible_timer=90
        if self.hp<=0: self.alive=False
        return True
    def draw(self,sf):
        if self.invincible_timer>0 and (pygame.time.get_ticks()//80)%2==0: return
        sf.blit(self.image,self.rect)
        if self.shield_timer>0:
            try:
                sh=pygame.Surface((72,72),pygame.SRCALPHA); pygame.draw.circle(sh,(0,180,255,100),(36,36),34,3)
                sf.blit(sh,sh.get_rect(center=self.rect.center))
            except: pass
        if self.laser_timer>0:
            try:
                col=(0,255,255,150) if self.laser_timer%4<2 else (180,80,255,100)
                ls=pygame.Surface((8,SCREEN_HEIGHT),pygame.SRCALPHA); pygame.draw.rect(ls,col,(0,0,8,self.rect.top))
                sf.blit(ls,ls.get_rect(centerx=self.rect.centerx))
            except: pass
    def draw_hp_bar(self,sf):
        bw=80; bh=10; bx=self.rect.left-2; by=self.rect.top-18
        pygame.draw.rect(sf,(40,40,60),(bx,by,bw,bh),border_radius=3)
        for i in range(self.hp):
            hx=bx+2+i*(bw//self.max_hp); hw=bw//self.max_hp-2
            try: pygame.draw.rect(sf,GREEN if self.hp>1 else RED,(hx,by+1,hw-1,bh-2),border_radius=2)
            except: pass

# ======================== 子弹 ========================
class Bullet:
    _sf={}
    @classmethod
    def _init_surfaces(cls):
        cls._sf={
            'player':(pygame.Surface((6,16),pygame.SRCALPHA),CYAN,4),
            'player_laser':(pygame.Surface((8,SCREEN_HEIGHT),pygame.SRCALPHA),(0,200,255),4),
            'enemy':(pygame.Surface((8,12),pygame.SRCALPHA),RED,4),
            'enemy_fast':(pygame.Surface((6,10),pygame.SRCALPHA),ORANGE,3),
            'enemy_spread':(pygame.Surface((8,12),pygame.SRCALPHA),MAGENTA,4),
            'enemy_homing':(pygame.Surface((10,14),pygame.SRCALPHA),(255,100,200),5),
        }
    def __init__(self,x,y,vx,vy,kind='enemy'):
        if not Bullet._sf: Bullet._init_surfaces()
        self.x=x; self.y=y; self.vx=vx; self.vy=vy; self.kind=kind
        self.active=True; self.alive=True
        surf,color,r=Bullet._sf.get(kind,(pygame.Surface((6,12),pygame.SRCALPHA),RED,3))
        s=surf.copy()
        if kind=='player_laser':
            s.fill(color)
        else:
            try: pygame.draw.ellipse(s,color,s.get_rect())
            except: s.fill(color)
        self.image=s; self.radius=r
        self.rect=s.get_rect(center=(int(x),int(y)))
        self._homing=False
    def update(self):
        if self.kind=='enemy_homing' and hasattr(self,'target'):
            tx,ty=self.target.rect.centerx,self.target.rect.centery
            dx,dy=tx-self.x,ty-self.y; d=math.sqrt(dx*dx+dy*dy)
            if d>0: self.vx+=dx/d*0.4; self.vy+=dy/d*0.4; sp=math.sqrt(self.vx**2+self.vy**2)
            if sp>7: self.vx=7*self.vx/sp; self.vy=7*self.vy/sp; self._homing=True
        self.x+=self.vx; self.y+=self.vy
        self.rect.center=(int(self.x),int(self.y))
        if self.kind=='player_laser':
            self.rect.y=int(self.y-self.rect.height//2)
        if self.y<-50 or self.y>SCREEN_HEIGHT+50 or self.x<-50 or self.x>SCREEN_WIDTH+50: self.alive=False
    def draw(self,sf):
        if self.alive:
            if self.kind=='player_laser':
                r=self.rect.copy(); r.y=0; r.height=sf.get_height()
                try: sf.blit(self.image,r)
                except: pass
            else:
                try: sf.blit(self.image,self.rect)
                except: pass

# ======================== 敌机 ========================
class Enemy:
    SCORES={'small':100,'medium':200,'large':400}
    _imgs={}
    @classmethod
    def _init_imgs(cls):
        if not cls._imgs: cls._imgs={ch:{t:create_enemy_surface(t,ch) for t in ['small','medium','large']} for ch in range(1,6)}
    def __init__(self,etype='small',chapter=1):
        if not Enemy._imgs: Enemy._init_imgs()
        self.type=etype; self.chapter=chapter
        self.image=Enemy._imgs[chapter][etype]
        self.rect=self.image.get_rect()
        self.rect.x=random.randint(20,SCREEN_WIDTH-60)
        self.rect.y=-self.rect.height-10
        self.speed=random.uniform(2.0,3.5)+chapter*0.3
        self.score=Enemy.SCORES[etype]; self.alive=True
        self.shoot_timer=random.randint(60,150);         self.hp={'small':1,'medium':2,'large':4}[etype]
    def update(self,frozen=False):
        if frozen: return True
        self.rect.y+=self.speed
        if self.rect.top>SCREEN_HEIGHT+60: self.alive=False
        self.shoot_timer-=1
        return self.alive
    def shoot(self):
        if self.shoot_timer<=0:
            self.shoot_timer=random.randint(90,180)
            bx=self.rect.centerx; by=self.rect.bottom+4
            if self.type=='large': return [Bullet(bx-15,by,random.uniform(-1.5,1.5),random.uniform(4,6),'enemy'),
                                            Bullet(bx+15,by,random.uniform(-1.5,1.5),random.uniform(4,6),'enemy')]
            elif self.type=='medium': return [Bullet(bx,by,0,random.uniform(3,5.5),'enemy_fast')]
            return [Bullet(bx,by,0,random.uniform(3,5),'enemy')]
        return None
    def hit(self):
        self.hp-=1
        if self.hp<=0:
            self.alive=False; return True
        return False
    def draw(self,sf):
        if self.alive: sf.blit(self.image,self.rect)

enemy_imgs={ch:{t:create_enemy_surface(t,ch) for t in ['small','medium','large']} for ch in range(1,6)}

# ======================== Boss ========================
class Boss:
    """各章节Boss，每章不同血量、攻击模式"""
    # 每章Boss配置
    CONFIGS = {
        1: {'hp': 80,  'score': 3000, 'name': '红色尖兵', 'speed': 1.0, 'color': RED},
        2: {'hp': 150, 'score': 6000, 'name': '紫色利刃', 'speed': 1.2, 'color': PURPLE},
        3: {'hp': 250, 'score': 10000,'name': '棕色重甲', 'speed': 0.8, 'color': BROWN},
        4: {'hp': 400, 'score': 18000,'name': '绿色精英', 'speed': 1.5, 'color': GREEN},
        5: {'hp': 600, 'score': 30000,'name': '黄金终焉', 'speed': 1.8, 'color': GOLD},
    }

    def __init__(self, chapter, player_rect=None):
        self.chapter = chapter
        cfg = self.CONFIGS[chapter]
        self.max_hp = cfg['hp']; self.hp = self.max_hp
        self.score = cfg['score']; self.name = cfg['name']
        self.speed = cfg['speed']; self.color = cfg['color']
        self.image = boss_imgs[chapter]
        self.rect = self.image.get_rect(centerx=SCREEN_WIDTH//2, top=-10)
        self.active = True; self.alive = True
        self.x = self.rect.centerx; self.target_x = SCREEN_WIDTH//2
        self.y = self.rect.centery; self.target_y = 90
        self.phase = 0; self.phase_timer = 0; self.angle = 0
        self.bullet_pattern = 0; self.pattern_timer = 0
        self.move_dir = 1; self.move_timer = 0
        # 追踪目标（玩家对象，供追踪弹使用）
        self.target = player_rect if hasattr(player_rect, 'rect') else None
        # 章节Boss颜色
        colors = {1:RED, 2:PURPLE, 3:BROWN, 4:GREEN, 5:GOLD}
        self.bullet_color = colors[chapter]

    def _fire_chapter_pattern(self):
        """章节Boss专属弹幕模式"""
        ch = self.chapter
        bullets = []
        cx, cy = self.rect.centerx, self.rect.bottom

        if ch == 1:
            # ---- 第1章Boss：十字交叉弹幕 ----
            for ang in [math.pi*0.5, math.pi*0.5+0.3, math.pi*0.5-0.3]:
                bullets.append(Bullet(cx, cy, math.cos(ang)*5, math.sin(ang)*5, 'enemy'))
            for ang in [0, math.pi*0.3, math.pi*0.6, math.pi*0.9, math.pi*1.2]:
                b = Bullet(cx, cy, math.cos(ang)*4, math.sin(ang)*4, 'enemy')
                b.x = cx + math.cos(ang)*20; b.y = cy + math.sin(ang)*20
                b.rect.center = (int(b.x), int(b.y)); bullets.append(b)

        elif ch == 2:
            # ---- 第2章Boss：旋转螺旋弹幕 ----
            for i in range(6):
                ang = self.angle + i * math.pi / 3
                b = Bullet(cx, cy, math.cos(ang)*4.5, math.sin(ang)*4.5, 'enemy_spread')
                bullets.append(b)
            self.angle += 0.25

        elif ch == 3:
            # ---- 第3章Boss：3方向散射弹幕 ----
            for ang in [math.pi*0.5-0.4, math.pi*0.5, math.pi*0.5+0.4]:
                for spd in [3.5, 5.0]:
                    bullets.append(Bullet(cx, cy, math.cos(ang)*spd, math.sin(ang)*spd, 'enemy'))
            for side in [-1, 1]:
                bx = cx + side*80; by = cy - 20
                for i in range(4):
                    ang = math.pi*0.5 + side*0.3*i
                    bullets.append(Bullet(bx, by, math.cos(ang)*4, math.sin(ang)*4, 'enemy_spread'))

        elif ch == 4:
            # ---- 第4章Boss：追踪弹 + 散布弹 ----
            if self.pattern_timer % 90 == 0:
                b = Bullet(cx, cy, 0, 3, 'enemy_homing')
                if self.target: b.target = self.target
                bullets.append(b)
            for ang in [math.pi*0.5-0.5, math.pi*0.5-0.25, math.pi*0.5, math.pi*0.5+0.25, math.pi*0.5+0.5]:
                if self.pattern_timer % 25 == 0:
                    bullets.append(Bullet(cx, cy, math.cos(ang)*4, math.sin(ang)*4, 'enemy_spread'))

        elif ch == 5:
            # ---- 第5章Boss：全屏乱射 ----
            for i in range(8):
                ang = self.angle + i * math.pi / 4
                b = Bullet(cx, cy, math.cos(ang)*3.5, math.sin(ang)*3.5, 'enemy')
                bullets.append(b)
            if self.pattern_timer % 60 == 0:
                for ang in [math.pi*0.5-0.6, math.pi*0.5+0.6]:
                    for j in range(3):
                        delay = j * 10
                        bx = cx + math.cos(ang)*10; by = cy + math.sin(ang)*10 + delay
                        b = Bullet(bx, by, 0, 4.5, 'enemy_fast'); bullets.append(b)
            self.angle += 0.15

        return bullets

    def update(self, player_rect=None):
        # 入场
        if self.y < self.target_y:
            self.y += 2.5; self.rect.y = int(self.y)
            return []
        # 移动
        self.move_timer += 1
        if self.move_timer > 40:
            self.move_timer = 0; self.move_dir *= -1
        self.x += self.speed * self.move_dir
        self.x = max(110, min(SCREEN_WIDTH-110, self.x))
        self.rect.centerx = int(self.x)
        self.angle += 0.04; self.pattern_timer += 1
        # 射击
        bullets = self._fire_chapter_pattern()
        return bullets

    def hit(self):
        self.hp -= 1
        if self.hp <= 0:
            self.alive = False; self.active = False
            return True
        return False

    def draw(self, sf):
        if self.alive:
            sf.blit(self.image, self.rect)
            # 血条
            bw = 180; bh = 12; bx = self.rect.centerx - bw//2; by = self.rect.bottom + 8
            pygame.draw.rect(sf, (40,40,60), (bx, by, bw, bh), border_radius=4)
            ratio = max(0, self.hp / self.max_hp)
            try:
                pg = (bx+2, by+2, int((bw-4)*ratio), bh-4)
                if ratio > 0.6: col = GREEN
                elif ratio > 0.3: col = YELLOW
                else: col = RED
                pygame.draw.rect(sf, col, pg, border_radius=3)
            except: pass
            # BOSS名
            nm = font_small.render(self.name, True, CHAPTER_THEMES[self.chapter]['accent'])
            sf.blit(nm, nm.get_rect(centerx=self.rect.centerx, bottom=self.rect.top - 6))

# Boss图片
boss_imgs = {ch: create_boss_surface(ch) for ch in range(1,6)}

# ======================== 距离追踪 ========================
class DistanceTracker:
    def __init__(self):
        self.distance = 0.0
        self.base_speed = 200  # 提升基准速度，确保Boss能在合理时间内出现
        self.last_update = pygame.time.get_ticks()
    def reset(self):
        self.distance = 0.0; self.last_update = pygame.time.get_ticks()
    def update(self, chapter, speed_boost=False):
        now = pygame.time.get_ticks(); dt = (now - self.last_update) / 1000.0
        self.last_update = now
        mult = 1.0 + chapter * 0.15
        if speed_boost: mult *= 1.5
        self.distance += self.base_speed * mult * dt
    @property
    def display_distance(self):
        if self.distance >= 1000: return f"{self.distance/1000:.2f} km"
        return f"{int(self.distance)} m"

# ======================== 排行榜 ========================
class Leaderboard:
    def __init__(self, fp=LEADERBOARD_FILE):
        self.fp = fp; self.entries = []; self.load()
    def load(self):
        if os.path.exists(self.fp):
            try:
                with open(self.fp, 'r', encoding='utf-8') as f:
                    data = json.load(f); self.entries = data.get('entries', [])
            except: self.entries = []
    def save(self):
        try:
            os.makedirs(os.path.dirname(self.fp), exist_ok=True)
            with open(self.fp, 'w', encoding='utf-8') as f:
                json.dump({'entries': self.entries}, f, ensure_ascii=False, indent=2)
        except: pass
    def add_entry(self, name, score, dist, kills, chapter):
        e = {'name': name[:10], 'score': int(score), 'distance': round(dist, 1), 'kills': kills,
             'chapter': chapter, 'date': datetime.now().strftime('%Y-%m-%d %H:%M'), 'mode': getattr(self, '_mode', 'story')}
        self.entries.append(e); self.entries.sort(key=lambda x: x['score'], reverse=True)
        self.entries = self.entries[:10]; self.save()
    def get_top_n(self, n=10): return self.entries[:n]
    def is_high_score(self, score):
        if len(self.entries) < 10: return True
        return score > self.entries[-1]['score']
    @property
    def top_score(self): return self.entries[0]['score'] if self.entries else 0

# ======================== 章节解锁进度 ========================
class ChapterProgress:
    """管理故事模式章节解锁进度"""
    def __init__(self, fp=PROGRESS_FILE):
        self.fp = fp
        self.unlocked_chapters = set()  # 已解锁的章节编号
        self.defeated_bosses = set()     # 已击败Boss的章节
        self.load()

    def load(self):
        """从文件加载进度"""
        if os.path.exists(self.fp):
            try:
                with open(self.fp, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.unlocked_chapters = set(data.get('unlocked', [1]))  # 默认只解锁第1章
                    self.defeated_bosses = set(data.get('defeated', []))
            except:
                self.unlocked_chapters = {1}
                self.defeated_bosses = set()
        else:
            # 首次运行：只解锁第1章
            self.unlocked_chapters = {1}
            self.defeated_bosses = set()

    def save(self):
        """保存进度到文件"""
        try:
            with open(self.fp, 'w', encoding='utf-8') as f:
                json.dump({
                    'unlocked': sorted(list(self.unlocked_chapters)),
                    'defeated': sorted(list(self.defeated_bosses)),
                }, f, ensure_ascii=False, indent=2)
        except:
            pass

    def is_unlocked(self, chapter):
        """章节是否已解锁"""
        return chapter in self.unlocked_chapters

    def unlock_next(self, after_chapter):
        """击败Boss后解锁下一章节"""
        next_ch = after_chapter + 1
        if next_ch <= 5:
            self.unlocked_chapters.add(next_ch)
            self.defeated_bosses.add(after_chapter)
            self.save()
            return True
        return False

    def reset_all(self):
        """重置所有进度（重新开始）"""
        self.unlocked_chapters = {1}
        self.defeated_bosses = set()
        self.save()

# ======================== 主游戏类 ========================
class Game:
    # 每章Boss触发距离（故事模式）
    # 大幅降低，确保每章能在 ~15-30秒内遇到Boss
    STORY_BOSS_DISTANCES = {
        1: 800,   # 第1章Boss：800m（约8秒）
        2: 1500,  # 第2章Boss：1500m
        3: 2500,  # 第3章Boss：2500m
        4: 4000,  # 第4章Boss：4000m
        5: 6000,  # 第5章Boss：6000m
    }
    # 挑战模式Boss触发间隔（每波Boss之间）
    CHALLENGE_BOSS_INTERVAL = 1800  # 每1800m一波Boss

    def __init__(self):
        self.state = 'menu'          # menu | story_select | challenge | playing | paused | enter_name | leaderboard
        self.game_mode = None        # 'story' | 'challenge'
        self.select_chapter = 1      # 故事模式选中的章节

        self.player = Player()
        self.enemies = []; self.player_bullets = []; self.enemy_bullets = []
        self.explosions = []; self.particles_list = []; self.trail_particles = []
        self.powerups = []; self.obstacles = []; self.star_field = StarField()
        self.leaderboard = Leaderboard()
        # 章节解锁进度（类属性，_full_reset时不会被清除）
        if not hasattr(Game, '_chapter_progress'):
            Game._chapter_progress = ChapterProgress()
        self.chapter_progress = Game._chapter_progress  # 引用，始终指向同一个对象
        self.score = 0; self.high_score = self.leaderboard.top_score
        self.chapter = 1; self.enemy_spawn_timer = 0; self.obstacle_spawn_timer = 0
        self.enemies_killed = 0; self.combo = 0; self.combo_timer = 0; self.combo_max = 0
        self.screen_shake = 0; self.bombs_available = 2; self.freeze_timer = 0
        self.distance_tracker = DistanceTracker()
        self.game_time = 0; self.input_name = "PILOT"; self.name_cursor_visible = True
        self.name_cursor_timer = 0; self.current_rank = 0
        self.notification_queue = []; self.level_up_display_timer = 0

        # Boss系统
        self.boss = None; self.boss_warning_timer = 0; self.boss_intro_timer = 0
        self.chapter_complete_timer = 0; self.chapter_complete_shown = False
        self.victory = False

        # 挑战模式专用
        self.challenge_boss_count = 0   # 已击败的Boss数量（挑战模式）
        self.challenge_next_boss_dist = self.CHALLENGE_BOSS_INTERVAL  # 下次Boss距离

        # Boss预警系统（60%距离时提前告知）
        self.boss_approaching_timer = 0

        # 射击冷却
        self.shoot_cooldown = 0

        # 菜单按钮（动态绑定）
        self._menu_rects = {}

    # ======================== 启动游戏 ========================
    def _start_story(self, chapter=1):
        """启动故事模式（从选定章节开始）"""
        self._full_reset()
        self.game_mode = 'story'
        self.chapter = chapter

    def _start_challenge(self):
        """启动挑战模式"""
        self._full_reset()
        self.game_mode = 'challenge'
        self.chapter = 1  # 挑战模式用章节1的配色，但循环使用所有Boss
        self.challenge_boss_count = 0
        self.challenge_next_boss_dist = self.CHALLENGE_BOSS_INTERVAL

    def _full_reset(self):
        """完整重置游戏状态"""
        old_high = self.high_score
        # 保留排行榜
        lb = self.leaderboard
        # 保留菜单按钮
        old_rects = self._menu_rects
        self.__dict__.clear()
        self.__init__()
        self.leaderboard = lb
        self.high_score = max(old_high, self.leaderboard.top_score)
        self._menu_rects = old_rects
        self.state = 'playing'
        self.distance_tracker.reset()
        self.leaderboard._mode = self.game_mode

    def _retry_same(self):
        """在同一模式下重试（保留章节）"""
        mode = self.game_mode
        ch = self.chapter
        lb = self.leaderboard
        old_high = self.high_score
        old_rects = self._menu_rects
        self.__init__()
        self.leaderboard = lb
        self.high_score = max(old_high, self.leaderboard.top_score)
        self._menu_rects = old_rects
        self.game_mode = mode
        self.chapter = ch
        if mode == 'challenge':
            self.challenge_boss_count = 0
            self.challenge_next_boss_dist = self.CHALLENGE_BOSS_INTERVAL
        self.state = 'playing'
        self.distance_tracker.reset()
        self.leaderboard._mode = mode

    # ======================== 敌机生成 ========================
    def spawn_enemy(self):
        self.enemy_spawn_timer -= 1
        if self.enemy_spawn_timer <= 0:
            r = random.random()
            ch = self.chapter
            if ch == 1:
                etype = 'small' if r < 0.8 else 'medium'
            elif ch == 2:
                etype = 'small' if r < 0.6 else ('medium' if r < 0.9 else 'large')
            else:
                etype = 'small' if r < 0.4 else ('medium' if r < 0.75 else 'large')
            self.enemies.append(Enemy(etype, ch))
            base_int = max(50 - ch * 4, 18)
            self.enemy_spawn_timer = base_int + random.randint(0, 25)

    def spawn_obstacle(self):
        self.obstacle_spawn_timer -= 1
        if self.obstacle_spawn_timer <= 0:
            chance = min(0.03 + self.chapter * 0.008, 0.10)
            if random.random() < chance: self.obstacles.append(Obstacle())
            interval = max(140 - self.chapter * 10, 60)
            self.obstacle_spawn_timer = interval + random.randint(0, 50)

    # ======================== 碰撞检测 ========================
    def check_collisions(self):
        # 玩家子弹 vs 敌机
        for bullet in [b for b in self.player_bullets if b.active]:
            for enemy in [e for e in self.enemies if e.alive]:
                if bullet.rect.colliderect(enemy.rect):
                    bullet.active = False
                    try: self.player_bullets.remove(bullet)
                    except: pass
                    if enemy.hit():
                        cb = 1 + self.combo * 0.15; self.score += int(enemy.score * cb)
                        self.enemies_killed += 1; self.combo += 1; self.combo_timer = 90
                        if self.combo > self.combo_max: self.combo_max = self.combo
                        self.explosions.append(Explosion(enemy.rect.centerx, enemy.rect.centery, 1.5))
                        self.screen_shake = 4
                        if random.random() < 0.22: self.powerups.append(PowerUp(enemy.rect.centerx, enemy.rect.centery))
                        try:
                            if explosion_snd: explosion_snd.play()
                        except: pass
                    break

        # 玩家子弹 vs Boss
        if self.boss and self.boss.alive and self.boss.active:
            for bullet in [b for b in self.player_bullets if b.active]:
                if bullet.rect.colliderect(self.boss.rect):
                    bullet.active = False
                    try: self.player_bullets.remove(bullet)
                    except: pass
                    if self.boss.hit():
                        # Boss被击杀
                        self.score += self.boss.score
                        for _ in range(5):
                            self.explosions.append(Explosion(
                                self.boss.rect.centerx + random.uniform(-40, 40),
                                self.boss.rect.centery + random.uniform(-30, 30), 2.0))
                        self.screen_shake = 12
                        try:
                            if explosion_snd: explosion_snd.play()
                        except: pass
                        self._on_boss_defeated()
                    break

        # 玩家子弹 vs 障碍物
        for bullet in [b for b in self.player_bullets if b.active]:
            for obs in [o for o in self.obstacles if o.alive]:
                if bullet.rect.colliderect(obs.rect):
                    bullet.active = False
                    try: self.player_bullets.remove(bullet)
                    except: pass
                    if obs.type == 'asteroid':
                        obs.alive = False; self.score += obs.score
                        self.explosions.append(Explosion(obs.rect.centerx, obs.rect.centery, 1.3, BROWN))
                        self.screen_shake = 2
                        for _ in range(8):
                            self.particles_list.append(Particle(obs.rect.centerx, obs.rect.centery,
                                color=random.choice([BROWN, GRAY, ORANGE])))
                    break

        # 敌机子弹 vs 玩家
        for bullet in [b for b in self.enemy_bullets if b.active]:
            if bullet.rect.colliderect(self.player.rect) and self.player.alive:
                bullet.active = False
                try: self.enemy_bullets.remove(bullet)
                except: pass
                if self.player.hit():
                    self.explosions.append(Explosion(self.player.rect.centerx, self.player.rect.centery, 0.8))
                    self.screen_shake = 5; self.combo = 0
                    try:
                        if hit_snd: hit_snd.play()
                    except: pass

        # Boss子弹 vs 玩家
        for bullet in [b for b in self.enemy_bullets if b.active]:
            if bullet.rect.colliderect(self.player.rect) and self.player.alive:
                bullet.active = False
                try: self.enemy_bullets.remove(bullet)
                except: pass
                if self.player.hit():
                    self.explosions.append(Explosion(self.player.rect.centerx, self.player.rect.centery, 0.8))
                    self.screen_shake = 5; self.combo = 0
                    try:
                        if hit_snd: hit_snd.play()
                    except: pass

        # 敌机 vs 玩家
        for enemy in [e for e in self.enemies if e.alive]:
            if enemy.rect.colliderect(self.player.rect) and self.player.alive:
                if self.player.hit():
                    enemy.alive = False
                    self.explosions.append(Explosion(enemy.rect.centerx, enemy.rect.centery, 1.2))
                    self.explosions.append(Explosion(self.player.rect.centerx, self.player.rect.centery, 0.8))
                    self.screen_shake = 6; self.combo = 0

        # Boss vs 玩家
        if self.boss and self.boss.alive and self.boss.active:
            if self.boss.rect.colliderect(self.player.rect) and self.player.alive:
                if self.player.hit():
                    self.screen_shake = 8; self.combo = 0

        # 障碍物 vs 玩家
        for obs in [o for o in self.obstacles if o.alive]:
            if obs.rect.colliderect(self.player.rect) and self.player.alive:
                for _ in range(obs.damage):
                    if self.player.alive and self.player.hit(): pass
                if obs.type != 'barrier':
                    obs.alive = False
                    self.explosions.append(Explosion(obs.rect.centerx, obs.rect.centery, 1.0, ORANGE))
                self.screen_shake = 4; self.combo = 0

        # 道具拾取
        for pu in self.powerups[:]:
            if pu.rect.colliderect(self.player.rect):
                pu.apply(self.player, game=self)
                if pu.type == 'bomb': self.use_bomb()
                tn = {'power': '火力提升!', 'heal': '生命回复!', 'bomb': '炸弹!', 'shield': '护盾激活!',
                      'speed': '加速启动!', 'magnet': '磁铁吸力!', 'freeze': '冰冻减速!', 'score': '+500分!', 'laser': '激光炮!'}
                self.show_notification(tn.get(pu.type, ''))
                try: self.powerups.remove(pu)
                except: pass

    def _on_boss_defeated(self):
        """Boss被击杀"""
        self.challenge_boss_count += 1  # 挑战模式计数

        if self.game_mode == 'story':
            # 故事模式：击败Boss，解锁下一章节
            if self.chapter < 5:
                # 解锁下一章节
                unlocked = self.chapter_progress.unlock_next(self.chapter)
                self.chapter += 1
                if unlocked:
                    self.show_notification(f"第{self.chapter}章 已解锁!")
                else:
                    self.show_notification(f"第{self.chapter}章 开始!")
                self.boss = None
                self.chapter_complete_shown = True
                self.chapter_complete_timer = 120
            else:
                # 通关！第5章Boss被击败
                self.chapter_progress.unlock_next(5)  # 标记第5章完成
                self.victory = True
                self.boss = None
                self.state = 'enter_name'
        else:
            # 挑战模式：击败后继续，下一波Boss在更远处
            self.boss = None
            # 随时间增长Boss间隔，但有上限
            interval = min(self.CHALLENGE_BOSS_INTERVAL + self.challenge_boss_count * 100, 4000)
            self.challenge_next_boss_dist = self.distance_tracker.distance + interval
            self.show_notification(f"第{self.challenge_boss_count}波Boss 已击败! 继续!")

    # ======================== 道具效果 ========================
    def use_bomb(self):
        for _ in range(12):
            self.particles_list.append(Particle(
                random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT),
                color=random.choice([WHITE, YELLOW, CYAN, ORANGE])))
        for enemy in self.enemies: enemy.alive = False
        if self.boss and self.boss.alive:
            for _ in range(3):
                self.explosions.append(Explosion(
                    self.boss.rect.centerx + random.uniform(-30, 30),
                    self.boss.rect.centery + random.uniform(-20, 20), 1.5))
            self.boss.hp -= 3
            if self.boss.hp <= 0:
                self.score += self.boss.score
                self._on_boss_defeated()
        self.enemy_bullets.clear()
        self.freeze_timer = 30
        self.screen_shake = 8

    def show_notification(self, text):
        self.notification_queue.append({'text': text, 'timer': 120})

    def update_notifications(self):
        for n in self.notification_queue[:]:
            n['timer'] -= 1
            if n['timer'] <= 0: self.notification_queue.remove(n)

    # ======================== 主更新循环 ========================
    def update(self):
        if self.state != 'playing': return

        keys = pygame.key.get_pressed()
        self.game_time += 1
        self.star_field.update()
        self.player.update(keys)

        # 尾迹
        if self.player.alive and self.game_time % 3 == 0:
            self.trail_particles.append(TrailParticle(
                self.player.rect.centerx + random.randint(-6, 6),
                self.player.rect.bottom - 5,
                color=ORANGE if self.player.engine_flicker < 2 else YELLOW))

        # 射击（带冷却）
        if keys[pygame.K_SPACE] and self.shoot_cooldown <= 0:
            nb = self.player.shoot(); self.player_bullets.extend(nb)
            self.shoot_cooldown = 10  # 约6发/秒
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        # 更新子弹
        for b in self.player_bullets: b.update()
        for b in self.enemy_bullets: b.update()
        self.player_bullets = [b for b in self.player_bullets if b.active]
        self.enemy_bullets = [b for b in self.enemy_bullets if b.active]

        # 碰撞检测（核心！必须每帧调用）
        self.check_collisions()

        # 更新距离
        self.distance_tracker.update(self.chapter, self.player.speed_boost)
        dist = self.distance_tracker.distance

        # ======================== Boss触发逻辑 ========================
        if not self.boss:
            if self.game_mode == 'story':
                # 故事模式：特定章节Boss
                boss_dist = self.STORY_BOSS_DISTANCES.get(self.chapter, 999999)
                warn_dist = int(boss_dist * 0.60)  # 60%距离时预警

                # 提前预警提示
                if dist >= warn_dist and self.boss_approaching_timer == 0 and dist < boss_dist:
                    self.show_notification(f"BOSS即将来袭! [{boss_dist}m]")
                    self.boss_approaching_timer = 180

                if self.boss_approaching_timer > 0:
                    self.boss_approaching_timer -= 1

                if dist >= boss_dist and not self.chapter_complete_shown and self.boss_warning_timer == 0:
                    self.boss_warning_timer = 120  # 2秒警告动画（仅设置一次）

            elif self.game_mode == 'challenge':
                # 挑战模式：固定间隔Boss
                warn_dist = int(self.challenge_next_boss_dist * 0.60)
                if dist >= warn_dist and self.boss_approaching_timer == 0 and dist < self.challenge_next_boss_dist:
                    self.show_notification(f"BOSS即将来袭! [{int(self.challenge_next_boss_dist)}m]")
                    self.boss_approaching_timer = 180
                if self.boss_approaching_timer > 0:
                    self.boss_approaching_timer -= 1

                if dist >= self.challenge_next_boss_dist and self.boss_warning_timer == 0:
                    self.boss_warning_timer = 120

        # Boss预警计时
        if self.boss_warning_timer > 0:
            self.boss_warning_timer -= 1
            if self.boss_warning_timer == 0:
                # 决定使用哪个章节Boss
                if self.game_mode == 'story':
                    boss_ch = self.chapter
                else:
                    # 挑战模式：循环使用1-5章节Boss
                    boss_ch = (self.challenge_boss_count % 5) + 1
                self.boss = Boss(boss_ch, self.player.rect)
                self.boss.target = self.player  # 让Boss可以追踪玩家位置
                self.boss_intro_timer = 90
                self.boss_approaching_timer = 0

        # Boss入场/更新
        if self.boss and self.boss.active:
            if self.boss_intro_timer > 0:
                self.boss_intro_timer -= 1
                self.boss.update(self.player.rect)
            else:
                nb = self.boss.update(self.player.rect)
                if nb:
                    for b in nb: self.enemy_bullets.append(b)

        # 章节完成动画
        if self.chapter_complete_timer > 0:
            self.chapter_complete_timer -= 1
            if self.chapter_complete_timer == 0:
                self.chapter_complete_shown = False

        # 生成敌机（Boss战时减少刷新）
        if not self.boss or (self.boss and not self.boss.active):
            self.spawn_enemy()
            self.spawn_obstacle()

        # 更新敌机
        is_frz = self.freeze_timer > 0
        for e in self.enemies:
            e.update(frozen=is_frz)
            bullet = e.shoot()
            if bullet and not is_frz: self.enemy_bullets.extend(bullet)
        self.enemies = [e for e in self.enemies if e.alive and e.rect.top <= SCREEN_HEIGHT + 50]

        # 更新障碍物
        self.obstacles = [o for o in self.obstacles if o.update() and o.alive]

        # 更新道具
        self.powerups = [p for p in self.powerups if p.update() and p.alive]

        # 更新爆炸
        for ex in self.explosions[:]: ex.update()
        self.explosions = [ex for ex in self.explosions if ex.alive]

        # 粒子限制
        self.particles_list = [p for p in self.particles_list if p.update()]
        if len(self.particles_list) > 150: self.particles_list = self.particles_list[-150:]
        self.trail_particles = [p for p in self.trail_particles if p.update()]
        if len(self.trail_particles) > 80: self.trail_particles = self.trail_particles[-80:]
        if len(self.explosions) > 15: self.explosions = self.explosions[-15:]

        if self.screen_shake > 0: self.screen_shake -= 1
        if self.combo_timer > 0: self.combo_timer -= 1
        else: self.combo = 0
        if self.level_up_display_timer > 0: self.level_up_display_timer -= 1
        self.update_notifications()
        if self.freeze_timer > 0: self.freeze_timer -= 1

        # 磁铁效果
        if self.player.magnet_active:
            mr = getattr(self.player, 'magnet_range', 150)
            for pu in self.powerups:
                dx = self.player.rect.centerx - pu.x; dy = self.player.rect.centery - pu.y
                d = math.sqrt(dx*dx+dy*dy)
                if d < mr and d > 0:
                    pu.x += dx/d*5; pu.y += dy/d*5; pu.rect.center = (int(pu.x), int(pu.y))

        # 玩家死亡检测
        if not self.player.alive:
            self.state = 'enter_name'

        # 挑战模式HUD特殊信息
        if self.game_mode == 'challenge':
            # 显示已击败Boss数量
            pass

    # ======================== HUD绘制 ========================
    def draw_hud(self, sf):
        # 背景
        pygame.draw.rect(sf, (0, 0, 0, 120), (0, 0, SCREEN_WIDTH, 58))
        pygame.draw.line(sf, CHAPTER_THEMES[self.chapter]['accent'], (0, 58), (SCREEN_WIDTH, 58), 2)

        # 分数
        sf.blit(font_tiny.render("SCORE", True, SILVER), (8, 4))
        sf.blit(font_small.render(f"{int(self.score):,}", True, YELLOW), (8, 20))

        # 距离
        sf.blit(font_tiny.render("DISTANCE", True, SILVER), (140, 4))
        sf.blit(font_small.render(self.distance_tracker.display_distance, True, CYAN), (140, 20))

        # 章节/模式
        mode_label = f"[挑战:{self.challenge_boss_count}波]" if self.game_mode == 'challenge' else f"第{self.chapter}章"
        try:
            mc = CHAPTER_THEMES[self.chapter]['accent']
        except:
            mc = GOLD
        sf.blit(font_small.render(mode_label, True, mc), (300, 10))

        # 生命
        for i in range(self.player.max_hp):
            x = 8 + i * 28; y = 44
            col = GREEN if i < self.player.hp else (40, 40, 60)
            pygame.draw.rect(sf, col, (x, y, 22, 10), border_radius=3)

        # 炸弹
        for i in range(self.bombs_available):
            bx = SCREEN_WIDTH - 30 - i * 28; by = 44
            pygame.draw.circle(sf, RED, (bx, by + 5), 9)
            try:
                bt = font_tiny.render("B", True, WHITE); sf.blit(bt, bt.get_rect(center=(bx, by + 5)))
            except: pass

        # Combo
        if self.combo > 1:
            try:
                ct = font_medium.render(f"×{self.combo} COMBO", True, ORANGE)
                sf.blit(ct, ct.get_rect(centerx=SCREEN_WIDTH//2, top=62))
            except: pass

        # Boss预警横幅
        if self.boss_warning_timer > 0 and self.boss is None:
            alpha = min(255, (120 - self.boss_warning_timer) * 4)
            try:
                ps = pygame.Surface((SCREEN_WIDTH, 50), pygame.SRCALPHA)
                pygame.draw.rect(ps, (200, 0, 0, alpha // 2), ps.get_rect(), border_radius=6)
                t = font_large.render("! BOSS APPROACHING !", True, (255, 255, 255, alpha))
                ps.blit(t, t.get_rect(center=ps.get_rect().center))
                sf.blit(ps, (0, SCREEN_HEIGHT // 2 - 25))
            except: pass

        # Boss来袭预警文字（60%距离时）
        if self.boss_approaching_timer > 0 and self.boss is None:
            alpha2 = min(200, self.boss_approaching_timer * 2)
            try:
                ap = pygame.Surface((SCREEN_WIDTH, 40), pygame.SRCALPHA)
                t2 = font_medium.render("前方发现BOSS信号!", True, (255, 200, 0, alpha2))
                ap.blit(t2, t2.get_rect(center=ap.get_rect().center))
                sf.blit(ap, (0, SCREEN_HEIGHT // 2 - 100))
            except: pass

        # 章节完成提示
        if self.chapter_complete_timer > 0:
            alpha3 = min(255, self.chapter_complete_timer * 3)
            try:
                cp = pygame.Surface((SCREEN_WIDTH, 60), pygame.SRCALPHA)
                msg = f"第{self.chapter-1}章 CLEAR! 第{self.chapter}章 开始!"
                t3 = font_large.render(msg, True, (0, 255, 100, alpha3))
                cp.blit(t3, t3.get_rect(center=cp.get_rect().center))
                sf.blit(cp, (0, SCREEN_HEIGHT // 2 - 30))
            except: pass

        # 通知队列
        for i, n in enumerate(self.notification_queue[:3]):
            nt = font_medium.render(n['text'], True, GOLD)
            nr = nt.get_rect(centerx=SCREEN_WIDTH // 2, top=80 + i * 40)
            if n['timer'] > 90:
                alpha_n = (120 - n['timer']) * 6
            else:
                alpha_n = n['timer'] * 4
            alpha_n = max(0, min(255, alpha_n))
            try:
                ns = pygame.Surface((nr.width + 20, nr.height + 8), pygame.SRCALPHA)
                pygame.draw.rect(ns, (0, 0, 0, alpha_n // 3), ns.get_rect(), border_radius=6)
                ns.blit(nt, (10, 4)); sf.blit(ns, ns.get_rect(centerx=SCREEN_WIDTH//2, top=80 + i * 40))
            except: pass

        # 挑战模式Boss进度条
        if self.game_mode == 'challenge' and not self.boss:
            pg = self.distance_tracker.distance / self.challenge_next_boss_dist
            pg = min(1.0, pg)
            bw = SCREEN_WIDTH - 20; bh = 8
            bx2 = 10; by2 = SCREEN_HEIGHT - 20
            pygame.draw.rect(sf, (30, 30, 50), (bx2, by2, bw, bh), border_radius=4)
            try:
                pygame.draw.rect(sf, RED, (bx2, by2, int(bw * pg), bh), border_radius=4)
            except: pass
            try:
                bt2 = font_tiny.render(f"下一波Boss: {self.distance_tracker.display_distance} / {int(self.challenge_next_boss_dist)}m", True, SILVER)
                sf.blit(bt2, bt2.get_rect(centerx=SCREEN_WIDTH//2, top=by2 - 16))
            except: pass

        # 玩家HP条（上方）
        self.player.draw_hp_bar(sf)

    # ======================== 菜单绘制 ========================
    def draw_menu(self, sf):
        self.star_field.update(); self.star_field.draw(sf)
        # 背景遮罩
        if not hasattr(Game, '_menu_ov'):
            Game._menu_ov = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            Game._menu_ov.fill((0, 0, 0, 140))
        sf.blit(Game._menu_ov, (0, 0))

        # 标题
        ty = 120 + math.sin(pygame.time.get_ticks() * 0.002) * 6
        for off in range(4, 0, -1):
            try:
                ss = font_title.render("飞机大战", True, (*CYAN[:3], 15 + 12 * off))
                sf.blit(ss, ss.get_rect(centerx=SCREEN_WIDTH // 2, y=ty + off * 2))
            except: pass
        try:
            title = font_title.render("飞机大战", True, WHITE)
            sf.blit(title, title.get_rect(centerx=SCREEN_WIDTH // 2, y=ty))
            ver = font_small.render("v3.1 双模式章节Boss", True, GOLD)
            sf.blit(ver, ver.get_rect(centerx=SCREEN_WIDTH // 2, y=ty + 58))
        except: pass

        # 模式选择按钮
        btn_data = [
            ("1  故事模式", "STORY MODE", CYAN,    (130, 220, 280, 60)),
            ("2  挑战模式", "CHALLENGE MODE", RED, (130, 300, 280, 60)),
            ("3  排行榜", "RANKING", ORANGE,       (130, 380, 280, 60)),
        ]
        self._menu_rects = {}
        mp = pygame.mouse.get_pos()
        for i, (cn, en, col, (bx, by, bw, bh)) in enumerate(btn_data):
            rect = pygame.Rect(bx, by, bw, bh)
            hovered = rect.collidepoint(mp)
            bg = (40, 70, 120) if hovered else (15, 25, 55)
            pygame.draw.rect(sf, bg, rect, border_radius=10)
            pygame.draw.rect(sf, col, rect, 2, border_radius=10)
            try:
                t1 = font_medium.render(cn, True, col if hovered else WHITE)
                sf.blit(t1, t1.get_rect(center=rect.center))
                t2 = font_tiny.render(en, True, col if hovered else LIGHT_GRAY)
                sf.blit(t2, t2.get_rect(centerx=rect.centerx, top=rect.bottom - 18))
            except: pass
            key_map = {0: pygame.K_1, 1: pygame.K_2, 2: pygame.K_3}
            key_near = False
            try:
                pressed = pygame.key.get_pressed()
                if pressed[key_map[i]]: key_near = True
            except: pass
            if hovered or key_near:
                pygame.draw.rect(sf, col, rect.inflate(4, 4), 3, border_radius=12)
            self._menu_rects[cn[:2]] = rect

        # 故事模式说明
        try:
            info_box = pygame.Surface((380, 80), pygame.SRCALPHA)
            info_box.fill((0, 0, 0, 120))
            info_lines = [
                (f"故事模式: 选择章节，击败每章Boss通关", CYAN),
                (f"挑战模式: 无限距离，随机Boss循环，看你能飞多远", RED),
            ]
            for j, (text, col2) in enumerate(info_lines):
                t = font_small.render(text, True, col2)
                info_box.blit(t, t.get_rect(centerx=190, top=8 + j * 36))
            ir = info_box.get_rect(centerx=SCREEN_WIDTH // 2, top=455)
            sf.blit(info_box, ir)
        except: pass

        # 最高分
        if self.high_score > 0:
            if not hasattr(Game, '_hs_bx'):
                Game._hs_bx = pygame.Surface((200, 40), pygame.SRCALPHA); Game._hs_bx.fill((100, 50, 0, 150))
            hx = Game._hs_bx; hxr = hx.get_rect(centerx=SCREEN_WIDTH // 2, y=550)
            pygame.draw.rect(sf, GOLD, hxr, 2, border_radius=6); sf.blit(hx, hxr)
            try:
                hs = font_medium.render(f"TOP: {self.high_score:,}", True, GOLD)
                sf.blit(hs, hs.get_rect(centerx=SCREEN_WIDTH // 2, centery=hxr.centery))
            except: pass

        # 操作说明
        try:
            instrs = [("方向键/WASD 移动 | SPACE 射击 | B 炸弹 | P 暂停", LIGHT_GRAY)]
            for i, (line, col2) in enumerate(instrs):
                t = font_small.render(line, True, col2); sf.blit(t, t.get_rect(centerx=SCREEN_WIDTH // 2, y=600 + i * 26))
        except: pass

        try:
            ft = font_tiny.render("by 阿爪 🦞  2026", True, GRAY); sf.blit(ft, ft.get_rect(centerx=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT - 25))
        except: pass

    # ======================== 故事模式章节选择 ========================
    def draw_story_select(self, sf):
        self.star_field.update(); self.star_field.draw(sf)
        if not hasattr(Game, '_ss_ov'):
            Game._ss_ov = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            Game._ss_ov.fill((0, 0, 0, 160))
        sf.blit(Game._ss_ov, (0, 0))

        try:
            # 标题
            title = font_large.render("故事模式 · 选择章节", True, WHITE)
            sf.blit(title, title.get_rect(centerx=SCREEN_WIDTH // 2, y=40))
            sub = font_small.render("击败Boss解锁新章节", True, LIGHT_GRAY)
            sf.blit(sub, sub.get_rect(centerx=SCREEN_WIDTH // 2, y=85))
        except: pass

        mp = pygame.mouse.get_pos()
        self._menu_rects = {}

        # 章节按钮（5个）
        boss_names = {1: '红色尖兵', 2: '紫色利刃', 3: '棕色重甲', 4: '绿色精英', 5: '黄金终焉'}
        boss_dists = {1: '800m', 2: '1500m', 3: '2500m', 4: '4000m', 5: '6000m'}

        for i, ch in enumerate(range(1, 6)):
            row = i // 3; col_idx = i % 3
            bx = 45 + col_idx * 165; by = 130 + row * 220
            rect = pygame.Rect(bx, by, 150, 190)
            is_unlocked = self.chapter_progress.is_unlocked(ch)
            is_defeated = ch in self.chapter_progress.defeated_bosses
            hovered = rect.collidepoint(mp) and is_unlocked
            theme = CHAPTER_THEMES[ch]

            if not is_unlocked:
                # 锁定状态：灰色遮罩
                bg = (15, 15, 25)
                pygame.draw.rect(sf, bg, rect, border_radius=12)
                pygame.draw.rect(sf, (60, 60, 80), rect, 1, border_radius=12)
                try:
                    lock_title = font_title.render(str(ch), True, (50, 50, 70))
                    sf.blit(lock_title, lock_title.get_rect(centerx=rect.centerx, y=rect.y + 10))
                    nm = font_small.render(f"第{ch}章", True, (60, 60, 80))
                    sf.blit(nm, nm.get_rect(centerx=rect.centerx, y=rect.y + 72))
                    # 锁定图标
                    try:
                        lock_font = pygame.font.SysFont("simhei", 36)
                        lock_icon = lock_font.render("🔒", True, (50, 50, 80))
                        sf.blit(lock_icon, lock_icon.get_rect(centerx=rect.centerx, y=rect.y + 105))
                    except:
                        lock_t = font_medium.render("[Locked]", True, (50, 50, 80))
                        sf.blit(lock_t, lock_t.get_rect(centerx=rect.centerx, y=rect.y + 105))
                    hint = font_tiny.render("击败前一章Boss解锁", True, (45, 45, 65))
                    sf.blit(hint, hint.get_rect(centerx=rect.centerx, y=rect.y + 155))
                except: pass
            else:
                # 已解锁状态
                bg = (20, 20, 40) if not hovered else (40, 40, 80)
                pygame.draw.rect(sf, bg, rect, border_radius=12)
                pygame.draw.rect(sf, theme['accent'], rect, 2 if not hovered else 3, border_radius=12)
                try:
                    chn = font_title.render(str(ch), True, theme['accent'])
                    sf.blit(chn, chn.get_rect(centerx=rect.centerx, y=rect.y + 8))
                    nm = font_small.render(f"第{ch}章", True, WHITE)
                    sf.blit(nm, nm.get_rect(centerx=rect.centerx, y=rect.y + 70))
                    bn = font_tiny.render(boss_names[ch], True, theme['accent'])
                    sf.blit(bn, bn.get_rect(centerx=rect.centerx, y=rect.y + 100))
                    dist = font_tiny.render(f"Boss: {boss_dists[ch]}", True, SILVER)
                    sf.blit(dist, dist.get_rect(centerx=rect.centerx, y=rect.y + 125))
                    # 已击败标记
                    if is_defeated:
                        try:
                            ok_font = pygame.font.SysFont("simhei", 20)
                            ok_icon = ok_font.render("✓ 已通关", True, GREEN)
                            sf.blit(ok_icon, ok_icon.get_rect(centerx=rect.centerx, y=rect.y + 150))
                        except:
                            ok_t = font_tiny.render("✓ CLEAR", True, GREEN)
                            sf.blit(ok_t, ok_t.get_rect(centerx=rect.centerx, y=rect.y + 150))
                    else:
                        ready_t = font_tiny.render("▶ 可选", True, theme['accent'])
                        sf.blit(ready_t, ready_t.get_rect(centerx=rect.centerx, y=rect.y + 150))
                except: pass
                self._menu_rects[f'ch{ch}'] = rect

        # 底部按钮行：重置进度 | 返回
        reset_rect = pygame.Rect(30, 620, 160, 45)
        hovered_reset = reset_rect.collidepoint(mp)
        bg_r = (50, 20, 20) if hovered_reset else (25, 10, 10)
        pygame.draw.rect(sf, bg_r, reset_rect, border_radius=8)
        pygame.draw.rect(sf, (120, 40, 40), reset_rect, 1, border_radius=8)
        try:
            rt = font_small.render("重置进度", True, (180, 60, 60) if hovered_reset else (120, 40, 40))
            sf.blit(rt, rt.get_rect(center=reset_rect.center))
        except: pass
        self._menu_rects['reset_progress'] = reset_rect

        back_rect = pygame.Rect(SCREEN_WIDTH // 2 - 80, 620, 160, 45)
        hovered_back = back_rect.collidepoint(mp)
        bg_b = (60, 20, 20) if hovered_back else (30, 10, 10)
        pygame.draw.rect(sf, bg_b, back_rect, border_radius=8)
        pygame.draw.rect(sf, RED, back_rect, 1, border_radius=8)
        try:
            bt = font_medium.render("← 返回", True, RED)
            sf.blit(bt, bt.get_rect(center=back_rect.center))
        except: pass
        self._menu_rects['back'] = back_rect

    # ======================== 挑战模式说明 ========================
    def draw_challenge_info(self, sf):
        """挑战模式开始界面"""
        self.star_field.update(); self.star_field.draw(sf)
        if not hasattr(Game, '_ci_ov'):
            Game._ci_ov = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            Game._ci_ov.fill((0, 0, 0, 160))
        sf.blit(Game._ci_ov, (0, 0))

        try:
            title = font_large.render("挑战模式", True, RED)
            sf.blit(title, title.get_rect(centerx=SCREEN_WIDTH // 2, y=80))
            sub = font_small.render("CHALLENGE MODE · Infinite Boss Rush", True, LIGHT_GRAY)
            sf.blit(sub, sub.get_rect(centerx=SCREEN_WIDTH // 2, y=125))
        except: pass

        rules = [
            ("每1800m出现一波Boss", CYAN),
            ("Boss随机选择5种章节类型", PURPLE),
            ("击败Boss进入下一波，间隔逐渐增加", ORANGE),
            ("无限距离，看你能坚持多久", YELLOW),
            ("随时可按 ESC 暂停，P 暂停", SILVER),
        ]
        try:
            for j, (text, col2) in enumerate(rules):
                t = font_medium.render(text, True, col2)
                sf.blit(t, t.get_rect(centerx=SCREEN_WIDTH // 2, y=200 + j * 55))
        except: pass

        mp = pygame.mouse.get_pos()
        # 开始按钮
        start_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 520, 200, 60)
        hovered = start_rect.collidepoint(mp)
        bg = (40, 10, 10) if hovered else (20, 5, 5)
        pygame.draw.rect(sf, bg, start_rect, border_radius=10)
        pygame.draw.rect(sf, RED, start_rect, 2, border_radius=10)
        try:
            st = font_large.render("开始挑战", True, RED if hovered else WHITE)
            sf.blit(st, st.get_rect(center=start_rect.center))
        except: pass
        self._menu_rects['ci_start'] = start_rect

        # 返回
        back_rect = pygame.Rect(SCREEN_WIDTH // 2 - 80, 600, 160, 50)
        hovered_b = back_rect.collidepoint(mp)
        bg2 = (60, 20, 20) if hovered_b else (30, 10, 10)
        pygame.draw.rect(sf, bg2, back_rect, border_radius=8)
        pygame.draw.rect(sf, GRAY, back_rect, 1, border_radius=8)
        try:
            bt = font_medium.render("← 返回", True, GRAY)
            sf.blit(bt, bt.get_rect(center=back_rect.center))
        except: pass
        self._menu_rects['ci_back'] = back_rect

    # ======================== 暂停界面 ========================
    def draw_paused(self, sf):
        if not hasattr(Game, '_pov'):
            Game._pov = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA); Game._pov.fill((0, 0, 0, 170))
        sf.blit(Game._pov, (0, 0))
        if not hasattr(Game, '_pbx'):
            Game._pbx = pygame.Surface((280, 200), pygame.SRCALPHA); Game._pbx.fill((10, 20, 40, 220))
        pb = Game._pbx; pbr = pb.get_rect(centerx=SCREEN_WIDTH // 2, centery=SCREEN_HEIGHT // 2)
        pygame.draw.rect(sf, CYAN, pbr, 2, border_radius=12); sf.blit(pb, pbr)
        try:
            pt = font_title.render("PAUSE", True, WHITE); sf.blit(pt, pt.get_rect(centerx=SCREEN_WIDTH // 2, y=pbr.top + 15))
            ht = font_medium.render("P or ESC 继续", True, YELLOW); sf.blit(ht, ht.get_rect(centerx=SCREEN_WIDTH // 2, y=pbr.top + 95))
            cs = font_small.render(f"Score: {int(self.score):,}", True, SILVER); sf.blit(cs, cs.get_rect(centerx=SCREEN_WIDTH // 2, y=pbr.top + 145))
            mode_disp = "故事模式" if self.game_mode == 'story' else "挑战模式"
            md = font_small.render(f"模式: {mode_disp}", True, CHAPTER_THEMES[self.chapter]['accent'])
            sf.blit(md, md.get_rect(centerx=SCREEN_WIDTH // 2, y=pbr.top + 175))
        except: pass

    # ======================== 输入名字界面 ========================
    def draw_enter_name(self, sf):
        self.star_field.update(); self.star_field.draw(sf)
        if not hasattr(Game, '_pov'):
            Game._pov = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA); Game._pov.fill((0, 0, 0, 170))
        sf.blit(Game._pov, (0, 0))
        if not hasattr(Game, '_ibx'):
            Game._ibx = pygame.Surface((420, 460), pygame.SRCALPHA); Game._ibx.fill((8, 16, 36, 235))
        ib = Game._ibx; ibr = ib.get_rect(centerx=SCREEN_WIDTH // 2, centery=SCREEN_HEIGHT // 2)
        pygame.draw.rect(sf, GOLD, ibr, 3, border_radius=12); sf.blit(ib, ibr)
        try:
            mode_tag = "[故事模式]" if self.game_mode == 'story' else "[挑战模式]"
            mt = font_small.render(mode_tag, True, CHAPTER_THEMES[self.chapter]['accent'])
            sf.blit(mt, mt.get_rect(centerx=SCREEN_WIDTH // 2, y=ibr.top + 8))
            go = font_title.render("GAME OVER" if not self.victory else "VICTORY!", True, RED if not self.victory else GOLD)
            sf.blit(go, go.get_rect(centerx=SCREEN_WIDTH // 2, y=ibr.top + 30))
            dist_str = self.distance_tracker.display_distance
            if self.game_mode == 'challenge':
                stats = [
                    (f"得分: {int(self.score):,}", YELLOW),
                    (f"飞行距离: {dist_str}", CYAN),
                    (f"击落敌机: {self.enemies_killed}", WHITE),
                    (f"击败Boss: {self.challenge_boss_count} 波", RED),
                    (f"最高Combo: {self.combo_max}", ORANGE),
                ]
            else:
                stats = [
                    (f"得分: {int(self.score):,}", YELLOW),
                    (f"飞行距离: {dist_str}", CYAN),
                    (f"到达章节: 第{self.chapter}章", CHAPTER_THEMES[self.chapter]['accent']),
                    (f"击落敌机: {self.enemies_killed}", WHITE),
                    (f"最高Combo: {self.combo_max}", ORANGE),
                ]
            for i2, (text, col2) in enumerate(stats):
                t = font_medium.render(text, True, col2); sf.blit(t, t.get_rect(centerx=SCREEN_WIDTH // 2, y=ibr.top + 100 + i2 * 38))
            if self.leaderboard.is_high_score(int(self.score)) and int(self.score) > 0:
                nr = font_medium.render("新纪录! 输入名字:", True, GOLD); sf.blit(nr, nr.get_rect(centerx=SCREEN_WIDTH // 2, y=ibr.top + 305))
            self.name_cursor_timer += 1
            if self.name_cursor_timer >= 30: self.name_cursor_visible = not self.name_cursor_visible; self.name_cursor_timer = 0
            cursor_str = "|" if self.name_cursor_visible else ""
            nd = self.input_name + cursor_str
            if not hasattr(Game, '_nmbg'):
                Game._nmbg = pygame.Surface((260, 44), pygame.SRCALPHA); Game._nmbg.fill((20, 30, 50))
            nbg = Game._nmbg; nbr = nbg.get_rect(centerx=SCREEN_WIDTH // 2, y=ibr.top + 345)
            pygame.draw.rect(sf, CYAN, nbr, 2, border_radius=6); sf.blit(nbg, nbr)
            nt = font_medium.render(nd, True, WHITE); sf.blit(nt, nt.get_rect(centerx=SCREEN_WIDTH // 2, centery=nbr.centery))
            opts = font_small.render("ENTER保存 | ESC跳过 | R重试", True, GRAY)
            sf.blit(opts, opts.get_rect(centerx=SCREEN_WIDTH // 2, y=ibr.top + 395))
        except: pass

    # ======================== 排行榜界面 ========================
    def draw_leaderboard(self, sf):
        self.star_field.update(); self.star_field.draw(sf)
        if not hasattr(Game, '_lb_ov'):
            Game._lb_ov = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA); Game._lb_ov.fill((0, 0, 0, 180))
        sf.blit(Game._lb_ov, (0, 0))
        if not hasattr(Game, '_lb_bx'):
            Game._lb_bx = pygame.Surface((480, 560), pygame.SRCALPHA); Game._lb_bx.fill((5, 12, 30, 230))
        lb_bx = Game._lb_bx; lb_br = lb_bx.get_rect(centerx=SCREEN_WIDTH // 2, centery=SCREEN_HEIGHT // 2)
        pygame.draw.rect(sf, GOLD, lb_br, 2, border_radius=12); sf.blit(lb_bx, lb_br)
        try:
            title = font_large.render("排行榜 TOP 10", True, GOLD)
            sf.blit(title, title.get_rect(centerx=SCREEN_WIDTH // 2, y=lb_br.top + 8))
            entries = self.leaderboard.get_top_n(10)
            header = font_small.render(f"{'排名':<4} {'名字':<10} {'得分':>8}  {'距离':>10}  {'模式':^8}", True, SILVER)
            sf.blit(header, header.get_rect(centerx=SCREEN_WIDTH // 2, y=lb_br.top + 55))
            pygame.draw.line(sf, GOLD, (lb_br.left + 20, lb_br.top + 80), (lb_br.right - 20, lb_br.top + 80), 1)
            for idx, e in enumerate(entries):
                d = e.get('distance', 0)
                ds = f"{d/1000:.1f}km" if d >= 1000 else f"{int(d)}m"
                mode_tag = e.get('mode', 'story')
                mt = '故事' if mode_tag == 'story' else '挑战'
                col2 = GOLD if idx == 0 else WHITE
                row = font_small.render(f"#{idx+1:<2}  {e['name']:<10} {e['score']:>8,}  {ds:>10}  {mt:^8}", True, col2)
                sf.blit(row, row.get_rect(centerx=SCREEN_WIDTH // 2, y=lb_br.top + 90 + idx * 42))
            hint = font_tiny.render("按 L 或 ESC 返回", True, GRAY); sf.blit(hint, hint.get_rect(centerx=SCREEN_WIDTH // 2, y=lb_br.bottom - 22))
        except: pass

    # ======================== 主绘制 ========================
    def draw(self):
        sx = sy = 0
        if self.screen_shake > 0:
            si = max(1, self.screen_shake // 4); sx = random.randint(-si, si); sy = random.randint(-si, si)
        if not hasattr(Game, '_dbuf'):
            Game._dbuf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        gs = Game._dbuf
        # 根据章节/模式调整星空背景色
        ch = self.chapter
        theme = CHAPTER_THEMES.get(ch, CHAPTER_THEMES[1])
        gs.fill((theme['bg_r'], theme['bg_g'], theme['bg_b']))

        if self.state == 'menu':
            self.draw_menu(gs)
        elif self.state == 'story_select':
            self.draw_story_select(gs)
        elif self.state == 'challenge_info':
            self.draw_challenge_info(gs)
        elif self.state == 'playing':
            self.star_field.draw(gs)
            for tp in self.trail_particles: tp.draw(gs)
            for pu in self.powerups: pu.draw(gs)
            for obs in self.obstacles: obs.draw(gs)
            for e in self.enemies: e.draw(gs)
            if self.boss and self.boss.alive: self.boss.draw(gs)
            self.player.draw(gs)
            for b in self.player_bullets: b.draw(gs)
            for b in self.enemy_bullets: b.draw(gs)
            for ex in self.explosions: ex.draw(gs)
            for p in self.particles_list: p.draw(gs)
            self.draw_hud(gs)
        elif self.state == 'paused':
            self.star_field.draw(gs)
            for pu in self.powerups: pu.draw(gs)
            for obs in self.obstacles: obs.draw(gs)
            self.player.draw(gs)
            for b in self.player_bullets: b.draw(gs)
            for e in self.enemies: e.draw(gs)
            if self.boss and self.boss.alive: self.boss.draw(gs)
            for b in self.enemy_bullets: b.draw(gs)
            for ex in self.explosions: ex.draw(gs)
            for p in self.particles_list: p.draw(gs)
            self.draw_hud(gs)
            self.draw_paused(gs)
        elif self.state == 'enter_name':
            self.draw_enter_name(gs)
        elif self.state == 'leaderboard':
            self.draw_leaderboard(gs)

        screen.fill(BLACK); screen.blit(gs, (sx, sy)); pygame.display.flip()

# ======================== 音效（预留）====================
try:
    explosion_snd = None  # pygame.mixer.Sound(...) 如需要音效
    hit_snd = None
except:
    explosion_snd = None; hit_snd = None

# ======================== 主循环 ========================
def main():
    game = Game()
    running = True; ec = 0; MAX_EC = 5

    while running:
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos

                    if game.state == 'menu':
                        # 故事模式
                        if game._menu_rects.get('1 ') and game._menu_rects['1 '].collidepoint(mx, my):
                            game.state = 'story_select'
                        # 挑战模式说明
                        elif game._menu_rects.get('2 ') and game._menu_rects['2 '].collidepoint(mx, my):
                            game.state = 'challenge_info'
                        # 排行榜
                        elif game._menu_rects.get('3 ') and game._menu_rects['3 '].collidepoint(mx, my):
                            game.state = 'leaderboard'

                    elif game.state == 'story_select':
                        # 重置进度
                        if game._menu_rects.get('reset_progress') and game._menu_rects['reset_progress'].collidepoint(mx, my):
                            game.chapter_progress.reset_all()
                        # 章节选择（仅解锁章节可选）
                        for ch in range(1, 6):
                            key = f'ch{ch}'
                            if (game._menu_rects.get(key) and
                                game._menu_rects[key].collidepoint(mx, my) and
                                game.chapter_progress.is_unlocked(ch)):
                                game._start_story(chapter=ch); break
                        # 返回
                        if game._menu_rects.get('back') and game._menu_rects['back'].collidepoint(mx, my):
                            game.state = 'menu'

                    elif game.state == 'challenge_info':
                        if game._menu_rects.get('ci_start') and game._menu_rects['ci_start'].collidepoint(mx, my):
                            game._start_challenge()
                        elif game._menu_rects.get('ci_back') and game._menu_rects['ci_back'].collidepoint(mx, my):
                            game.state = 'menu'

                    elif game.state == 'leaderboard':
                        game.state = 'menu'

                    elif game.state in ('enter_name',):
                        game.state = 'menu'

                elif event.type == pygame.KEYDOWN:
                    k = event.key

                    if k == pygame.K_ESCAPE:
                        if game.state == 'playing': game.state = 'paused'
                        elif game.state == 'paused': game.state = 'playing'
                        elif game.state in ('leaderboard', 'story_select', 'challenge_info', 'enter_name'):
                            game.state = 'menu'

                    elif k == pygame.K_RETURN:
                        if game.state == 'enter_name':
                            game.leaderboard.add_entry(game.input_name, game.score,
                                game.distance_tracker.distance, game.enemies_killed, game.chapter)
                            game.high_score = game.leaderboard.top_score; game.state = 'leaderboard'

                    elif k == pygame.K_p:
                        if game.state == 'playing': game.state = 'paused'
                        elif game.state == 'paused': game.state = 'playing'

                    elif k == pygame.K_r:
                        if game.state == 'enter_name': game._retry_same()

                    elif k == pygame.K_m:
                        if game.state == 'enter_name': game.state = 'menu'

                    elif k == pygame.K_l:
                        if game.state == 'menu': game.state = 'leaderboard'
                        elif game.state == 'leaderboard': game.state = 'menu'

                    elif k == pygame.K_b:
                        if game.state == 'playing' and game.bombs_available > 0:
                            game.bombs_available -= 1; game.use_bomb()

                    elif k == pygame.K_1:
                        if game.state == 'menu': game.state = 'story_select'

                    elif k == pygame.K_2:
                        if game.state == 'menu': game.state = 'challenge_info'

                    elif k == pygame.K_3:
                        if game.state == 'menu': game.state = 'leaderboard'

                    elif game.state == 'enter_name':
                        if k == pygame.K_BACKSPACE:
                            game.input_name = game.input_name[:-1] if game.input_name else ""
                        elif k == pygame.K_SPACE:
                            game.input_name += "_"
                        elif event.unicode and len(game.input_name) < 10:
                            if event.unicode.isprintable() and ord(event.unicode) < 128:
                                game.input_name += event.unicode.upper()

            game.update(); game.draw(); clock.tick(60); ec = 0
        except pygame.error as e:
            ec += 1; print(f"[Pygame Error #{ec}]: {e}")
            if ec >= MAX_EC: print("Safe exit."); break
            continue
        except Exception as e:
            ec += 1; print(f"[Warning #{ec}]: {type(e).__name__}: {e}")
            if ec >= MAX_EC: print("Safe exit."); break
            continue
    pygame.quit(); sys.exit()

if __name__ == "__main__":
    import io; sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    print("=" * 55)
    print("  *** 飞机大战 v3.1 双模式章节Boss版 ***")
    print("=" * 55)
    print("\n  故事模式：")
    print("  第1章 红色尖兵 Boss (800m)")
    print("  第2章 紫色利刃 Boss (1500m)")
    print("  第3章 棕色重甲 Boss (2500m)")
    print("  第4章 绿色精英 Boss (4000m)")
    print("  第5章 黄金终焉 Boss (6000m)")
    print("\n  挑战模式：无限距离，每1800m随机Boss循环")
    print("\n  操作: WASD移动 | SPACE射击 | B炸弹 | P暂停\n")
    print("  启动中...\n")
    main()
