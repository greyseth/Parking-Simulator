dt = 0


def updateDeltaTime(clock):
    global dt
    dt = clock.tick(60) / 1000
