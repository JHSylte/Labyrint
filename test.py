import time

import Astar

def cameraPos():
    return (5, 5)

def reached_position(pos, target, deviation):
    return

grid = [
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
    [0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 0, 1, 0],
    [1, 0, 1, 1, 1, 1, 0, 1, 0, 0],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 0, 0, 0, 1, 0, 0, 1]
]

position = cameraPos()
destination = (0, 0)

deviation = 0.2
solver = True

if solver:
    path = Astar.a_star(grid, position, destination)

    if not path:
        print("Ingen rute funnet.")

    path_to_pls = Astar.simplify_path(path)

    for target in path_to_pls:
        #add modbus update for x and y

        while True:

            if not reached_position(cameraPos(), target, deviation):
                time.sleep(0.1)