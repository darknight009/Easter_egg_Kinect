import os
import pygame, sys, datetime
import random
from pygame.locals import *
from pykinect import nui
import time
from pykinect.nui import JointId

g=2
class basket:
	inst=2
	def __init__(self, img= 'basket.png'):
		basket.inst+=1
		self.img=img
		self.speed_x=random.randint(-5,5)
		self.x=random.randint(0,400)
		self.instance=(basket.inst)%3
		self.y= self.instance*300 +40
		self.basket_img=self.load()
	def load(self):	
		bskt=pygame.image.load(self.img).convert_alpha()
		bskt=pygame.transform.scale(bskt, [105,50])
		return bskt
	def pose(self):
		if self.x>=400:
			self.speed_x*=-1
		if self.x<=0:
			self.speed_x=abs(self.speed_x)
		self.x+=self.speed_x
		return (self.x, self.y)

class Egg:
	def __init__(self, basket, img='egg.png'):
		self.img=img
		self.spped_x=0
		self.speed_y=0
		self.x=0
		self.y=0
		self.angle=0
		self.basket=basket
		self.egg_im=self.load()
		self.airborne=False
	def load(self):	
		egg_im=pygame.image.load(self.img).convert_alpha()
		egg_im=pygame.transform.scale(egg_im, [40,60])
		egg_im=pygame.transform.rotate(egg_im, self.angle)
		return egg_im
	def set_pose(self, basket):
		if basket:
			self.speed_x=basket.speed_x
			self.speed_y=0
			self.x=basket.x+30-self.speed_x
			self.y=basket.y-15
		else:
			self.speed_x=0
			self.speed_y-=g
			self.angle+=18
			self.angle%=360
		self.x+=self.speed_x
		self.y-=self.speed_y
	def get_pose(self):
		return (self.x, self.y)
	def shoot(self):
		self.airborne=True
		self.speed_y=40
		self.set_pose(False)

class Life_bar:
	def __init__(self, img='egg.png', lives=3, score=0):
		self.img=img
		self.lives=lives
		self.score=score
		self.egg_im=self.load_lives()
		self.font=pygame.font.SysFont("comicsansms", 18)
		self.medium_font=pygame.font.SysFont("comicsansms", 28)
		self.big_font=pygame.font.SysFont("comicsansms",93)
	def load_lives(self):	
		egg_im=pygame.image.load(self.img).convert_alpha()
		egg_im=pygame.transform.scale(egg_im, [20,30])
		return egg_im
	def show_score(self):
		return self.font.render("Score: "+str(self.score), True, (255, 255, 255))
	def game_over(self):
		return self.big_font.render("Game Over", True, (255, 255, 255))
	def play_again(self):
		return self.medium_font.render("Press Enter to play again \n or Escape to quit", True, (255, 255, 255))
	def time(self, time_passed):
		time_passed="Time: "+str(time_passed.hour-5)+":"+str(time_passed.minute-30)+":"+str(time_passed.second)
		return self.font.render(time_passed, True, (255, 255, 255))

def display(DISP, bg, baskets, life_bar, egg, time_passed):
	DISP.blit(bg, [0,0])
	DISP.blit(life_bar.time(time_passed), (200, 750))
	DISP.blit(baskets[0].basket_img, baskets[0].pose())
	DISP.blit(baskets[1].basket_img, baskets[1].pose())
	DISP.blit(baskets[2].basket_img, baskets[2].pose())
	for l in range(life_bar.lives):
		DISP.blit(life_bar.egg_im, (30*l, 750))
	DISP.blit(life_bar.show_score(), (380, 750))
	if life_bar.lives!=-1:
		DISP.blit(egg.egg_im, egg.get_pose())
	else:
		DISP.blit(life_bar.game_over(), (00, 300))
		DISP.blit(life_bar.play_again(), (00, 400))

