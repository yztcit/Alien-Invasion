# _*_ coding: UTF-8 _*_
class Setting():
	def __init__(self):
		#屏幕尺寸
		self.screen_width = 1200
		self.screen_height = 800
		
		# 背景色
		self.bg_color = (230, 230, 230)
		
		# 飞船移动单元 像素
		self.ship_limit = 3

		# 子弹属性
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = (60, 60, 60)
		# 限制子弹的数量
		self.bullet_allowed = 10
		
		# 外星人属性
		self.fleet_drop_speed = 10
		
		# 飞船发生碰撞后游戏间歇时间
		self.time_sleep = 0.5
		
		# 加快游戏节奏
		self.speedup_scale = 1.1
		# 得分随节奏加快提高
		self.score_scale = 1.5
		
		# 最高分存档
		self.high_score_file = "data/high_score.json"
		
		self.initialize_dynamic_settings()
		
	def initialize_dynamic_settings(self):
		"""初始化随游戏进行而变化的配置"""
		self.ship_speed_factor = 1.5
		self.bullet_speed_factor = 2
		self.alien_speed_factor = 1
		
		# fleet_direction 为1表示右移，-1表示左移
		self.fleet_direction = 1
		
		# 记分，随着进度加快得分提高
		self.alien_points = 50
	
	def increase_speed(self):
		"""提高速度设置和外星人点数"""
		self.ship_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale
		
		self.alien_points = int(self.alien_points * self.score_scale )
