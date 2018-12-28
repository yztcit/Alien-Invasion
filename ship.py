# _*_ coding: UTF-8 _*_
import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
	
	def __init__(self, ai_settings, screen):
		'''初始化飞船并初始化其位置'''
		super().__init__()
		self.screen = screen
		self.ai_settings = ai_settings
		
		# 加载飞船图像并获取其外接矩形
		self.image = pygame.image.load('images/ship.bmp')
		self.rect = self.image.get_rect()
		self.screen_rect = self.screen.get_rect()
		
		# 将每艘新飞船放到屏幕底部中央位置
		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom
		
		# 在飞船的属性center中存储小数值
		self.centerx = float(self.rect.centerx)
		self.bottom = float(self.rect.bottom)
		
		# 移动标志
		self.moving_left = False
		self.moving_up = False
		self.moving_right = False
		self.moving_down = False
		
		
	def center_ship(self):
		self.center = self.screen_rect.centerx
		self.bottom = self.screen_rect.bottom
		
	def update(self):
		# 左移
		if self.moving_left and self.rect.left > 0:
			self.centerx -= self.ai_settings.ship_speed_factor
			
		# 右移
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.centerx += self.ai_settings.ship_speed_factor
		
		# 上移
		if self.moving_up and self.rect.top > 0:
			self.bottom -= self.ai_settings.ship_speed_factor
		
		# 下移
		if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
			self.bottom += self.ai_settings.ship_speed_factor
		
		
		self.rect.centerx = self.centerx
		self.rect.bottom = self.bottom
			
	def blitme(self):
		'''在指定的位置绘制飞船'''
		self.screen.blit(self.image, self.rect)
