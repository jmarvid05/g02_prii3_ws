# Ejecución en JetBot real

Este documento explica cómo ejecutar los nodos desarrollados para el **JetBot real**.

El JetBot utiliza **ROS 2 Foxy**.

## 1. Arrancar el JetBot

En una primera terminal:

```bash
source /opt/ros/foxy/setup.bash
source ~/jetbot_ws/install/setup.bash
ros2 launch jetbot_pro_ros2 jetbot.py
```

Esta terminal debe permanecer abierta mientras se utiliza el robot.

## 2. Descargar o actualizar el proyecto

El repositorio debe estar disponible en:

```text
~/g02_prii3_ws
```

Para clonar desde cero:

```bash
cd ~
git clone https://github.com/jmarvid05/g02_prii3_ws.git
cd ~/g02_prii3_ws
```

Si ya existe:

```bash
cd ~/g02_prii3_ws
git pull origin main
```

## 3. Compilar el paquete del JetBot

En una segunda terminal:

```bash
cd ~/g02_prii3_ws
source /opt/ros/foxy/setup.bash
source ~/jetbot_ws/install/setup.bash
colcon build --packages-select g02_prii3_move_jetbot
source install/setup.bash
```

## 4. Dibujar el número 2

Con la base del JetBot arrancada en la primera terminal:

```bash
cd ~/g02_prii3_ws
source /opt/ros/foxy/setup.bash
source ~/jetbot_ws/install/setup.bash
source install/setup.bash
ros2 launch g02_prii3_move_jetbot draw_number_jetbot.launch.py
```

El código se encuentra en:

```text
src/g02_prii3_move_jetbot/g02_prii3_move_jetbot/draw_number_jetbot.py
```

## 5. Valores ajustados para el robot real

### Estado 0 - Curva

```python
msg.linear.x = 0.12
msg.angular.z = -0.55
self.contador >= 75
```

### Estado 1 - Diagonal recta

```python
msg.linear.x = 0.12
msg.angular.z = 0.0
self.contador >= 35
```

### Estado 2 - Giro a la izquierda

```python
msg.linear.x = 0.0
msg.angular.z = 0.8
self.contador >= 34
```

### Estado 3 - Base recta

```python
msg.linear.x = 0.12
msg.angular.z = 0.0
self.contador >= 33
```

## 6. Servicios de control del dibujo

El nodo `draw_number_jetbot` dispone de tres servicios:

- `/detener_dibujo`
- `/reanudar_dibujo`
- `/reiniciar_dibujo`

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

## 7. Evitación de obstáculos

El paquete `g02_prii3_move_jetbot` incluye dos nodos para el PBI 2.2:

```text
collision_avoidance
obstacle_avoidance
```

Ambos utilizan el LiDAR mediante mensajes `sensor_msgs/msg/LaserScan` y publican el movimiento en `/cmd_vel`.

### Collision avoidance

El nodo `collision_avoidance` continúa dibujando el número 2 mientras el camino está libre.

Cuando detecta un obstáculo delante a menos de la distancia de seguridad, el JetBot se detiene completamente y congela el contador de la trayectoria.

Cuando el obstáculo desaparece, el robot continúa el dibujo desde el punto lógico en el que se encontraba.

Ejecución:

```bash
ros2 run g02_prii3_move_jetbot collision_avoidance
```

Por defecto utiliza:

```text
scan_topic = /scan
```

Si el LiDAR publica en otro topic:

```bash
ros2 run g02_prii3_move_jetbot collision_avoidance --ros-args -p scan_topic:=/topic_del_lidar
```

La distancia de seguridad inicial es:

```text
0.45 m
```

### Obstacle avoidance

El nodo `obstacle_avoidance` esquiva el obstáculo sin quedarse parado.

El LiDAR analiza tres sectores:

```text
Frente:     -20° a +20°
Izquierda:  +20° a +90°
Derecha:    -90° a -20°
```

Al detectar un obstáculo delante, compara el espacio disponible a izquierda y derecha y elige el lado más libre.

La maniobra consta de:

1. `GIRO_SALIDA`: avanza mientras gira para separarse del obstáculo.
2. `AVANCE`: continúa avanzando para superarlo.
3. `GIRO_RETORNO`: gira en sentido contrario mientras avanza para recuperar aproximadamente la orientación anterior.

