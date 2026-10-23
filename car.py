import math
import sys

import pygame as pg

import gamemanager as gm


class Car:
    position = (0, 0)
    angle = 0
    scaleDivider = 3.5
    collisionSize = pg.Vector2(50, 100)

    isParked = False
    moveSpeed = 500

    def __init__(self, position):
        try:
            self.position = position

            rawImg = pg.image.load("./assets/cat.png").convert_alpha()
            self.carImg = pg.transform.scale(
                rawImg,
                (
                    rawImg.get_width() / self.scaleDivider,
                    rawImg.get_height() / self.scaleDivider,
                ),
            )
            self.carRect = self.carImg.get_rect(center=position)
        except pg.error as e:
            print(f"Error when loading image: {e}")
            sys.exit()

    def update(self, screen: pg.Surface):
        # handles movement
        if hasattr(self, "destination"):
            destDistance = pg.Vector2(self.position).distance_to(self.destination)
            if destDistance > 2:
                movementDirection = self.destination - pg.Vector2(self.position)
                remainingDistance = movementDirection.length()
                movementDirection = movementDirection.normalize()
                step = self.moveSpeed * gm.dt

                if remainingDistance <= step:
                    self.position = (self.destination.x, self.destination.y)
                else:
                    self.position = (
                        self.position[0] + movementDirection.x * step,
                        self.position[1] + movementDirection.y * step,
                    )
            else:
                del self.destination

                if self.onDestinationReached is not None:
                    self.onDestinationReached(self)

        # renders car
        self.drawCar(screen)

    def drawCar(self, screen: pg.Surface, boundingBox: bool = False):
        if self.carImg is None or self.carRect is None:
            return

        self.carRect.center = self.position

        car = pg.transform.rotate(self.carImg, self.angle)
        newRect = car.get_rect(center=self.carRect.center)

        screen.blit(car, newRect)

        # draws bounding box
        if boundingBox:
            pg.draw.rect(
                screen,
                "green",
                (
                    self.position[0] - self.collisionSize.x / 2,
                    self.position[1] - self.collisionSize.y / 2,
                    self.collisionSize.x,
                    self.collisionSize.y,
                ),
                4,
            )

    def getPosition(self):
        return pg.Vector2(self.position[0], self.position[1])

    def getAngle(self):
        return self.angle

    def setDestination(
        self, dest: pg.Vector2, onDestinationReached=None, invertedAngle: bool = False
    ):
        self.destination = dest
        self.onDestinationReached = onDestinationReached

        dir = dest - self.getPosition()
        if invertedAngle:
            dir = -dir
        self.angle = math.degrees(math.atan2(dir.y, -dir.x)) + 90