def main():
	pygame.init()
	clock = pygame.time.Clock()
	size=width, height = 480, 790
	DISP=pygame.display.set_mode(size)
	baskets=[basket(), basket(), basket()]
	egg=Egg(2)
	life_bar=Life_bar()
	pygame.display.set_caption('Easter Egg')
	bg=pygame.image.load('background.jpg').convert()
	bg=pygame.transform.scale(bg, size)
	arg=baskets[2]
	egg.set_pose(arg)
	transl=False
	variation=1
	start_ticks=pygame.time.get_ticks()
	#Kinect_initializers
	kinect= nui.Runtime()
	kinect.skeleton_engine.enabled = True
	prev_diff=0
    #kinect_initializers end
	while 1:	#GameLoop
		ms=(pygame.time.get_ticks() - start_ticks)
		time_passed=datetime.datetime.fromtimestamp(ms/1000.0)
		variation=(life_bar.score+20)/20
		if baskets[1].speed_x == baskets[2].speed_x and baskets[1].speed_x==0:
			baskets[1].speed_x=random.randint(-5*variation,5*variation)
		if baskets[1].speed_x == baskets[0].speed_x and baskets[1].speed_x==0:
			baskets[1].speed_x=random.randint(-5*variation,5*variation)
		if transl:
			temp=baskets[0].speed_x
			for t in range(60):
				for b in baskets:
					b.speed_x=0
					b.y+=10
					b.y%=900
				egg.y+=10
				display(DISP, bg, baskets, life_bar, egg, time_passed)
				pygame.display.update()
				clock.tick(60)
			baskets[0], baskets[1], baskets[2] = baskets[1], baskets[2], baskets[0]
			egg.basket=2
			arg=baskets[egg.basket]
			baskets[0].speed_x=random.randint(-5*variation,5*variation)
			baskets[1].speed_x=random.randint(-5*variation,5*variation)
			baskets[2].speed_x=temp
			transl=False
		else:
			if egg.y>=720:
				life_bar.lives-=1
				egg.airborne=False
				if life_bar.lives==-1:
					print("Game Over")
				arg=baskets[egg.basket]
			if baskets[egg.basket-1].x -10 <= egg.x <= baskets[egg.basket-1].x +90:
				if baskets[egg.basket-1].y -25 <= egg.y <= baskets[egg.basket-1].y +25:
					if egg.speed_y<=0:
						life_bar.score+=1
						egg.basket-=1
						if egg.basket==0:
							transl=True
						arg=baskets[egg.basket]
						egg.airborne=False
		egg.set_pose(arg)
		display(DISP, bg, baskets, life_bar, egg, time_passed)
		#kinect_code
		frame = kinect.skeleton_engine.get_next_frame()
		for index, data in enumerate(frame.SkeletonData):
			elb_r = data.SkeletonPositions[JointId.ElbowRight]
			wrist_r = data.SkeletonPositions[JointId.WristRight]
			wrist_l = data.SkeletonPositions[JointId.WristLeft]
			diff_clap = abs(wrist_r.x-wrist_l.x <= 0.05) and abs(wrist_r.y-wrist_l.y <= 0.05) and abs(wrist_r.z-wrist_l.z <= 0.05)
			diff_right_Hand=wrist_r.y - elb_r.y
			if elb_r.w == 0.0 or wrist_r.w == 0.0:
				continue
			if diff_right_Hand-prev_diff > 0.07 and egg.speed_y==0 and life_bar.lives!=-1 and egg.airborne==False:
				arg=False
				egg.shoot()
			elif diff_clap:
				return False
			prev_diff=diff_right_Hand	
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and egg.speed_y==0 and life_bar.lives!=-1 and egg.airborne==False:
					arg=False
					egg.shoot()
				if event.key == K_RETURN:
					return False
				if event.key == K_ESCAPE:
					pygame.quit()
					sys.exit()
				if event.key == K_u:
					kinect.camera.elevation_angle += 2
				if event.key == K_j:
					kinect.camera.elevation_angle -= 2
				if event.key == K_x:
					kinect.camera.elevation_angle = 2
			if event.type==QUIT:
				pygame.quit()
				sys.exit()
		pygame.display.update()
		clock.tick(100)

if __name__ == '__main__':
	while True:
		main()