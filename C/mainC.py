from balltrackC import initTracker, readPositions
from scaling import scaling

# Rød farge
RHSV = {'hmin': 117, 'smin': 136, 'vmin': 106,'hmax': 179, 'smax': 187, 'vmax': 251}

# Grønn farge
GHSV = {'hmin': 53, 'smin': 70, 'vmin': 54, 'hmax': 83, 'smax': 165, 'vmax': 224}

tracker = initTracker(camera_port=0, hsvOne=RHSV, hsvTwo=GHSV, show_window=True)

# Forrige posisjoner for de grønne kulene
prev_g1 = None
prev_g2 = None

while True:
    pos = readPositions(tracker)
    if pos is None:
        break

    # Hent posisjoner for grønne baller
    g1 = pos[1][1:3]  # farge2_1 → (x, y)
    g2 = pos[2][1:3]  # farge2_2 → (x, y)

    # Sjekk om nye posisjoner er gyldige, ellers bruk forrige
    if None not in g1:
        prev_g1 = g1
    if None not in g2:
        prev_g2 = g2

    if prev_g1 is not None and prev_g2 is not None:
        x_min = min(prev_g1[0], prev_g2[0])
        x_max = max(prev_g1[0], prev_g2[0])
        y_min = min(prev_g1[1], prev_g2[1])
        y_max = max(prev_g1[1], prev_g2[1])

        fx, fy, _ = pos[0][1:]

        # Sjekk at røde ballens posisjon også er gyldig
        if fx is not None and fy is not None:
            x_scaled = scaling(fx, x_min, x_max, 0, 100)
            y_scaled = scaling(fy, y_min, y_max, 0, 100)
            print(f"Skalert X: {x_scaled:.1f}, Y: {y_scaled:.1f}")
        else:
            print("Rød ball ikke funnet")
    else:
        print("Grønne referanseballer ikke funnet (og ingen tidligere posisjon lagret)")