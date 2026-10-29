import cv2

# Configuracion
CAMARA = 1
TAMANO_ARUCO = 0.05
CALIBRACION = 'src/g02_prii3_move_jetbot/config/CameraModel.yml'

# Cargar calibracion
fs = cv2.FileStorage(CALIBRACION, cv2.FILE_STORAGE_READ)
camera_matrix = fs.getNode('cameraMatrix').mat()
dist_coeffs = fs.getNode('distCoeffs').mat()
fs.release()

# Configurar detector ArUco
diccionario = cv2.aruco.getPredefinedDictionary(
    cv2.aruco.DICT_4X4_100
)

parametros = cv2.aruco.DetectorParameters_create()

# Abrir webcam
camara = cv2.VideoCapture(CAMARA)

while True:

    # Leer imagen de la webcam
    ret, frame = camara.read()

    if not ret:
        break

    # Detectar ArUcos
    esquinas, ids, _ = cv2.aruco.detectMarkers(
        frame,
        diccionario,
        parameters=parametros
    )

    # Si se detecta algun ArUco
    if ids is not None:

        # Dibujar borde e ID
        cv2.aruco.drawDetectedMarkers(
            frame,
            esquinas,
            ids
        )

        # Calcular posicion y orientacion
        rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(
            esquinas,
            TAMANO_ARUCO,
            camera_matrix,
            dist_coeffs
        )

        # Dibujar ejes XYZ en cada ArUco
        for rvec, tvec in zip(rvecs, tvecs):

            cv2.drawFrameAxes(
                frame,
                camera_matrix,
                dist_coeffs,
                rvec,
                tvec,
                TAMANO_ARUCO
            )

    # Mostrar resultado
    cv2.imshow('ArUco tiempo real', frame)

    # Salir pulsando Q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cerrar
camara.release()
cv2.destroyAllWindows()