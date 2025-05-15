from balltrackC import initTracker, readPositions
from scaling import scaling

# Rød farge
RHSV = {'hmin': 117, 'smin': 136, 'vmin': 106,'hmax': 179, 'smax': 187, 'vmax': 251
}

# Grønn farge
GHSV = {'hmin': 54, 'smin': 81, 'vmin': 82, 'hmax': 70, 'smax': 175, 'vmax': 174}

tracker = initTracker(camera_port=1, hsvOne=RHSV, hsvTwo=GHSV, show_window=True)

while True:
    # Hent posisjoner
    pos = readPositions(tracker)
    if pos is None:
        break

    # Hent x/y for de to grønne ballene
    g1 = pos[1][1:3]  # farge2_1 → (x, y)
    g2 = pos[2][1:3]  # farge2_2 → (x, y)

    # Sjekk at begge er gyldige
    if None not in g1 and None not in g2:
        x_min = min(g1[0], g2[0])
        x_max = max(g1[0], g2[0])
        y_min = min(g1[1], g2[1])
        y_max = max(g1[1], g2[1])

        # Hent farge1 sin posisjon
        fx, fy, _ = pos[0][1:]

        # Skalér farge1 sin x/y til 0–100 basert på grønne baller
        x_scaled = scaling(fx, x_min, x_max, 0, 100)
        y_scaled = scaling(fy, y_min, y_max, 0, 100)

        print(f"Skalert X: {x_scaled:.1f}, Y: {y_scaled:.1f}")
    else:
        print("Grønne referanseballer ikke funnet")

