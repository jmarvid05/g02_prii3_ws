# Sprint 2 - Movimiento, LiDAR y visión

## Objetivo

En el Sprint 2 se trabaja con TurtleBot3 en simulación y con el JetBot real.

Los principales apartados son:

- Movimiento autónomo.
- Comunicación mediante publishers y subscribers.
- Control del dibujo mediante servicios.
- Uso del LiDAR para detectar obstáculos.
- Calibración de cámara.
- Detección de marcadores ArUco.

## Paquetes

```text
g02_prii3_move_turtlebot
g02_prii3_move_jetbot
```

`g02_prii3_move_turtlebot` contiene los nodos utilizados con TurtleBot3 en simulación.

`g02_prii3_move_jetbot` contiene los nodos destinados al JetBot real y la parte de visión.

Los comandos específicos del robot real están documentados en:

```text
README_JETBOT.md
```

---

## PBI 2.1 - Movimiento autónomo

### Nodo draw_number

El nodo:

```text
draw_number
```

publica mensajes:

```text
geometry_msgs/msg/Twist
```

en:

```text
/cmd_vel
```

para realizar la trayectoria correspondiente al número 2.

La trayectoria se divide en diferentes tramos utilizando:

```text
linear.x
angular.z
```

### Rastro del robot

El nodo:

```text
trail_node
```

recibe la odometría desde:

```text
/odom
```

y publica:

```text
nav_msgs/msg/Path
```

en:

```text
/robot_path
```

Esto permite visualizar el recorrido del robot en RViz.

### Compilar y ejecutar

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws

source /opt/ros/humble/setup.bash

colcon build --packages-select g02_prii3_move_turtlebot

source install/setup.bash

ros2 launch g02_prii3_move_turtlebot draw_number.launch.py
```

El launch inicia la simulación, el movimiento del robot, el rastro y RViz.

### Servicios

El dibujo dispone de tres servicios:

```text
/detener_dibujo
/reanudar_dibujo
/reiniciar_dibujo
```

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

---

## PBI 2.2 - Detección de obstáculos

El LiDAR publica sus medidas en:

```text
/scan
```

utilizando:

```text
sensor_msgs/msg/LaserScan
```

### Comprobar el LiDAR

```bash
ros2 topic type /scan
ros2 interface show sensor_msgs/msg/LaserScan
ros2 topic echo /scan --once
ros2 topic hz /scan
```

### laser_filter

El nodo `laser_filter` recibe `/scan` y publica los datos filtrados en:

```text
/filtered_scan
```

El flujo es:

```text
LiDAR
  ↓
/scan
  ↓
laser_filter
  ↓
/filtered_scan
```

Algunos parámetros pueden modificarse durante la ejecución:

```bash
ros2 param set /laser_filter laser_angle 60.0
ros2 param set /laser_filter distance 2.0
```

Para comprobar el resultado:

```bash
ros2 topic echo /filtered_scan --once
```

### collision_avoidance

El nodo `collision_avoidance` recibe los datos del LiDAR y controla `/cmd_vel`.

```text
/filtered_scan
      ↓
collision_avoidance
      ↓
   /cmd_vel
```

Funcionamiento:

```text
camino libre
→ el robot continúa la trayectoria

obstáculo delante
→ el robot se detiene

desaparece el obstáculo
→ continúa desde donde se había detenido
```

En simulación se utiliza una distancia de seguridad aproximada de:

```text
0.45 m
```

### Ejecutar en simulación

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws

source /opt/ros/humble/setup.bash
source install/setup.bash

ros2 launch g02_prii3_move_turtlebot collision_avoidance.launch.py
```

### Comprobar publishers y subscribers

```bash
ros2 node info /collision_avoidance
ros2 node info /laser_filter

ros2 topic info /scan -v
ros2 topic info /filtered_scan -v
ros2 topic info /cmd_vel -v
```

---

## PBI 2.3 - Calibración de cámara y ArUco

La parte de visión se encuentra principalmente en:

```text
g02_prii3_move_jetbot
```

### Calibración de cámara

Se utilizaron imágenes de un tablero de ajedrez tomadas desde diferentes posiciones y ángulos.

El proceso de calibración incluye:

```text
detección del tablero
→ refinado de esquinas
→ calibración
→ cálculo del error
→ filtrado
→ CameraModel.yml
```

El fichero de calibración contiene:

```text
cameraMatrix
distCoeffs
```

y se encuentra en la carpeta de configuración del paquete.

### Rectificación

La rectificación utiliza los parámetros obtenidos durante la calibración para corregir la distorsión de la cámara.

El nodo correspondiente utiliza:

```text
cv2.undistort()
```

para generar la imagen rectificada.

### Detección ArUco

En el Sprint 2 se trabajó con:

```text
DICT_4X4_50
```

El detector permite obtener:

```text
ID del marcador
contorno
posición/orientación
```

> En el Sprint 3 se utiliza un detector diferente basado en `DICT_4X4_100`. La documentación correspondiente está en `README_sprint3.md`.

---

## Comunicación ROS 2 utilizada

Ejemplos de publishers y subscribers del Sprint 2:

```text
draw_number
    → /cmd_vel

LiDAR
    → /scan
    → laser_filter
    → /filtered_scan
    → collision_avoidance
    → /cmd_vel

/odom
    → trail_node
    → /robot_path
    → RViz

/camera/image_raw
    → nodos de visión
```

Un nodo puede actuar al mismo tiempo como subscriber y publisher.

---

## Compilar los paquetes del Sprint 2

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws

source /opt/ros/humble/setup.bash

colcon build \
--packages-select \
g02_prii3_move_turtlebot \
g02_prii3_move_jetbot

source install/setup.bash
```

## Comandos útiles

```bash
ros2 node list
ros2 topic list
ros2 service list

ros2 topic info /cmd_vel -v
ros2 topic info /scan -v
ros2 topic info /filtered_scan -v
```

## JetBot real

La configuración, conexión y comandos específicos del JetBot están centralizados en:

```text
README_JETBOT.md
```