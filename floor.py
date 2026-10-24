import pygame as pg

from lib.queue import Queue
from parkingSpace import ParkingSpace


class Floor:
    hasCounted = False
    parkingHeight = 0
    parkingWidth = 0
    parkingOutlineWidth = 0
    parkingOutlineColor = "black"

    realSpaces = []
    realSpacesDraw = []

    def __init__(self, size: int):
        self.spaces = Queue(5)

    def countSpaces(
        self,
        _initPos: pg.Vector2,
        parkingHeight,
        parkingWidth,
        parkingOutlineWidth,
        parkingOutlineColor,
    ):
        if self.hasCounted:
            return
        ret = pg.Vector2(0, 0)

        for i in range(self.spaces.size()):
            initPos = pg.Vector2(_initPos.x + i * parkingWidth, _initPos.y)

            # Points for each line to be drawn
            leftLinePoints = [
                initPos,
                pg.Vector2(
                    initPos.x, initPos.y + parkingHeight + parkingOutlineWidth / 2
                ),
            ]  # left line
            bottomLinePoints = [
                pg.Vector2(initPos.x, initPos.y + parkingHeight),
                pg.Vector2(initPos.x + parkingWidth, initPos.y + parkingHeight),
            ]  # bottom line
            rightLinePoints = [
                pg.Vector2(
                    initPos.x + parkingWidth,
                    initPos.y + parkingHeight + parkingOutlineWidth / 2,
                ),
                pg.Vector2(initPos.x + parkingWidth, initPos.y),
            ]  # right line

            self.realSpacesDraw.append(
                (leftLinePoints, bottomLinePoints, rightLinePoints)
            )
            self.realSpaces.append(
                ParkingSpace(
                    pg.Vector2(
                        initPos.x + parkingWidth / 2, initPos.y + parkingHeight / 2
                    ),
                    _initPos.x,
                    _initPos.y,
                    self.spaces,
                )
            )

            ret = pg.Vector2(initPos.x + parkingWidth, initPos.y + parkingHeight)

        self.parkingHeight = parkingHeight
        self.parkingWidth = parkingWidth
        self.parkingOutlineWidth = parkingOutlineWidth
        self.parkingOutlineColor = parkingOutlineColor

        self.hasCounted = True
        return ret

    def drawSpaces(self, screen):
        if not self.hasCounted:
            return

        for draw in self.realSpacesDraw:
            # Draws parking spot
            pg.draw.lines(
                screen,
                self.parkingOutlineColor,
                False,
                [*draw[0], *draw[1], *draw[2]],
                self.parkingOutlineWidth,
            )

    def getEmptySpace(self) -> tuple[int, ParkingSpace]:
        ret = (-1, None)

        for i, rs in enumerate(self.realSpaces):
            if not rs.occupied:
                ret = (i, rs)
                break

        return ret
