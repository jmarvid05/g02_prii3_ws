import cv2
import numpy as np
import glob
import os

CHECKERBOARD = (13, 9)
UMBRAL_ERROR = 3.0

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

# Primera calibracion
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
    objpoints,
    imgpoints,
    gray.shape[::-1],
    None,
    None
)

objpoints_filtrados = []
imgpoints_filtrados = []

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

    if error <= UMBRAL_ERROR:
        objpoints_filtrados.append(objpoints[i])
        imgpoints_filtrados.append(imgpoints[i])

print("Imagenes iniciales:", len(objpoints))
print("Imagenes tras filtrado:", len(objpoints_filtrados))

# Segunda calibracion
ret2, mtx2, dist2, rvecs2, tvecs2 = cv2.calibrateCamera(
    objpoints_filtrados,
    imgpoints_filtrados,
    gray.shape[::-1],
    None,
    None
)

print()
print("Error de calibracion filtrada:", ret2)

print()
print("Matriz de camara:")
print(mtx2)

print()
print("Coeficientes de distorsion:")
print(dist2)

fs = cv2.FileStorage(
    "calibracion/CameraModel_filtrado.yml",
    cv2.FILE_STORAGE_WRITE
)

fs.write("cameraMatrix", mtx2)
fs.write("distCoeffs", dist2)

fs.release()

print()
print("Guardado en calibracion/CameraModel_filtrado.yml")
