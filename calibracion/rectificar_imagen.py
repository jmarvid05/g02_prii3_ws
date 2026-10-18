import cv2
import numpy as np

# Imagen que vamos a rectificar
ruta_imagen = "calibracion/fotos/2026-09-24-194027.jpg"

# Archivo con los parametros de calibracion
ruta_calibracion = "calibracion/CameraModel.yml"


# Cargar parametros de calibracion
fs = cv2.FileStorage(
    ruta_calibracion,
    cv2.FILE_STORAGE_READ
)

camera_matrix = fs.getNode("cameraMatrix").mat()
dist_coeffs = fs.getNode("distCoeffs").mat()

fs.release()


# Cargar imagen original
img = cv2.imread(ruta_imagen)

if img is None:
    print("No se pudo cargar la imagen")
    exit()


h, w = img.shape[:2]


# Calcular una nueva matriz de camara
new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(
    camera_matrix,
    dist_coeffs,
    (w, h),
    1,
    (w, h)
)


# Rectificar la imagen
rectificada = cv2.undistort(
    img,
    camera_matrix,
    dist_coeffs,
    None,
    new_camera_matrix
)


# Añadir textos para comparar
original = img.copy()

cv2.putText(
    original,
    "ORIGINAL",
    (40, 60),
    cv2.FONT_HERSHEY_SIMPLEX,
    1.5,
    (0, 255, 0),
    3
)

cv2.putText(
    rectificada,
    "RECTIFICADA",
    (40, 60),
    cv2.FONT_HERSHEY_SIMPLEX,
    1.5,
    (0, 255, 0),
    3
)


# Poner las dos imagenes una al lado de la otra
comparacion = np.hstack(
    (original, rectificada)
)


# Reducir solo para visualizar en pantalla
escala = 0.5

comparacion_pantalla = cv2.resize(
    comparacion,
    None,
    fx=escala,
    fy=escala
)


# Guardar resultado completo
cv2.imwrite(
    "calibracion/comparacion_rectificacion.jpg",
    comparacion
)


# Mostrar
cv2.imshow(
    "Original vs Rectificada",
    comparacion_pantalla
)

print("Comparacion guardada en:")
print("calibracion/comparacion_rectificacion.jpg")

cv2.waitKey(0)
cv2.destroyAllWindows()
