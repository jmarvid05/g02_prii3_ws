import cv2
import numpy as np
import glob
import os

CHECKERBOARD = (13, 9)

criteria = (
    cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
    30,
    0.001
)

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
rutas_validas = []

imagenes = []

for extension in ["*.jpg", "*.jpeg", "*.png", "*.JPG", "*.JPEG", "*.PNG"]:
    imagenes.extend(
        glob.glob(os.path.join("calibracion/fotos", extension))
    )

imagenes.sort()

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
        rutas_validas.append(ruta)

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
    objpoints,
    imgpoints,
    gray.shape[::-1],
    None,
    None
)

errores = []

for i in range(len(objpoints)):

    proyectados, _ = cv2.projectPoints(
        objpoints[i],
        rvecs[i],
        tvecs[i],
        mtx,
        dist
    )

    diferencia = imgpoints[i] - proyectados

    error = np.sqrt(
        np.mean(
            np.sum(diferencia ** 2, axis=2)
        )
    )

    errores.append(
        (error, os.path.basename(rutas_validas[i]))
    )

errores.sort(reverse=True)

print("Error global de calibracion:", ret)
print()
print("Errores por imagen (de peor a mejor):")
print()

for error, nombre in errores:
    print(f"{error:.3f} px  {nombre}")

print()
print("Matriz de camara:")
print(mtx)

print()
print("Coeficientes de distorsion:")
print(dist)
