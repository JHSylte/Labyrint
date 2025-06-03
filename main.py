import time
import numpy as np
import Astar
import threading
from JS_handler import initialize_joystick, read_joystick_axes
from modbus_server import store
from ball_tracker import get_ball_position

grid = np.loadtxt("/home/gruppe5/Desktop/labyrint_dilated.txt", dtype=int).tolist()

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

def grid_to_pixel(gx, gy):
    # Skaler tilbake til pikselrom
    x = gx / (94 - 1) * (pmax_x - pmin_x) + pmin_x
    y = gy / (94 - 1) * (pmax_y - pmin_y) + pmin_y
    return int(x), int(y)

def cameraPos():
    pos = get_ball_position(show=True)
    if pos is None:
        return (0, 0)  # fallback eller sist kjente posisjon
    x, y, _ = pos

    print(f"Position: x = {x}, y = {y}")

    store.setValues(3, 0, [to_two_compliment(int(x))])
    store.setValues(3, 1, [to_two_compliment(int(y))])

    gx, gy = scale_to_grid(x, y)

    return (gx, gy)


def reached_position(pos, target, deviation):
    dx = abs(pos[0] - target[0])
    dy = abs(pos[1] - target[1])
    return dx <= deviation and dy <= deviation


def to_two_compliment(value):
    if value < 0:
        return 65535 + value
    return value


def run_astar_mode(done_callback=None, stop_flag=None):
    position = cameraPos()
    destination = (3, 90)
    deviation = 1

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
        if stop_flag and stop_flag.is_set():
            print("A*-modus avbrutt (før steg)")
            if done_callback:
                done_callback()
            return

        print(f"Går mot: {target}")
        inside_start_time = None

        while True:
            if stop_flag and stop_flag.is_set():
                print("A*-modus avbrutt (i steg)")
                if done_callback:
                    done_callback()
                return

            pos = cameraPos()
            print("posisjon:", pos)

            Astar_x, Astar_y = target
            pix_x, pix_y = grid_to_pixel(Astar_x, Astar_y)

            store.setValues(3, 4, [pix_x])
            store.setValues(3, 5, [pix_y])

            if reached_position(pos, target, deviation):
                if inside_start_time is None:
                    inside_start_time = time.time()
                elif time.time() - inside_start_time >= 1.0:
                    break
            else:
                inside_start_time = None

            time.sleep(0.01)  # Unngå busy-wait

    print("A*-mål nådd!")
    if done_callback:
        done_callback()


def run_joystick_mode(stop_flag=None):
    joystick = initialize_joystick()
    if not joystick:
        return

    try:
        while True:
            if stop_flag and stop_flag.is_set():
                print("Joystick-modus avbrutt")
                return

            x, y = read_joystick_axes(joystick)
            print(f"Joystick: X={x:.2f}, Y={y:.2f}")
            int_x_axis = int(-(x * 100))
            int_y_axis = int(y * 100)

            store.setValues(3, 2, [to_two_compliment(int_x_axis)])
            store.setValues(3, 3, [to_two_compliment(int_y_axis)])

            cameraPos()

            time.sleep(0.001)
    except KeyboardInterrupt:
        print("\nAvslutter joystick-modus...")


def send_camera_position():
    while True:
        cameraPos()  # Henter og sender posisjon til PLS
        time.sleep(0.001)


def main():
    previous_mode = None
    stop_flag = threading.Event()
    current_thread = None  # Holder referanse til aktiv modus-tråd

    # Start kamera-posisjonstråd (daemon slik at programmet kan avslutte)
    threading.Thread(target=send_camera_position, daemon=True).start()

    while True:
        try:
            mode_val = store.getValues(3, 6, 1)[0]

            if mode_val != previous_mode:
                print(f"→ Endrer modus til {mode_val}")
                stop_flag.set()  # Be eksisterende modus om å stoppe

                # Vent på at tidligere tråd avsluttes
                if current_thread is not None:
                    current_thread.join()
                    current_thread = None

                stop_flag.clear()  # Nullstill flagget etter at gammel tråd er ferdig

                if mode_val == 1:
                    print("→ Starter A*-modus")
                    current_thread = threading.Thread(target=run_astar_mode, args=(None, stop_flag))
                    current_thread.start()
                elif mode_val == 2:
                    print("→ Starter joystick-modus")
                    current_thread = threading.Thread(target=run_joystick_mode, args=(stop_flag,), daemon=True)
                    current_thread.start()
                elif mode_val == 0:
                    print("→ Idle (ingen aktiv styring)")

                previous_mode = mode_val

            time.sleep(0.001)
        except KeyboardInterrupt:
            print("Avslutter program...")
            stop_flag.set()
            if current_thread is not None:
                current_thread.join()
            break

if __name__ == "__main__":
    main()
