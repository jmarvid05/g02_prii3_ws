import cv2
import numpy as np

# Configuracion
CAMARA = 1
TAMANO_ARUCO = 0.05
CALIBRACION = 'src/g02_prii3_move_jetbot/config/CameraModel.yml'

# Cargar calibracion
fs = cv2.FileStorage(CALIBRACION, cv2.FILE_STORAGE_READ)
camera_matrix = fs.getNode('cameraMatrix').mat()
dist_coeffs = fs.getNode('distCoeffs').mat()
fs.release()

# Detector ArUco
diccionario = cv2.aruco.getPredefinedDictionary(
    cv2.aruco.DICT_4X4_100
)
parametros = cv2.aruco.DetectorParameters_create()

# Puntos 3D del marcador
mitad = TAMANO_ARUCO / 2

puntos_3d = np.array([
    [-mitad,  mitad, 0],
    [ mitad,  mitad, 0],
    [ mitad, -mitad, 0],
    [-mitad, -mitad, 0],
], dtype=np.float32)

# Abrir webcam
camara = cv2.VideoCapture(CAMARA)

while True:

    ret, frame = camara.read()

    if not ret:
        break

    # Detectar ArUcos
    esquinas, ids, _ = cv2.aruco.detectMarkers(
        frame,
        diccionario,
        parameters=parametros
    )

    if ids is not None:

        # Dibujar borde e ID
        cv2.aruco.drawDetectedMarkers(
            frame,
            esquinas,
            ids
        )

        # Calcular pose y dibujar ejes
        for esquina in esquinas:

            puntos_2d = esquina.reshape(4, 2)

            _, rvec, tvec = cv2.solvePnP(
                puntos_3d,
                puntos_2d,
                camera_matrix,
                dist_coeffs,
                flags=cv2.SOLVEPNP_IPPE_SQUARE
            )

            cv2.drawFrameAxes(
                frame,
                camera_matrix,
                dist_coeffs,
                rvec,
                tvec,
                TAMANO_ARUCO
            )

    # Mostrar imagen
    cv2.imshow('ArUco tiempo real', frame)

    # Salir con Q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camara.release()
cv2.destroyAllWindows()