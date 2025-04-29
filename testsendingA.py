import time
import Astar  # Din fungerende A*-algoritme

# Simulert global posisjon (som om kameraet sporer)
current_pos = [5, 5]

def cameraPos():
    return tuple(current_pos)

def reached_position(pos, target, deviation):
    return abs(pos[0] - target[0]) <= deviation and abs(pos[1] - target[1]) <= deviation

def move_towards_target(current, target, step=1):
    for i in range(2):
        diff = target[i] - current[i]
        if abs(diff) > step:
            current[i] += step if diff > 0 else -step
        else:
            current[i] = target[i]
    return current

# Rutenett (1 = åpen, 0 = blokkert)
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

# Start og slutt
position = cameraPos()
destination = (0, 0)
deviation = 0
solver = True

if solver:
    # Kjør A*
    path = Astar.a_star(grid, position, destination)
    if not path:
        print("❌ Ingen rute funnet.")
    else:
        simplified_path = Astar.simplify_path(path)
        print("📍 Rute funnet:", simplified_path)

        for i, target in enumerate(simplified_path):
            print(f"\n➡️ Går mot punkt {i}: {target}")

            while not reached_position(cameraPos(), target, deviation):
                move_towards_target(current_pos, target)
                print(f"   📷 Kamera sier: {cameraPos()}")

                # Her kan du sende posisjon til PLS:
                # f.eks. modbus.write(x=cameraPos()[0], y=cameraPos()[1])

                time.sleep(0.2)  # Simuler tidsintervall

            print(f"✅ Nådd punkt {i}: {target}")