import cv2
import glob
import os

# Numero de esquinas interiores del tablero
CHECKERBOARD = (13, 9)

# Lista donde guardaremos las imagenes encontradas
imagenes = []

# Buscar imagenes dentro de calibracion/fotos
for extension in ["*.jpg", "*.jpeg", "*.png", "*.JPG", "*.JPEG", "*.PNG"]:
    imagenes.extend(
        glob.glob(os.path.join("calibracion/fotos", extension))
    )

# Ordenar las imagenes por nombre
imagenes.sort()

# Contador de imagenes validas
validas = 0

print(f"Imagenes encontradas: {len(imagenes)}")
print()

# Recorrer todas las imagenes
for ruta in imagenes:

    # Leer la imagen
    img = cv2.imread(ruta)

    # Comprobar que se ha podido abrir
    if img is None:
        print(f"[ERROR] {ruta}")
        continue

    # Convertir la imagen a escala de grises
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Buscar las esquinas interiores del tablero
    encontrado, esquinas = cv2.findChessboardCorners(
        gray,
        CHECKERBOARD,
        cv2.CALIB_CB_ADAPTIVE_THRESH
        + cv2.CALIB_CB_NORMALIZE_IMAGE
        + cv2.CALIB_CB_FAST_CHECK
    )

    # Obtener solo el nombre del archivo
    nombre = os.path.basename(ruta)

    if encontrado:

        validas += 1
        print(f"[OK] {nombre}")

        # Dibujar las esquinas detectadas sobre la imagen
        cv2.drawChessboardCorners(
            img,
            CHECKERBOARD,
            esquinas,
            encontrado
        )

        # Mostrar la imagen con las esquinas
        cv2.imshow("Esquinas detectadas", img)

        # Esperar a que pulsemos una tecla
        cv2.waitKey(0)

    else:
        print(f"[NO] {nombre}")

# Cerrar todas las ventanas de OpenCV
cv2.destroyAllWindows()

print()
print(f"Imagenes validas: {validas}/{len(imagenes)}")
