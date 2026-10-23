import pygame as pg

import car
import carmanager
import gamemanager as gm
import lib.queue as queue
import lib.stack as stack

pg.init()
screen = pg.display.set_mode((1280, 720))
clock = pg.time.Clock()

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                carmanager.spawnCar()

    screen.fill("white")

    carmanager.drawParkingSpaces(screen)
    carmanager.updateCars(screen)

    pg.display.flip()
    gm.updateDeltaTime(clock)

pg.quit()
