import cv2

ruta_imagen = "calibracion/fotos/2026-09-24-194027.jpg"
ruta_calibracion = "calibracion/CameraModel.yml"

MARKER_SIZE = 0.05  # 5 cm provisionales

# Cargar imagen
img = cv2.imread(ruta_imagen)

if img is None:
    print("No se pudo cargar la imagen")
    exit()

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Cargar calibracion
fs = cv2.FileStorage(
    ruta_calibracion,
    cv2.FILE_STORAGE_READ
)

camera_matrix = fs.getNode("cameraMatrix").mat()
dist_coeffs = fs.getNode("distCoeffs").mat()

fs.release()

# Diccionario ArUco
diccionario = cv2.aruco.Dictionary_get(
    cv2.aruco.DICT_4X4_50
)

parametros = cv2.aruco.DetectorParameters_create()

# Detectar marcadores
corners, ids, rechazados = cv2.aruco.detectMarkers(
    gray,
    diccionario,
    parameters=parametros
)

if ids is not None:

    cv2.aruco.drawDetectedMarkers(
        img,
        corners,
        ids
    )

    # Estimar pose 3D
    rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(
        corners,
        MARKER_SIZE,
        camera_matrix,
        dist_coeffs
    )

    for i in range(len(ids)):

        marker_id = ids[i][0]

        print("ArUco detectado - ID:", marker_id)

        # Dibujar ejes 3D
        cv2.drawFrameAxes(
            img,
            camera_matrix,
            dist_coeffs,
            rvecs[i],
            tvecs[i],
            MARKER_SIZE * 0.5
        )

        # Mostrar ID sobre la imagen
        esquina = corners[i][0][0]

        x = int(esquina[0])
        y = int(esquina[1])

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

# Guardar resultado
cv2.imwrite(
    "calibracion/aruco_detectado.jpg",
    img
)

# Reducir para visualizar
pantalla = cv2.resize(
    img,
    None,
    fx=0.6,
    fy=0.6
)

cv2.imshow(
    "Deteccion ArUco",
    pantalla
)

cv2.waitKey(0)
cv2.destroyAllWindows()
