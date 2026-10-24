import pygame as pg

import carmanager
import gamemanager as gm

pg.init()
screen = pg.display.set_mode((1280, 720))
pg.display.set_caption("Studi Kasus Stack & Queue Statis: Simulasi Parkir Kendaraan")
clock = pg.time.Clock()

gm.screen = screen

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

    gm.renderPointerBox()

    pg.display.flip()
    gm.updateDeltaTime(clock)

pg.quit()
