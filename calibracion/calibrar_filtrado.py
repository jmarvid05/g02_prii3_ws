import cv2
import numpy as np
import glob
import os

# Numero de esquinas interiores del tablero
CHECKERBOARD = (13, 9)

# Error maximo permitido para aceptar una imagen
UMBRAL_ERROR = 3.0

# Criterio para mejorar la precision de las esquinas
criteria = (
    cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
    30,
    0.001
)

# Crear los puntos 3D teoricos del tablero
objp = np.zeros(
    (CHECKERBOARD[0] * CHECKERBOARD[1], 3),
    np.float32
)

# Colocar los puntos en forma de rejilla
objp[:, :2] = np.mgrid[
    0:CHECKERBOARD[0],
    0:CHECKERBOARD[1]
].T.reshape(-1, 2)

# Puntos reales del tablero
objpoints = []

# Puntos detectados en las imagenes
imgpoints = []

# Guardar las rutas de las imagenes validas
rutas_validas = []

# Lista de imagenes
imagenes = []

# Buscar todas las imagenes de la carpeta
for extension in ["*.jpg", "*.jpeg", "*.png", "*.JPG", "*.JPEG", "*.PNG"]:
    imagenes.extend(
        glob.glob(os.path.join("calibracion/fotos", extension))
    )

# Ordenar las imagenes
imagenes.sort()

gray = None

# Recorrer todas las imagenes
for ruta in imagenes:

    # Leer la imagen
    img = cv2.imread(ruta)

    # Si no se puede leer, pasar a la siguiente
    if img is None:
        continue

    # Convertir la imagen a escala de grises
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Buscar las esquinas del tablero
    encontrado, corners = cv2.findChessboardCorners(
        gray,
        CHECKERBOARD,
        cv2.CALIB_CB_ADAPTIVE_THRESH
        + cv2.CALIB_CB_NORMALIZE_IMAGE
        + cv2.CALIB_CB_FAST_CHECK
    )

    # Si encuentra el tablero
    if encontrado:

        # Mejorar la precision de las esquinas
        corners2 = cv2.cornerSubPix(
            gray,
            corners,
            (11, 11),
            (-1, -1),
            criteria
        )

        # Guardar los puntos del tablero
        objpoints.append(objp)

        # Guardar las esquinas detectadas
        imgpoints.append(corners2)

        # Guardar la ruta de la imagen
        rutas_validas.append(ruta)


# Primera calibracion de la camara
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
    objpoints,
    imgpoints,
    gray.shape[::-1],
    None,
    None
)

# Listas para guardar solo las imagenes buenas
objpoints_filtrados = []
imgpoints_filtrados = []

# Calcular el error de cada imagen
for i in range(len(objpoints)):

    # Proyectar los puntos 3D sobre la imagen
    proyectados, _ = cv2.projectPoints(
        objpoints[i],
        rvecs[i],
        tvecs[i],
        mtx,
        dist
    )

    # Comparar puntos detectados y puntos proyectados
    diferencia = imgpoints[i] - proyectados

    # Calcular el error de reproyeccion
    error = np.sqrt(
        np.mean(
            np.sum(diferencia ** 2, axis=2)
        )
    )

    # Guardar solo las imagenes con poco error
    if error <= UMBRAL_ERROR:
        objpoints_filtrados.append(objpoints[i])
        imgpoints_filtrados.append(imgpoints[i])

# Mostrar cuantas imagenes se han utilizado
print("Imagenes iniciales:", len(objpoints))
print("Imagenes tras filtrado:", len(objpoints_filtrados))


# Segunda calibracion usando solo las imagenes buenas
ret2, mtx2, dist2, rvecs2, tvecs2 = cv2.calibrateCamera(
    objpoints_filtrados,
    imgpoints_filtrados,
    gray.shape[::-1],
    None,
    None
)

# Mostrar el error final
print()
print("Error de calibracion filtrada:", ret2)

# Mostrar la matriz de la camara
print()
print("Matriz de camara:")
print(mtx2)

# Mostrar los coeficientes de distorsion
print()
print("Coeficientes de distorsion:")
print(dist2)


# Crear el archivo donde se guardara la calibracion
fs = cv2.FileStorage(
    "calibracion/CameraModel_filtrado.yml",
    cv2.FILE_STORAGE_WRITE
)

# Guardar la matriz de la camara
fs.write("cameraMatrix", mtx2)

# Guardar los coeficientes de distorsion
fs.write("distCoeffs", dist2)

# Cerrar el archivo
fs.release()

print()
print("Guardado en calibracion/CameraModel_filtrado.yml")