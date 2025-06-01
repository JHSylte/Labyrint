import time
import Astar
from JS_handler import initialize_joystick, read_joystick_axes
from modbus_server import store
from ball_tracker import get_ball_position

def cameraPos():
    pos = get_ball_position(show=True)
    if pos is None:
        return (0, 0)  # fallback eller sist kjente posisjon
    x, y, _ = pos

    print(f"Position: x = {x}, y = {y}")

    store.setValues(3, 0, [to_two_compliment(int(x))])
    store.setValues(3, 1, [to_two_compliment(int(y))])

    return (x, y)

def reached_position(pos, target, deviation):
    dx = abs(pos[0] - target[0])
    dy = abs(pos[1] - target[1])
    return dx <= deviation and dy <= deviation

def to_two_compliment(value):
    if value < 0:
       return 65535 + value
    return value

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
    deviation = 0

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
            time.sleep(0.1)

            store.setValues(3, 4, [Astar_x])
            store.setValues(3, 5, [Astar_y])

            #time.sleep(0.1)
        print(f"Nådd: {target}")

def run_joystick_mode():
    joystick = initialize_joystick()
    if not joystick:
        return

    try:
        while True:
            x, y = read_joystick_axes(joystick)
            print(f"Joystick: X={x:.2f}, Y={y:.2f}")
            int_x_axis = int(-(x * 100))
            int_y_axis = int(y * 100)

            store.setValues(3, 2, [to_two_compliment(int_x_axis)])
            store.setValues(3, 3, [to_two_compliment(int_y_axis)])
        
            cameraPos()

            #time.sleep(0.1)
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
