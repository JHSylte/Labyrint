import time
import Astar
from JS_handler import initialize_joystick, read_joystick_axes
from modbus_server import store

def cameraPos():

    return (5, 5)

def reached_position(pos, target, deviation):
    dx = abs(pos[0] - target[0])
    dy = abs(pos[1] - target[1])
    return dx <= deviation and dy <= deviation

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

def run_astar_mode():
    position = cameraPos()
    destination = (0, 0)
    deviation = 0.2

    path = Astar.a_star(grid, position, destination)
    if not path:
        print("Ingen rute funnet.")
        return

    simplified_path = Astar.simplify_path(path)

    for target in simplified_path:
        print(f"Går mot: {target}")
        while not reached_position(cameraPos(), target, deviation):
            Astar_x= target[0]
            Astar_y= target[1]

            store.setValues(3, 4, [Astar_x])
            store.setValues(3, 5, [Astar_y])

            time.sleep(0.1)
        print(f"Nådd: {target}")

def run_joystick_mode():
    joystick = initialize_joystick()
    if not joystick:
        return

    try:
        while True:
            x, y = read_joystick_axes(joystick)
            print(f"Joystick: X={x:.2f}, Y={y:.2f}")
            store.setValues(3, 2, [int(x * 1000)])
            store.setValues(3, 3, [int(y * 1000)])
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nAvslutter joystick-modus...")

def main():
    mode = input("Velg modus (astar/js): ").strip().lower()

    if mode == "astar":
        run_astar_mode()
    elif mode == "js":
        run_joystick_mode()
    else:
        print("Ugyldig modus. Bruk 'astar' eller 'js'.")

if __name__ == "__main__":
    main()
