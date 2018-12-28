# _*_ coding: UTF-8 _*_
import json

class GameStats():
	"""跟踪游戏的统计信息"""
	def __init__(self, ai_settings):
		"""初始化统计信息"""
		self.ai_settings = ai_settings
		self.reset_stats()
		self.game_active = False
		self.game_pause = False
		# 最高得分，任何情况都不重置
		self.read_high_score()
			
	def read_high_score(self):
		try:
			with open(self.ai_settings.high_score_file, 'r') as f_obj:
				self.high_score = json.load(f_obj)
		except:
			self.high_score = 0
		
	def storage_high_score(self):
		with open(self.ai_settings.high_score_file, 'w') as f_obj:
			json.dump(self.high_score, f_obj)
	
	def reset_stats(self):
		# 剩余游戏次数
		self.ships_left = self.ai_settings.ship_limit
		# 得分
		self.score = 0
		# 等级
		self.level = 1
