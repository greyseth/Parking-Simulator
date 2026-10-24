import pygame as pg

import gamemanager as gm
from car import Car
from lib.queue import Queue


class ParkingSpace:
    occupied = False
    time = 10

    def __init__(
        self, parkPosition: pg.Vector2, floorX: float, floorY: float, queue: Queue
    ):
        self.parkPosition = parkPosition
        self.floorY = floorY
        self.floorX = floorX
        self.queue = queue

    def parkCar(self, car):
        self.car.isParked = True

    def assignCar(self, car: Car):
        self.car = car
        self.occupied = True
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

    doneParking = False

    def updateSpace(self):
        if self.occupied:
            if self.car.isParked:
                self.time -= gm.dt
            if self.time <= 0:
                self.time = 0

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
