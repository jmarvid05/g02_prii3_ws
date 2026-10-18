# g02_prii3_ws - Sprint 2

Workspace de ROS 2 del grupo 02 para la asignatura Robots Inteligentes.

## Requisitos

### Simulación

- Ubuntu 22.04 LTS
- ROS 2 Humble
- Python 3
- TurtleBot3
- Gazebo
- RViz2
- OpenCV
- cv_bridge

### JetBot real

El JetBot utiliza ROS 2 Foxy. Las instrucciones específicas para el robot real se encuentran en `README_JETBOT.md`.

## Paquetes

El Sprint 2 utiliza dos paquetes:

- `g02_prii3_move_turtlebot`: nodos utilizados para la simulación con TurtleBot3 en Gazebo.
- `g02_prii3_move_jetbot`: nodos destinados al robot real JetBot, incluyendo movimiento y visión.

## PBI 2.1 - Movimiento autónomo

### Simulación

El nodo:

```text
draw_number
```

publica mensajes de tipo:

```text
geometry_msgs/msg/Twist
```

en:

```text
/cmd_vel
```

para realizar la trayectoria correspondiente al número 2.

La simulación se ejecuta con:

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws
source /opt/ros/humble/setup.bash
colcon build --packages-select g02_prii3_move_turtlebot
source install/setup.bash
ros2 launch g02_prii3_move_turtlebot draw_number.launch.py
```

El fichero launch inicia automáticamente:

- Gazebo
- Mundo vacío de TurtleBot3
- TurtleBot3 Burger
- Nodo `draw_number`
- Nodo `trail_node`
- RViz2

### Servicios de control del dibujo

El nodo `draw_number` dispone de tres servicios:

- `/detener_dibujo`: detiene temporalmente el movimiento.
- `/reanudar_dibujo`: continúa desde el punto en el que se detuvo.
- `/reiniciar_dibujo`: reinicia la trayectoria desde el primer estado.

Los tres utilizan:

```text
std_srvs/srv/Trigger
```

Detener:

```bash
ros2 service call /detener_dibujo std_srvs/srv/Trigger "{}"
```

Reanudar:

```bash
ros2 service call /reanudar_dibujo std_srvs/srv/Trigger "{}"
```

Reiniciar:

```bash
ros2 service call /reiniciar_dibujo std_srvs/srv/Trigger "{}"
```

El nodo muestra por terminal cuándo el dibujo ha sido detenido, reanudado o reiniciado.

### Rastro en RViz

El nodo:

```text
trail_node
```

recibe la odometría desde:

```text
/odom
```

y publica un:

```text
nav_msgs/msg/Path
```

en:

```text
/robot_path
```

RViz utiliza:

```text
Fixed Frame: odom
Path -> /robot_path
```

para visualizar el recorrido del TurtleBot3.

### JetBot real

La versión para robot real se encuentra en:

```text
src/g02_prii3_move_jetbot/g02_prii3_move_jetbot/draw_number_jetbot.py
```

También dispone de los servicios:

```text
/detener_dibujo
/reanudar_dibujo
/reiniciar_dibujo
```

Las instrucciones completas de ejecución están en `README_JETBOT.md`.

## PBI 2.2 - Evitación de obstáculos

Pendiente de completar.

Se implementarán para simulación y robot real:

```text
collision_avoidance
obstacle_avoidance
```

`collision_avoidance` detendrá el robot al detectar un obstáculo delante y reanudará la marcha cuando desaparezca.

`obstacle_avoidance` permitirá esquivar el obstáculo sin detener la marcha.

## PBI 2.3 - Calibración de cámara y ArUco

La parte de visión está incluida en el paquete:

```text
g02_prii3_move_jetbot
```

### Calibración de cámara

Se utilizaron imágenes de un tablero de ajedrez tomadas desde diferentes posiciones y ángulos.

El patrón utilizado contiene:

```text
13 x 9 esquinas interiores
```

El proceso realizado es:

1. Detección del tablero con `cv2.findChessboardCorners()`.
2. Refinado subpíxel con `cv2.cornerSubPix()`.
3. Cálculo de los parámetros con `cv2.calibrateCamera()`.
4. Análisis del error de reproyección.
5. Filtrado de imágenes con mayor error.
6. Generación del fichero de calibración.

El fichero final se encuentra en:

```text
src/g02_prii3_move_jetbot/config/CameraModel.yml
```

Contiene:

```text
cameraMatrix
distCoeffs
```

La calibración filtrada utilizada obtuvo un error aproximado de:

```text
1.19
```

### Rectificación de imagen

El nodo:

```text
camera_rectification
```

carga `CameraModel.yml`, recibe imágenes desde el topic de la cámara y muestra simultáneamente:

```text
ORIGINAL
RECTIFICADA
```

El nodo utiliza `cv2.undistort()` para corregir la distorsión de la imagen.

### Detección ArUco

El nodo:

```text
aruco_detection
```

utiliza el diccionario:

```text
DICT_4X4_50
```

y muestra:

- El ID de cada marcador detectado.
- El contorno del marcador.
- Los ejes de orientación 3D.

En las imágenes de prueba se detectaron correctamente los IDs:

```text
21
36
```

El tamaño configurado actualmente para el marcador es:

```text
0.05 m
```

Este valor debe ajustarse al tamaño físico real del ArUco si se necesita una escala de traslación precisa.

### Launch de visión

Los dos nodos de visión se pueden ejecutar conjuntamente con:

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 launch g02_prii3_move_jetbot vision_jetbot.launch.py
```

Por defecto se utiliza:

```text
/camera/image_raw
```

El topic puede cambiarse al lanzar:

```bash
ros2 launch g02_prii3_move_jetbot vision_jetbot.launch.py image_topic:=/topic/de/la/camara
```

### Prueba sin el JetBot

Para comprobar el sistema sin disponer físicamente del robot, se puede publicar una imagen guardada en `/camera/image_raw`:

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
python3 calibracion/publicar_imagen_ros.py
```

En otra terminal:

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 launch g02_prii3_move_jetbot vision_jetbot.launch.py
```

Se abren dos ventanas:

```text
Original vs Rectificada
Deteccion ArUco
```

## Compilar los paquetes del Sprint 2

Desde la raíz del workspace:

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws
source /opt/ros/humble/setup.bash
colcon build --packages-select g02_prii3_move_turtlebot g02_prii3_move_jetbot
source install/setup.bash
```

## Ejecución manual de nodos

Movimiento en simulación:

```bash
ros2 run g02_prii3_move_turtlebot draw_number
```

Rastro:

```bash
ros2 run g02_prii3_move_turtlebot trail_node
```

Rectificación:

```bash
ros2 run g02_prii3_move_jetbot camera_rectification
```

ArUco:

```bash
ros2 run g02_prii3_move_jetbot aruco_detection
```

## Grupo

Grupo 02
