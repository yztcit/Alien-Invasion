# _*_ coding: UTF-8 _*_
import sys
from time import sleep
import pygame

from bullet import Bullet
from alien import Alien

def fire_bullet(ai_settings, screen, ship, bullets):
	# 创建一个子弹并将其加入子弹编组
	if len(bullets) < ai_settings.bullet_allowed:
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)

def start_game(ai_settings, stats, screen, score_board, aliens, ship, bullets):
	if not stats.game_active:
		# 重置游戏设置
		ai_settings.initialize_dynamic_settings()
		
		# 隐藏光标
		pygame.mouse.set_visible(False)
		
		# 重置游戏统计信息
		stats.reset_stats()
		stats.game_active = True
		
		# 重置记分牌
		score_board.prep_images()
		
		# 清空子弹、外星人列表
		aliens.empty()
		bullets.empty()
		
		# 创建一群新的外星人，飞船居中
		creat_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()

def check_keydown_events(event, ai_settings, stats, screen, score_board, aliens, ship, bullets):
	"""响应按键"""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_UP:
		ship.moving_up = True
	elif event.key == pygame.K_DOWN:
		ship.moving_down = True
	
	# fire
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings, screen, ship, bullets)
	# play
	elif event.key == pygame.K_p:
		start_game(ai_settings, stats, screen, score_board, aliens, ship, bullets)
	# pause
	elif event.key == pygame.K_t:
		if stats.game_active:
			stats.game_pause = not stats.game_pause
	
def check_keyup_events(stats, event, ship):
	"""按键松开"""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False
	elif event.key == pygame.K_UP:
		ship.moving_up = False
	elif event.key == pygame.K_DOWN:
		ship.moving_down = False
		
	elif event.key == pygame.K_q:
		game_over(stats)
	
def check_play_button(ai_settings, stats, screen, score_board, play_button, aliens, ship,
		bullets, mouse_x, mouse_y):
	"""单击play按钮开始新游戏"""
	
	if play_button.rect.collidepoint(mouse_x, mouse_y):
		start_game(ai_settings, stats, screen, score_board, aliens, ship, bullets)

def game_over(stats):
	stats.storage_high_score()
	sys.exit()

def check_events(ai_settings, stats, screen, score_board, play_button, aliens, ship, bullets):
	"""响应鼠标和键盘事件"""
	
	for event in pygame.event.get():
		# 鼠标点击 X 退出 或按 q 键退出
		if event.type == pygame.QUIT:
			game_over(stats)
			
		elif event.type == pygame.MOUSEBUTTONDOWN:
			(mouse_x, mouse_y) = pygame.mouse.get_pos()
			check_play_button(
				ai_settings, stats, screen, score_board, play_button, 
				aliens, ship, bullets, mouse_x, mouse_y
			)
		
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(
				event, ai_settings, stats, screen, score_board,
				aliens, ship, bullets
			)
				
		elif event.type == pygame.KEYUP:
			check_keyup_events(stats, event, ship)
			
def get_num_alien_x(ai_settings, alien_width):
	# 创建一个外星人，并计算一行可以容纳多少个
	# 间距为其宽度
	available_space_x = ai_settings.screen_width - (2 * alien_width)
	num_aliens_x = int(available_space_x / (2 * alien_width))
	return num_aliens_x
	
def get_num_rows(ai_settings, alien_height, ship_height):
	"""计算屏幕可以容纳多少行外星人"""
	available_space_y = ai_settings.screen_height - 3 * alien_height - ship_height
	
	num_rows = int(available_space_y / (2 * alien_height))
	return num_rows

def creat_alien(ai_settings, screen, aliens, alien_num, row_num):
	# 创建一个外星人并添加到当前行
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_num
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_num
	
	aliens.add(alien)
	
def creat_fleet(ai_settings, screen, ship, aliens):
	# 创建外星人群
	# 创建一个外星人，并计算一行可以容纳多少个
	# 间距为其宽度
	alien = Alien(ai_settings, screen)			

	num_aliens_x = get_num_alien_x(ai_settings, alien.rect.width)
	num_rows = get_num_rows(ai_settings, alien.rect.height, ship.rect.height)
	
	# 创建一行外星人
	for row_num in range(num_rows):
		for alien_num in range(num_aliens_x):
			creat_alien(ai_settings, screen, aliens, alien_num, row_num)
	

