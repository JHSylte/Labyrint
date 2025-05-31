import cv2
import cvzone
from cvzone.ColorModule import ColorFinder

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

myColorFinder = ColorFinder(True)  # Kalibreringsmodus = True

camera = cv2.VideoCapture(CAMERA_PORT)
if not camera.isOpened():
    print(f"Feil: Kunne ikke åpne kamera på port {CAMERA_PORT}")
    exit()

camera.set(3, RESOLUTION[0])
camera.set(4, RESOLUTION[1])

# (Valgfritt) prøv å sette manuell eksponering
camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
camera.set(cv2.CAP_PROP_EXPOSURE, -6)  # Juster ned mot -8, -10 ved behov

while True:
    ret, img = camera.read()
    if not ret:
        print("Feil: Kunne ikke lese ramme fra kamera.")
        break

    # Blur for å jevne ut støy
    img = cv2.GaussianBlur(img, (7, 7), 0)

    # HSV-basert fargefiltrering
    imgColor, mask = myColorFinder.update(img)

    # Finn konturer med lavere minArea
    imgContour, _ = cvzone.findContours(img, mask, minArea=100)

    # Vis resultater
    cv2.imshow("Kalibrering - Juster HSV verdier", imgContour)
    cv2.imshow("Mask (hvitt = valgt farge)", mask)

camera.release()
cv2.destroyAllWindows()
