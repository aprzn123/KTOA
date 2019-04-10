from datetime import timedelta
from datetime import date as dtd

import pygame


pygame.init()
window = pygame.display.set_mode((800, 450))


class Task(object):
    def __init__(self, name, date, importance, estimated_time):
        self.name = name
        self.date = date
        self.importance = importance
        self.estimated_time = estimated_time
        self.pomodoros = []

screen = "Start"

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    pygame.draw.circle(window, (255, 127, 0), (400, 225), 15, 2)

    pygame.display.flip()
