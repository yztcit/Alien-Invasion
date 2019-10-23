# _*_ coding: UTF-8 _*_
import pygame
from pygame.sprite import Group

import game_functions as gf
from button import Button
from game_stats import GameStats
from scoreboard import Scoreboard
from settings import Setting
from ship import Ship


def run_game():
    # 游戏配置信息
    ai_settings = Setting()

    # 创建一个用于统计信息的实例，并创建记分牌
    stats = GameStats(ai_settings)

    # 初始化游戏，并创建一个屏幕对象
    pygame.init()
    screen = pygame.display.set_mode(
        [ai_settings.screen_width, ai_settings.screen_height]
    )
    pygame.display.set_caption("Alien Invasion")

    # 记分牌
    score_board = Scoreboard(ai_settings, stats, screen)

    # Play 按钮
    play_button = Button(ai_settings, screen, 'Play')

    # 创建一艘飞船
    ship = Ship(ai_settings, screen)
    # 创建外星人
    aliens = Group()
    gf.creat_fleet(ai_settings, screen, ship, aliens)

    # 创建一个用于存储子弹的编组
    bullets = Group()

    # 开始游戏的主循环
    while True:

        # 监视键盘和鼠标事件
        gf.check_events(
            ai_settings, stats, screen, score_board,
            play_button, aliens, ship, bullets
        )

        # 游只在戏处于活动状态时做相应的操作
        if stats.game_active and not stats.game_pause:
            ship.update()
            gf.update_bullets(
                ai_settings, stats, screen, score_board, aliens, ship, bullets
            )
            gf.update_aliens(
                ai_settings, stats, screen, aliens, score_board, ship, bullets
            )

        # 每次循环时都重新绘制屏幕
        # 让最新绘制的屏幕可见
        gf.update_screen(
            ai_settings, stats, screen, score_board,
            aliens, ship, bullets, play_button
        )


run_game()
