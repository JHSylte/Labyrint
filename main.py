import time
import numpy as np
import Astar
from JS_handler import initialize_joystick, read_joystick_axes
from modbus_server import store
from ball_tracker import get_ball_position

grid = np.loadtxt("labyrint_dilated.txt", dtype=int).tolist()

pmin_x = -195
pmax_x = 171
pmin_y = -168
pmax_y = 204

def scale_to_grid(x, y):
    # Normaliser og skaler til grid
    grid_x = (x - pmin_x) / (pmax_x - pmin_x) * (94 - 1)
    grid_y = (y - pmin_y) / (pmax_y - pmin_y) * (94 - 1)

    # Klipp verdiene slik at de alltid er innenfor gyldig indeks
    grid_x = max(0, min(94 - 1, int(round(grid_x))))
    grid_y = max(0, min(94 - 1, int(round(grid_y))))

    return grid_x, grid_y

def cameraPos():
    pos = get_ball_position(show=True)
    if pos is None:
        return (0, 0)  # fallback eller sist kjente posisjon
    x, y, _ = pos

    store.setValues(3, 0, [int(x)])
    store.setValues(3, 1, [int(y)])

    gx, gy = scale_to_grid(x, y)

    return (gx, gy)

def reached_position(pos, target, deviation):
    dx = abs(pos[0] - target[0])
    dy = abs(pos[1] - target[1])
    return dx <= deviation and dy <= deviation

def run_astar_mode(done_callback=None):
    position = cameraPos()
    destination = (3, 90)
    deviation = 0

    print("Starter fra:", position)
    print("Startverdi:", grid[position[1]][position[0]])
    print("Sluttverdi:", grid[destination[1]][destination[0]])

    path = Astar.a_star(grid, position, destination)
    if not path:
        print("Ingen rute funnet.")
        if done_callback:
            done_callback()
        return

    simplified_path = Astar.simplify_path(path)

    for target in simplified_path:
        print(f"Går mot: {target}")
        while not reached_position(cameraPos(), target, deviation):
            print("posisjon:", cameraPos())
            Astar_x = target[0]
            Astar_y = target[1]

            store.setValues(3, 4, [Astar_x])
            store.setValues(3, 5, [Astar_y])

            time.sleep(0.1)

    print("A*-mål nådd!")
    if done_callback:
        done_callback()


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

            cameraPos()

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

busy = False

#while True:
#    try:
#        mode_val = store.getValues(3, 6, 1)[0]
#
#        if not busy and mode_val != previous_mode:
#            stop_flag.set()  # avbryt nåværende modus (gjelder joystick)
#            time.sleep(0.2)
#            stop_flag.clear()
#
#            if mode_val == 1:
#                print("→ Starter A*-modus (låser kontroll til ferdig)")
#                busy = True
#                threading.Thread(target=run_astar_mode, args=(lambda: busy := False,)).start()
#            elif mode_val == 2:
#                print("→ Starter joystick-modus")
#                threading.Thread(target=run_joystick_mode).start()
#            elif mode_val == 0:
#                print("→ Idle")
#            previous_mode = mode_val
#
#        time.sleep(0.5)
#    except KeyboardInterrupt:
#        print("Avslutter program...")
#        break

if __name__ == "__main__":
    main()
