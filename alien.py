# _*_ coding: UTF-8 _*_
import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
	"""表示单个外星人"""
	
	def __init__(self, ai_settings, screen):
		"""初始化外星人，并设置其起始位置"""
		super().__init__()
		self.ai_settings = ai_settings
		self.screen = screen 
		
		# 加载外星人图像，并设置rect属性
		self.image = pygame.image.load("images/alien.bmp")
		self.rect = self.image.get_rect()
		# 每个外星人最初都出现在屏幕左上方
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height
		# 保存其精确的位置
		self.x = float(self.rect.x)

	def check_edges(self):
		"""如果碰到屏幕边缘返回True"""
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right:
			return True
		elif self.rect.left <= 0:
			return True


	def update(self):
		"""向左或者向右移动"""
		self.x += self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction
		self.rect.x = self.x

	def blitme(self):
		"""在指定的位置绘制外星人"""
		self.screen.blit(self.image, self.rect)
