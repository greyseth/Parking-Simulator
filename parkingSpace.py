from collections import deque

import pygame as pg

import gamemanager as gm
from car import Car


class ParkingSpace:
    _parkingId = 1
    occupied = False
    time = 10

    timeCountdown = time

    def __init__(
        self,
        parkPosition: pg.Vector2,
        floorX: float,
        floorY: float,
        queue: deque,
        floorType: str,
    ):
        self._parkingId = ParkingSpace._parkingId
        ParkingSpace._parkingId += 1

        self.parkPosition = parkPosition
        self.floorY = floorY
        self.floorX = floorX
        self.queue = queue
        self.floorType = floorType

    def canLeave(self):
        if self.floorType == "stack":
            # only the top car may leave
            return len(self.queue) > 0 and self.queue[-1] == self.car
        return True

    def leave(self):
        if self.floorType == "queue":
            self.queue.popleft()
        else:
            self.queue.pop()

    def parkCar(self, car):
        self.car.isParked = True

    def assignCar(self, car: Car):
        self.carInitialPosition = car.position

        self.car = car
        self.occupied = True
        self.doneParking = False

        if self.floorType == "queue":
            car.setDestination(
                pg.Vector2(car.position[0], self.floorY),
                lambda carDestination1: carDestination1.setDestination(
                    pg.Vector2(self.parkPosition.x, self.floorY),
                    lambda carDestination2: carDestination2.setDestination(
                        self.parkPosition, self.parkCar, DoDebugRays=False
                    ),
                    DoDebugRays=False,
                ),
                DoDebugRays=False,
            )
        else:
            car.setDestination(
                pg.Vector2(car.position[0], self.floorY),
                lambda carDestination1: carDestination1.setDestination(
                    pg.Vector2(self.parkPosition.x, self.parkPosition.y), self.parkCar
                ),
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
                if not self.canLeave():
                    self.timeCountdown = 0
                    return

                self.timeCountdown = self.time

                self.occupied = False
                self.car.isParked = False
                self.leave()

                if not self.doneParking:
                    if self.floorType == "queue":
                        self.car.setDestination(
                            pg.Vector2(self.parkPosition.x, self.floorY),
                            lambda carDestination1: carDestination1.setDestination(
                                pg.Vector2(self.floorX - 50, self.floorY),
                                lambda carDestination2: carDestination2.setDestination(
                                    pg.Vector2(
                                        gm.floorStartPos.x - 50, gm.floorEndPos.y
                                    ),
                                    lambda carDestinationReached: (
                                        carDestinationReached.deleteCar()
                                    ),
                                    DoDebugRays=False,
                                ),
                                DoDebugRays=False,
                            ),
                            False,
                            False,
                        )
                    else:
                        self.car.setDestination(
                            pg.Vector2(self.carInitialPosition[0], self.parkPosition.y),
                            lambda carDestination1: carDestination1.setDestination(
                                pg.Vector2(
                                    self.carInitialPosition[0], self.parkPosition.y - 50
                                ),
                                lambda carDestination2: carDestination2.setDestination(
                                    pg.Vector2(
                                        self.floorX - 50, self.parkPosition.y - 50
                                    ),
                                    lambda carDestination3: (
                                        carDestination3.setDestination(
                                            pg.Vector2(
                                                self.floorX - 50, gm.floorEndPos.y
                                            ),
                                            lambda carDestinationReached: (
                                                carDestinationReached.deleteCar()
                                            ),
                                        )
                                    ),
                                ),
                            ),
                        )

                    self.doneParking = True
