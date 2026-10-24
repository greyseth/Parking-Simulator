import pygame as pg

import gamemanager as gm
from car import Car
from lib.queue import Queue


class ParkingSpace:
    _parkingId = 1
    occupied = False
    time = 10

    timeCountdown = time

    def __init__(
        self, parkPosition: pg.Vector2, floorX: float, floorY: float, queue: Queue
    ):
        self._parkingId = ParkingSpace._parkingId
        ParkingSpace._parkingId += 1

        self.parkPosition = parkPosition
        self.floorY = floorY
        self.floorX = floorX
        self.queue = queue

    def parkCar(self, car):
        self.car.isParked = True

    def assignCar(self, car: Car):
        self.car = car
        self.occupied = True
        self.doneParking = False
        car.setDestination(
            pg.Vector2(car.position[0], self.floorY),
            lambda carDestination1: carDestination1.setDestination(
                pg.Vector2(self.parkPosition.x, self.floorY),
                lambda carDestination2: carDestination2.setDestination(
                    self.parkPosition, self.parkCar, DoDebugRays=True
                ),
                DoDebugRays=True,
            ),
            DoDebugRays=True,
        )

    def drawSpaceDetails(self):
        pg.draw.circle(
            gm.screen, "red" if self.occupied else "green", self.parkPosition, 5
        )

        gm.screen.blit(
            pg.font.SysFont("Arial", 10).render(
                str(int(self.timeCountdown)), True, (0, 0, 0)
            ),
            pg.Vector2(self.parkPosition.x, self.parkPosition.y - 20),
        )

    doneParking = False

    def updateSpace(self):
        self.drawSpaceDetails()

        if self.occupied:
            if self.car.isParked:
                self.timeCountdown -= gm.dt

            if self.timeCountdown <= 0:
                self.timeCountdown = self.time

                self.occupied = False
                self.car.isParked = False
                self.queue.dequeue()

                if not self.doneParking:
                    self.car.setDestination(
                        pg.Vector2(self.parkPosition.x, self.floorY),
                        lambda carDestination1: carDestination1.setDestination(
                            pg.Vector2(self.floorX - 50, self.floorY),
                            lambda carDestination2: carDestination2.setDestination(
                                pg.Vector2(gm.floorStartPos.x - 50, gm.floorEndPos.y),
                                lambda carDestinationReached: (
                                    carDestinationReached.deleteCar()
                                ),
                                DoDebugRays=True,
                            ),
                            DoDebugRays=True,
                        ),
                        True,
                        True,
                    )

                    self.doneParking = True
