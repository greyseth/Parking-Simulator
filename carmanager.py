import pygame as pg

import car
import lib.queue as queue

floors = [queue.Queue(3), queue.Queue(3), queue.Queue(3)]
cars = []

# display settings
windowPadding = 75
parkingWidth = 50
parkingHeight = parkingWidth * 1.5
floorGap = 75
parkingOutlineWidth = 4
parkingOutlineColor = "black"

# car spawning
parkingEndCoordinates = pg.Vector2(0, 0)
carSpawnMargin = 75


# drawing the parking lot
def drawParkingSpaces(screen):
    for floorI, floor in enumerate(floors):
        for spaceI, space in enumerate(floor.contents):
            initPos = pg.Vector2(
                windowPadding + spaceI * parkingWidth,
                windowPadding + floorI * (floorGap + parkingHeight),
            )

            # Points for each line to be drawn
            leftLinePoints = [
                initPos,
                pg.Vector2(
                    initPos.x, initPos.y + parkingHeight + parkingOutlineWidth / 2
                ),
            ]
            bottomLinePoints = [
                pg.Vector2(initPos.x, initPos.y + parkingHeight),
                pg.Vector2(initPos.x + parkingWidth, initPos.y + parkingHeight),
            ]
            rightLinePoints = [
                pg.Vector2(
                    initPos.x + parkingWidth,
                    initPos.y + parkingHeight + parkingOutlineWidth / 2,
                ),
                pg.Vector2(initPos.x + parkingWidth, initPos.y),
            ]

            # for car spawning coords
            global parkingEndCoordinates
            parkingEndCoordinates = pg.Vector2(
                initPos.x + parkingWidth, initPos.y + parkingHeight
            )

            # Draws parking spot
            pg.draw.lines(
                screen,
                parkingOutlineColor,
                False,
                [*leftLinePoints, *bottomLinePoints, *rightLinePoints],
                parkingOutlineWidth,
            )

    return


def parkCar(floorIndex, spaceIndex, car):
    floors[floorIndex].changeContent(spaceIndex, car)
    car.isParked = True


def findEmptySpot(index, newCar):
    spaceTargetIndex = next(
        (i for i, space in enumerate(floors[index].contents) if space is None),
        -1,
    )
    spaceTargetPos = pg.Vector2(
        windowPadding + spaceTargetIndex * parkingWidth + parkingWidth / 2,
        newCar.getPosition().y,
    )

    newCar.setDestination(
        spaceTargetPos,
        lambda c: c.setDestination(
            pg.Vector2(spaceTargetPos.x, spaceTargetPos.y + parkingHeight / 2),
            parkCar(index, spaceTargetIndex, c),
        ),
    )


def spawnCar():
    if len([c for c in cars if not c.isParked]) > 0:
        return

    newCar = car.Car(
        (
            parkingEndCoordinates.x + carSpawnMargin,
            parkingEndCoordinates.y + carSpawnMargin,
        )
    )

    # determine which closest floor isn't full
    floorTargetIndex = next(
        (i for i, floor in enumerate(floors) if not floor.isFull()), -1
    )

    if floorTargetIndex != -1:
        floorTargetPos = pg.Vector2(
            newCar.getPosition().x,
            windowPadding + floorTargetIndex * (floorGap + parkingHeight),
        )

        newCar.setDestination(
            floorTargetPos, lambda c: findEmptySpot(floorTargetIndex, c)
        )

    cars.append(newCar)


def updateCars(screen: pg.Surface):
    for _, c in enumerate(cars):
        c.update(screen)
