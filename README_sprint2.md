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

Se han implementado dos comportamientos de evitación de obstáculos tanto para simulación como para el JetBot real:

- `collision_avoidance`: el robot se detiene cuando detecta un obstáculo delante y reanuda el dibujo cuando el obstáculo desaparece.
- `obstacle_avoidance`: el robot esquiva el obstáculo sin quedarse detenido y después continúa el dibujo.

### Collision avoidance

El nodo utiliza los datos del LiDAR publicados como `sensor_msgs/msg/LaserScan`.

Mientras no haya ningún obstáculo delante, el robot continúa ejecutando la trayectoria del número 2.

Si detecta un obstáculo dentro de la distancia de seguridad, publica velocidad cero en `/cmd_vel` y congela el contador de la trayectoria. De esta forma, al desaparecer el obstáculo, el robot continúa desde el mismo punto lógico del dibujo.

#### Simulación

El nodo de simulación se encuentra en:

```text
src/g02_prii3_move_turtlebot/g02_prii3_move_turtlebot/collision_avoidance.py
```

La zona frontal analizada es aproximadamente de `-15°` a `+15°` y la distancia de seguridad utilizada es:

```text
0.45 m
```

Para probarlo, primero se inicia Gazebo:

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
export TURTLEBOT3_MODEL=burger
ros2 launch turtlebot3_gazebo empty_world.launch.py
```

En otra terminal:

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 run g02_prii3_move_turtlebot collision_avoidance
```

Comportamiento comprobado en simulación:

```text
Dibuja el 2
-> detecta un obstáculo delante
-> se detiene
-> el obstáculo desaparece
-> reanuda el dibujo desde donde se había detenido
```

#### JetBot real

La versión para el robot real se encuentra en:

```text
src/g02_prii3_move_jetbot/g02_prii3_move_jetbot/collision_avoidance.py
```

Ejecución:

```bash
ros2 run g02_prii3_move_jetbot collision_avoidance
```

El topic del LiDAR es configurable mediante el parámetro `scan_topic`.

Por defecto:

```text
/scan
```

Si el LiDAR del JetBot utiliza otro topic:

```bash
ros2 run g02_prii3_move_jetbot collision_avoidance --ros-args -p scan_topic:=/topic_del_lidar
```

La lógica está implementada y compilada, pero debe validarse físicamente en el JetBot.

### Obstacle avoidance

El nodo `obstacle_avoidance` evita el obstáculo sin quedarse parado.

El LiDAR divide el entorno en tres sectores:

```text
Frente:     -20° a +20°
Izquierda:  +20° a +90°
Derecha:    -90° a -20°
```

Cuando se detecta un obstáculo delante, el robot compara las distancias izquierda y derecha y elige el lado con más espacio libre.

La maniobra está dividida en tres fases:

1. `GIRO_SALIDA`: avanza mientras gira hacia el lado elegido.
2. `AVANCE`: continúa avanzando para superar el obstáculo.
3. `GIRO_RETORNO`: avanza mientras gira hacia el lado contrario para recuperar aproximadamente la orientación anterior.

Mientras se realiza la esquiva, el contador del dibujo del número 2 queda congelado. Al terminar la maniobra, el dibujo continúa desde el estado en el que se encontraba.

#### Simulación

El nodo se encuentra en:

```text
src/g02_prii3_move_turtlebot/g02_prii3_move_turtlebot/obstacle_avoidance.py
```

Ejecución:

```bash
ros2 run g02_prii3_move_turtlebot obstacle_avoidance
```

Valores comprobados en simulación:

```text
Distancia de detección: 0.50 m
Velocidad lineal durante la esquiva: 0.10 m/s
Velocidad angular durante los giros: +/-0.8 rad/s
GIRO_SALIDA: 15 ciclos
AVANCE: 25 ciclos
GIRO_RETORNO: 15 ciclos
```

El temporizador del nodo se ejecuta cada `0.1 s`, por lo que los 15 ciclos de giro corresponden aproximadamente a `1.5 s` y los 25 ciclos de avance a `2.5 s`.

El comportamiento se ha probado en Gazebo y el TurtleBot rodea el obstáculo sin quedarse parado, recupera aproximadamente su orientación y continúa la trayectoria.

#### JetBot real

La versión para el JetBot se encuentra en:

```text
src/g02_prii3_move_jetbot/g02_prii3_move_jetbot/obstacle_avoidance.py
```

Ejecución:

```bash
ros2 run g02_prii3_move_jetbot obstacle_avoidance
```

También permite modificar el topic del LiDAR:

```bash
ros2 run g02_prii3_move_jetbot obstacle_avoidance --ros-args -p scan_topic:=/topic_del_lidar
```

Los valores iniciales de la maniobra son los mismos que los comprobados en simulación. La lógica está implementada y compilada, pero los tiempos, velocidades y distancias deben comprobarse y ajustarse físicamente en el JetBot si fuera necesario.
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

Collision avoidance en simulación:

```bash
ros2 run g02_prii3_move_turtlebot collision_avoidance
```

Obstacle avoidance en simulación:

```bash
ros2 run g02_prii3_move_turtlebot obstacle_avoidance
```

Collision avoidance en JetBot:

```bash
ros2 run g02_prii3_move_jetbot collision_avoidance
```

Obstacle avoidance en JetBot:

```bash
ros2 run g02_prii3_move_jetbot obstacle_avoidance
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