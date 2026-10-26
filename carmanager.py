import pygame as pg

import car
import gamemanager as gm
from floor import Floor

floorWidth = 5
floors = [
    Floor(floorWidth),
    Floor(floorWidth),
    Floor(floorWidth),
    Floor(floorWidth, "stack"),
]
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
        initPos = pg.Vector2(
            windowPadding,
            windowPadding + floorI * (floorGap + parkingHeight),
        )

        if floorI == 0:
            gm.floorStartPos = initPos

        global parkingEndCoordinates
        temp = floor.countSpaces(
            initPos, parkingHeight, parkingWidth, parkingOutlineWidth, "black"
        )
        parkingEndCoordinates = parkingEndCoordinates if temp is None else temp
        gm.floorEndPos = parkingEndCoordinates
        floor.drawSpaces(screen)

    return


def spawnCar(floor):
    # UNUSED: determine which closest floor isn't full
    # floorTargetIndex = next(
    #     (i for i, f in enumerate(floors) if not f.spaces.isFull()), -1
    # )
    #

    # Chooses floor straight from parameter
    floorTargetIndex = floors.index(floor)

    newCar = car.Car(
        (
            parkingEndCoordinates.x + carSpawnMargin,
            parkingEndCoordinates.y + carSpawnMargin,
        ),
        cars,
        floorTargetIndex < 0,
    )

    if floorTargetIndex != -1:
        floors[floorTargetIndex].spaces.enqueue(newCar)
        _, space = floors[floorTargetIndex].getEmptySpace()
        space.assignCar(newCar)

    cars.append(newCar)


def updateCars(screen: pg.Surface):
    for _, c in enumerate(cars):
        c.update(screen)

    for f in floors:
        # checks for click in floor
        floorRect = pg.Rect(
            f.floorStart.x,
            f.floorStart.y,
            f.floorEnd.x - f.floorStart.x,
            f.floorEnd.y - f.floorStart.y,
        )
        if floorRect.collidepoint(pg.mouse.get_pos()) and gm.mouse[0]:
            spawnCar(f)

        for space in f.realSpaces:
            space.updateSpace()
