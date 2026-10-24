import pygame as pg

dt = 0
floorStartPos = pg.Vector2(0, 0)
floorEndPos = pg.Vector2(0, 0)


def updateDeltaTime(clock):
    global dt
    dt = clock.tick(60) / 1000