def check_fleet_edges(ai_settings, aliens):
	"""有外星人到达屏幕边缘采取相应的措施"""
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens)
			break

def change_fleet_direction(ai_settings, aliens):
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1	

def ship_hit(ai_settings, stats, screen, score_board, aliens, ship, bullets):
	"""
	响应外星人撞击飞船（三次机会）
	游戏结束后，重置相应参数
	"""
	if stats.ships_left > 1:
		# 将ship_left -1
		stats.ships_left -= 1
		score_board.prep_ships()
		
		# 清空外星人和子弹列表
		aliens.empty()
		bullets.empty()
		# 创建一群外星人，飞船位置初始化
		creat_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()
		# 延时0.5s
		sleep(ai_settings.time_sleep)
	else:
		# 重置参数
		stats.game_active = False
		pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, stats, screen, score_board, aliens, ship, bullets):
	"""检查是否有外星人到达屏幕底端"""	
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			ship_hit(ai_settings, stats, screen, score_board, aliens, ship, bullets)
		break

def update_aliens(ai_settings, stats, screen, aliens, score_board, ship, bullets):
	"""检查是否有外星人到达屏幕边缘，并整体更新外星人群的位置"""
	check_fleet_edges(ai_settings, aliens)
	aliens.update()
	
	"""检测飞船和外星人碰撞"""
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, stats, screen, score_board, aliens, ship, bullets)
		
	"""检查是否有外星人到达屏幕底端"""
	check_aliens_bottom(ai_settings, stats, screen, score_board, aliens, ship, bullets)
	
def check_high_score(stats, score_board):
	"""检查是否诞生新的最高分"""
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		score_board.prep_high_score()

def start_new_level(ai_settings, stats, screen, score_board, aliens, ship, bullets):
	if len(aliens) == 0:
		# 删除现有子弹，加快游戏节奏，并创建一群新的外星人
		bullets.empty()
		ai_settings.increase_speed()
		
		# 提高等级
		stats.level += 1
		score_board.prep_level()
		
		creat_fleet(ai_settings, screen, ship, aliens)

def check_bullet_alien_collisions(ai_settings, stats, screen, score_board, aliens, ship, bullets):
	"""
	检查是否有子弹击中外星人
	如果有做出相应的处理
	"""
	collections = pygame.sprite.groupcollide(bullets, aliens, False, True)
	
	"""击中外星人得分"""
	if collections:
		for aliens in collections.values():
			stats.score += ai_settings.alien_points * len(aliens)
			score_board.prep_score()
		check_high_score(stats, score_board)
		
	"""消灭所有外星人之后，再生成一组  无穷无尽"""
	start_new_level(ai_settings, stats, screen, score_board, aliens, ship, bullets)

def update_bullets(ai_settings, stats, screen, score_board, aliens, ship, bullets):
	"""更新子弹位置，并删除已消失的子弹"""
	bullets.update()
	
	for bullet in bullets:
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
			
	"""
	检查是否有子弹击中外星人
	如果有做出相应的处理
	"""
	check_bullet_alien_collisions(ai_settings, stats, screen, score_board, aliens, ship, bullets)

def update_screen(ai_settings, stats, screen, score_board, aliens, ship, bullets, play_button):
	"""更新屏幕上的图像，并切换到新屏幕上"""
	# 每次循环时都重新绘制屏幕
	screen.fill(ai_settings.bg_color)
	
	# 在飞船和外星人后面重新绘制所有子弹
	for bullet in bullets:
		bullet.draw_bullet()
	
	# 在指定的位置绘制飞船
	ship.blitme()
	# 绘制外星人群
	aliens.draw(screen)
	# 绘制记分牌
	score_board.show_score()
	
	# 当游戏处于非活动状态时，显示play按钮
	if not stats.game_active:
		play_button.draw_button()
	
	# 让最新绘制的屏幕可见
	pygame.display.flip()
