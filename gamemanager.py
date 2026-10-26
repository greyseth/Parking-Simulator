import pygame as pg

dt = 0
floorStartPos = pg.Vector2(0, 0)
floorEndPos = pg.Vector2(0, 0)
screen: pg.Surface

renderBox = None
renderBoxPosition = (0, 0)

mouse = [False, False, False]


def updateDeltaTime(clock):
    global dt
    dt = clock.tick(60) / 1000


pointerBoxPadding = 10


def drawPointerBox(contents, mousePos: tuple[int, int]):
    global renderBox, renderBoxPosition

    # Calculates text content
    contentText = pg.font.SysFont("Arial", 12).render(contents, False, (255, 255, 255))
    contentSize = pg.Vector2(contentText.get_width(), contentText.get_height())

    # calculates and draws rectangle and text
    pointerBoxSurface = pg.Surface(
        pg.Vector2(
            contentSize.x + pointerBoxPadding * 2, contentSize.y + pointerBoxPadding * 2
        )
    ).convert()
    pg.draw.rect(
        pointerBoxSurface,
        "darkcyan",
        (0, 0, pointerBoxSurface.get_width(), pointerBoxSurface.get_height()),
    )
    pointerBoxSurface.blit(contentText, (pointerBoxPadding, pointerBoxPadding))

    renderBox = pointerBoxSurface
    renderBoxPosition = mousePos


def renderPointerBox():
    global renderBox

    if renderBox is None:
        return
    screen.blit(renderBox, renderBoxPosition)

    renderBox = None
