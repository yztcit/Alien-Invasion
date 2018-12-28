# _*_ coding: UTF-8 _*_
import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard():
	"""显示得分的类"""
	
	def __init__(self, ai_settings, stats, screen):
		self.screen = screen
		self.screen_rect = self.screen.get_rect()
		self.ai_settings = ai_settings
		self.stats = stats
		
		# 显示得分信息的字体设置
		self.text_color = (30, 30, 30)
		self.font = pygame.font.SysFont(None, 38)
		
		# 初始化当前得分、最高得分图像，等级
		self.prep_images()
	
	def prep_images(self):
		# 初始化当前得分、最高得分图像，等级
		self.prep_score()
		self.prep_high_score()
		self.prep_level()
		self.prep_ships()
	
	def prep_score(self):
		"""将得分转化为渲染的图像"""
		# 将得分值圆整，到最近的10的整数倍（第二个参数控制小数位）
		rounded_score = int(round(self.stats.score, -1))
		# 字符串格式指令，在数值中间插入逗号
		score_str = "Score: " + "{:,}".format(rounded_score)
		self.score_image = self.font.render(
			score_str, True, self.text_color, self.ai_settings.bg_color
		)
		# 将得分放到屏幕的右上角
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 20
		self.score_rect.top = 10
		
	def prep_high_score(self):
		"""将得分转化为渲染的图像"""
		# 将得分值圆整，到最近的10的整数倍（第二个参数控制小数位）
		high_score = int(round(self.stats.high_score, -1))
		high_score_str = "High Score: " + "{:,}".format(high_score)
		self.high_score_image = self.font.render(
			high_score_str, True, 
			self.text_color, self.ai_settings.bg_color
		)
		# 将最高得分放到屏幕正上方，居中
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.centerx = self.screen_rect.centerx
		self.high_score_rect.top = 10
		
	def prep_level(self):
		level_str = "Level: " + str(self.stats.level)
		self.level_image = self.font.render(
			level_str, True, 
			self.text_color, self.ai_settings.bg_color
		)
		# 等级位于得分下方
		self.level_image_rect = self.level_image.get_rect()
		self.level_image_rect.right = self.screen_rect.right - 20
		self.level_image_rect.top = self.score_rect.bottom + 10
	
	def prep_ships(self):
		self.ships = Group()
		for ship_num in range(self.stats.ships_left):
			ship = Ship(self.ai_settings, self.screen)
			ship.rect.x = 10 + ship_num * ship.rect.width
			ship.rect.y = 10
			self.ships.add(ship)
	
	def show_score(self):
		"""在屏幕上显示当前得分、最高分和等级"""
		self.screen.blit(self.score_image, self.score_rect)
		self.screen.blit(self.high_score_image, self.high_score_rect)
		self.screen.blit(self.level_image, self.level_image_rect)

		# 绘制飞船
		self.ships.draw(self.screen)
