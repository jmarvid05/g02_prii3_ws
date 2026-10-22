import cv2

# Ruta de la imagen donde queremos detectar el ArUco
ruta_imagen = "calibracion/fotos/2026-09-24-194027.jpg"

# Ruta de los datos de calibracion de la camara
ruta_calibracion = "calibracion/CameraModel.yml"

# Tamaño real del marcador ArUco
MARKER_SIZE = 0.05  # 5 cm


# Cargar la imagen
img = cv2.imread(ruta_imagen)

# Comprobar que la imagen se ha cargado
if img is None:
    print("No se pudo cargar la imagen")
    exit()

# Convertir la imagen a escala de grises
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


# Abrir el archivo de calibracion
fs = cv2.FileStorage(
    ruta_calibracion,
    cv2.FILE_STORAGE_READ
)

# Leer la matriz de la camara
camera_matrix = fs.getNode("cameraMatrix").mat()

# Leer los coeficientes de distorsion
dist_coeffs = fs.getNode("distCoeffs").mat()

# Cerrar el archivo
fs.release()


# Seleccionar el diccionario de ArUcos
diccionario = cv2.aruco.Dictionary_get(
    cv2.aruco.DICT_4X4_50
)

# Crear los parametros del detector
parametros = cv2.aruco.DetectorParameters_create()


# Detectar los marcadores ArUco
corners, ids, rechazados = cv2.aruco.detectMarkers(
    gray,
    diccionario,
    parameters=parametros
)


# Comprobar si se ha detectado algun ArUco
if ids is not None:

    # Dibujar el contorno de los ArUcos detectados
    cv2.aruco.drawDetectedMarkers(
        img,
        corners,
        ids
    )

    # Calcular la posicion y orientacion 3D de cada ArUco
    rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(
        corners,
        MARKER_SIZE,
        camera_matrix,
        dist_coeffs
    )

    # Recorrer todos los ArUcos detectados
    for i in range(len(ids)):

        # Obtener el ID del marcador
        marker_id = ids[i][0]

        print("ArUco detectado - ID:", marker_id)

        # Dibujar los ejes X, Y, Z del marcador
        cv2.drawFrameAxes(
            img,
            camera_matrix,
            dist_coeffs,
            rvecs[i],
            tvecs[i],
            MARKER_SIZE * 0.5
        )

        # Obtener una esquina del ArUco
        esquina = corners[i][0][0]

        x = int(esquina[0])
        y = int(esquina[1])

        # Escribir el ID encima del marcador
        cv2.putText(
            img,
            f"ID: {marker_id}",
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

else:
    print("No se han detectado ArUcos")


# Guardar la imagen con el resultado
cv2.imwrite(
    "calibracion/aruco_detectado.jpg",
    img
)


# Reducir el tamaño para verla mejor en pantalla
pantalla = cv2.resize(
    img,
    None,
    fx=0.6,
    fy=0.6
)

# Mostrar la imagen
cv2.imshow(
    "Deteccion ArUco",
    pantalla
)

# Esperar hasta pulsar una tecla
cv2.waitKey(0)

# Cerrar la ventana
cv2.destroyAllWindows()