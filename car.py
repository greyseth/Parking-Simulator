import math
import sys

import pygame as pg

import gamemanager as gm


class Car:
    _carId = 1

    position = (0, 0)
    angle = 0
    scaleDivider = 3.5
    collisionSize = pg.Vector2(50, 100)

    isParked = False
    moveSpeed = 500

    spawnPosition = pg.Vector2(0, 0)
    retreatWait = 0.5

    debugRays = []

    def __init__(self, position, parentContainer, noPlace=False):
        self._carId = Car._carId
        Car._carId += 1

        try:
            self.position = position
            self.spawnPosition = pg.Vector2(position)
            self.parentContainer = parentContainer
            self.noPlace = noPlace

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

    def deleteCar(self):
        self.parentContainer.remove(self)

    def update(self, screen: pg.Surface):
        # handles movement
        if not self.noPlace:
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
        else:
            if self.retreatWait > 0:
                self.retreatWait -= gm.dt
            else:
                self.retreatWait = 0
                self.setDestination(
                    pg.Vector2(self.spawnPosition.x, self.spawnPosition.y + 100),
                    lambda c: self.deleteCar(),
                )

                self.noPlace = False

        # renders car
        self.drawCar(screen)

    def drawCar(self, screen: pg.Surface, boundingBox: bool = False):
        if self.carImg is None or self.carRect is None:
            return

        self.carRect.center = (
            int(self.position[0]),
            int(self.position[1]),
        )  # reconverted because the IDE keeps insisting they're incompatible types

        car = pg.transform.rotate(self.carImg, self.angle)
        newRect = car.get_rect(center=self.carRect.center)

        screen.blit(car, newRect)

        screen.blit(
            pg.font.SysFont("Arial", 20).render(
                "#" + str(self._carId), True, (0, 0, 0)
            ),
            pg.Vector2(self.position[0] - 5, self.position[1] - 5),
        )

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

        # draws debug rays
        for ray in self.debugRays:
            pg.draw.line(screen, "green", ray[0], ray[1], 2)

    def getPosition(self):
        return pg.Vector2(self.position[0], self.position[1])

    def getAngle(self):
        return self.angle

    def setDestination(
        self,
        dest: pg.Vector2,
        onDestinationReached=None,
        invertedAngle: bool = False,
        DoDebugRays=False,
    ):
        self.destination = dest
        self.onDestinationReached = onDestinationReached

        dir = dest - self.getPosition()
        if invertedAngle:
            dir = -dir
        self.angle = math.degrees(math.atan2(dir.y, -dir.x)) + 90

        if DoDebugRays:
            self.debugRays.append([self.getPosition(), dest])
