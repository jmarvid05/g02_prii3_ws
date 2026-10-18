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

## 7. Calibración de cámara

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

## 8. Rectificación de imagen

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

## 9. Detección de ArUco

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

## 10. Launch de visión

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

## 11. Comprobaciones

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

## 12. Editar y recompilar

Editar el movimiento:

```bash
vim ~/g02_prii3_ws/src/g02_prii3_move_jetbot/g02_prii3_move_jetbot/draw_number_jetbot.py
```

Después de realizar cambios:

```bash
cd ~/g02_prii3_ws
source /opt/ros/foxy/setup.bash
source ~/jetbot_ws/install/setup.bash
colcon build --packages-select g02_prii3_move_jetbot
source install/setup.bash
```

## 13. Parar el robot

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
