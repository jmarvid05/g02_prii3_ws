import cv2
import glob
import os

CHECKERBOARD = (13, 9)

imagenes = []

for extension in ["*.jpg", "*.jpeg", "*.png", "*.JPG", "*.JPEG", "*.PNG"]:
    imagenes.extend(glob.glob(os.path.join("calibracion/fotos", extension)))

imagenes.sort()

validas = 0

print(f"Imagenes encontradas: {len(imagenes)}")
print()

for ruta in imagenes:
    img = cv2.imread(ruta)

    if img is None:
        print(f"[ERROR] {ruta}")
        continue

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    encontrado, esquinas = cv2.findChessboardCorners(
        gray,
        CHECKERBOARD,
        cv2.CALIB_CB_ADAPTIVE_THRESH
        + cv2.CALIB_CB_NORMALIZE_IMAGE
        + cv2.CALIB_CB_FAST_CHECK
    )

    nombre = os.path.basename(ruta)

    if encontrado:
        validas += 1
        print(f"[OK] {nombre}")
    else:
        print(f"[NO] {nombre}")

print()
print(f"Imagenes validas: {validas}/{len(imagenes)}")
