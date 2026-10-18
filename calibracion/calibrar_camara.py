import cv2
import numpy as np
import glob
import os

CHECKERBOARD = (13, 9)

# Criterio para refinar las esquinas a nivel subpixel
criteria = (
    cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
    30,
    0.001
)

# Puntos 3D del tablero
objp = np.zeros(
    (CHECKERBOARD[0] * CHECKERBOARD[1], 3),
    np.float32
)

objp[:, :2] = np.mgrid[
    0:CHECKERBOARD[0],
    0:CHECKERBOARD[1]
].T.reshape(-1, 2)

objpoints = []
imgpoints = []

imagenes = []

for extension in ["*.jpg", "*.jpeg", "*.png", "*.JPG", "*.JPEG", "*.PNG"]:
    imagenes.extend(
        glob.glob(os.path.join("calibracion/fotos", extension))
    )

imagenes.sort()

validas = 0
gray = None

for ruta in imagenes:

    img = cv2.imread(ruta)

    if img is None:
        continue

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    encontrado, corners = cv2.findChessboardCorners(
        gray,
        CHECKERBOARD,
        cv2.CALIB_CB_ADAPTIVE_THRESH
        + cv2.CALIB_CB_NORMALIZE_IMAGE
        + cv2.CALIB_CB_FAST_CHECK
    )

    if encontrado:

        corners2 = cv2.cornerSubPix(
            gray,
            corners,
            (11, 11),
            (-1, -1),
            criteria
        )

        objpoints.append(objp)
        imgpoints.append(corners2)

        validas += 1

print("Imagenes validas:", validas)

if validas == 0:
    print("No se ha detectado el tablero en ninguna imagen.")
    exit()

# Calibracion
error, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(
    objpoints,
    imgpoints,
    gray.shape[::-1],
    None,
    None
)

print()
print("Error de calibracion:", error)

print()
print("Matriz de camara:")
print(camera_matrix)

print()
print("Coeficientes de distorsion:")
print(dist_coeffs)

# Guardar parametros
fs = cv2.FileStorage(
    "calibracion/CameraModel.yml",
    cv2.FILE_STORAGE_WRITE
)

fs.write("cameraMatrix", camera_matrix)
fs.write("distCoeffs", dist_coeffs)

fs.release()

print()
print("Parametros guardados en:")
print("calibracion/CameraModel.yml")
