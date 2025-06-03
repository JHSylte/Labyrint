import cv2
import cvzone
from cvzone.ColorModule import ColorFinder

# Funksjon for å liste opp tilgjengelige kamera-porter
def availableCameras(maxPorts=5):
    availablePorts = []
    for i in range(maxPorts):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            availablePorts.append(i)
        cap.release()
    return availablePorts

print("Søker etter tilgjengelige kamera")
availablePorts = availableCameras()

if not availablePorts:
    print("Ingen tilgjengelige kamera detektert")
    exit()

print(f"Tilgjengelige kamera-porter: {availablePorts}")

CAMERA_PORT = -1
RESOLUTION = (640, 480)

while CAMERA_PORT not in availablePorts:
    CAMERA_PORT = int(input(f"Velg et tilgjengelig kamera fra denne lista ({availablePorts}):"))

# HSV-verdier for rød farge (juster disse etter kalibrering)
hsvVals = {'hmin': 117, 'smin': 136, 'vmin': 106, 'hmax': 179, 'smax': 187, 'vmax': 251}

myColorFinder = ColorFinder(False)  # Ikke kalibreringsmodus

camera = cv2.VideoCapture(CAMERA_PORT)
if not camera.isOpened():
    print(f"Feil: Kunne ikke åpne kamera på port {CAMERA_PORT}")
    exit()

camera.set(3, RESOLUTION[0])
camera.set(4, RESOLUTION[1])

# (Valgfritt) prøv å sette manuell eksponering
camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
camera.set(cv2.CAP_PROP_EXPOSURE, -6)  # Juster etter behov

centerPoint = (RESOLUTION[0]//2, RESOLUTION[1]//2, 1000)

def getBallPosition(cap, hsvVals, centerPoint):
    ret, img = cap.read()
    if not ret:
        return None, None, None

    # Blur fjerner støy for små objekter
    img = cv2.GaussianBlur(img, (7, 7), 0)

    imgColor, mask = myColorFinder.update(img, hsvVals)

    # Redusert minArea for å fange små konturer
    imgContour, contours = cvzone.findContours(img, mask, minArea=100)

    # Vis bilde og maske
    cv2.imshow("Ballsporing", imgContour)
    cv2.imshow("Mask", mask)

    if contours:
        x = contours[0]['center'][0] - centerPoint[0]
        y = (RESOLUTION[1] - contours[0]['center'][1]) - centerPoint[1]
        z = (contours[0]['area'] - centerPoint[2]) / 1000

        return x, y, z

    return None, None, None

# Hovedløkke
while True:
    x, y, z = getBallPosition(camera, hsvVals, centerPoint)

    if x is not None:
        print(f"Ballposisjon: X={x}, Y={y}, Z={z:.2f}")
    else:
        print("Ingen ball funnet")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