Ejecución:

```bash
ros2 run g02_prii3_move_jetbot obstacle_avoidance
```

Para utilizar otro topic de LiDAR:

```bash
ros2 run g02_prii3_move_jetbot obstacle_avoidance --ros-args -p scan_topic:=/topic_del_lidar
```

Valores iniciales de la maniobra:

```text
Distancia de detección: 0.50 m
Velocidad lineal durante la esquiva: 0.10 m/s
Velocidad angular durante los giros: +/-0.8 rad/s
GIRO_SALIDA: 15 ciclos
AVANCE: 25 ciclos
GIRO_RETORNO: 15 ciclos
```

La lógica de ambos nodos está implementada y compilada. Antes de dar por definitivos los parámetros del robot real, deben comprobarse físicamente en el JetBot y ajustarse si fuera necesario.

## 8. Calibración de cámara

El fichero de calibración utilizado se encuentra en:

```text
src/g02_prii3_move_jetbot/config/CameraModel.yml
```

Contiene:

```text
cameraMatrix
distCoeffs
```

Los parámetros fueron obtenidos a partir del conjunto de imágenes de calibración utilizado en clase.

## 9. Rectificación de imagen

El nodo:

```text
camera_rectification
```

recibe imágenes de la cámara y muestra una comparación entre:

```text
ORIGINAL
RECTIFICADA
```

El topic de cámara se configura mediante el parámetro:

```text
image_topic
```

Por defecto:

```text
/camera/image_raw
```

Ejecución manual:

```bash
ros2 run g02_prii3_move_jetbot camera_rectification
```

Para utilizar otro topic:

```bash
ros2 run g02_prii3_move_jetbot camera_rectification --ros-args -p image_topic:=/topic/de/la/camara
```

## 10. Detección de ArUco

El nodo:

```text
aruco_detection
```

detecta marcadores del diccionario:

```text
DICT_4X4_50
```

y muestra:

- ID del ArUco.
- Contorno detectado.
- Ejes de orientación 3D.

Ejecución manual:

```bash
ros2 run g02_prii3_move_jetbot aruco_detection
```

El tamaño del marcador está configurado actualmente como:

```text
0.05 m
```

Este valor debe ajustarse al tamaño físico real del ArUco si se necesita una escala de traslación precisa.

## 11. Launch de visión

Para ejecutar rectificación y detección ArUco simultáneamente:

```bash
cd ~/g02_prii3_ws
source /opt/ros/foxy/setup.bash
source ~/jetbot_ws/install/setup.bash
source install/setup.bash
ros2 launch g02_prii3_move_jetbot vision_jetbot.launch.py
```

Si el topic real de la cámara es diferente:

```bash
ros2 launch g02_prii3_move_jetbot vision_jetbot.launch.py image_topic:=/topic/de/la/camara
```

Para conocer los topics disponibles:

```bash
ros2 topic list
```

## 12. Comprobaciones

Nodos activos:

```bash
ros2 node list
```

Servicios del dibujo:

```bash
ros2 service list
```

Deben aparecer:

```text
/detener_dibujo
/reanudar_dibujo
/reiniciar_dibujo
```

Comprobar que el JetBot está suscrito a `/cmd_vel`:

```bash
ros2 node info /jetbot
```

Visualizar los comandos enviados:

```bash
ros2 topic echo /cmd_vel
```

## 13. Editar y recompilar

Editar el movimiento:

```bash
code ~/g02_prii3_ws/src/g02_prii3_move_jetbot/g02_prii3_move_jetbot/draw_number_jetbot.py
```

Después de realizar cambios:

```bash
cd ~/g02_prii3_ws
source /opt/ros/foxy/setup.bash
source ~/jetbot_ws/install/setup.bash
colcon build --packages-select g02_prii3_move_jetbot
source install/setup.bash
```

## 14. Parar el robot

Detener un nodo:

```text
Ctrl+C
```

Si fuera necesario enviar velocidad cero manualmente:

```bash
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.0}, angular: {z: 0.0}}"
```

## Grupo

**Grupo 02**