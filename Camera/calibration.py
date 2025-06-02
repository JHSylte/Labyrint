import cv2
import cvzone
from cvzone.ColorModule import ColorFinder

#Funksjon for å liste opp tilgjengelige kamera-porter
def availableCameras(maxPorts = 5):
    availablePorts = []
    for i in range(maxPorts):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            availablePorts.append(i)
        cap.release()
    return availablePorts

#Viser hvilken kamera som er tilgjengelige
print("Søker etter tilgjengelige kamera")
availablePorts = availableCameras()

if not availablePorts:
    print("Ingen tilgjengelige kamera detektert")
    exit()

print(f"Tilgjengelige kamera-porter: {availablePorts}")

#Velge kamera-port manuelt
CAMERA_PORT = -1
RESOLUTION = (640, 480)

while CAMERA_PORT not in availablePorts:
    CAMERA_PORT = int(input(f"Velg et tilgjengelig kamera fra denne lista ({availablePorts}):"))

# Kamera port (prøv 0, 1, eller 2)
#CAMERA_PORT = 1  

# Opprett ColorFinder i kalibreringsmodus
myColorFinder = ColorFinder(True)  # Sett til True for å kunne justere HSV

# Åpne kamera
camera = cv2.VideoCapture(CAMERA_PORT)
if not camera.isOpened():
    print(f"Feil: Kunne ikke åpne kamera på port {CAMERA_PORT}")
    exit()

camera.set(3, 640)  # Bredde
camera.set(4, 480)  # Høyde

# Hovedløkke
while True:
    ret, img = camera.read()
    if not ret:
        print("Feil: Kunne ikke lese ramme fra kamera.")
        break

    # Oppdater bildet basert på HSV-verdiene
    imgColor, mask = myColorFinder.update(img)

    # Vis bilde med konturer
    imgContour, _ = cvzone.findContours(img, mask)

    cv2.imshow("Kalibrering - Juster HSV verdier", imgContour)

    # Trykk 's' for å lagre HSV-verdiene
    if cv2.waitKey(1) & 0xFF == ord('s'):
        print("Lagre verdier:", myColorFinder.hsvVals)
        break

    # Trykk 'q' for å avslutte uten å lagre
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Frigjør ressurser
camera.release()
cv2.destroyAllWindows()