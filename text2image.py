# -*- coding: utf-8 -*-

import os
import pygame

pygame.init()

text = u"这是一段测试文本，test 123。"
font = pygame.font.Font(os.path.join("fonts", "simsun.ttc"), 14)
rtext = font.render(text, True, (0, 0, 0), (255, 255, 255))

pygame.image.save(rtext, "t.jpg")
