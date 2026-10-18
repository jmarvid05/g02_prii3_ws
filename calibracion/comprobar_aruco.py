import cv2

ruta_imagen = "calibracion/fotos/2026-09-24-194027.jpg"

img = cv2.imread(ruta_imagen)

if img is None:
    print("No se pudo cargar la imagen")
    exit()

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

diccionarios = {
    "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
    "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
    "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
    "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
    "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
    "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
    "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
    "DICT_7X7_50": cv2.aruco.DICT_7X7_50,
    "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL
}

parametros = cv2.aruco.DetectorParameters_create()

for nombre, codigo in diccionarios.items():

    diccionario = cv2.aruco.Dictionary_get(codigo)

    corners, ids, rechazados = cv2.aruco.detectMarkers(
        gray,
        diccionario,
        parameters=parametros
    )

    if ids is not None:
        print(
            nombre,
            "->",
            len(ids),
            "marcadores. IDs:",
            ids.flatten().tolist()
        )
