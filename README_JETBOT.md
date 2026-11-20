# JetBot real

Este documento contiene la configuración y los comandos específicos utilizados con el **JetBot real**.

## Datos del robot

```text
IP: 172.16.190.172
Usuario SSH: jetbot
ROS 2: Foxy
ROS_DOMAIN_ID: 172
ROS_LOCALHOST_ONLY: 0
```

## Conexión por SSH

Desde el portátil:

```bash
ssh jetbot@172.16.190.172
```

En las terminales ROS del portátil y del JetBot se utiliza:

```bash
export ROS_DOMAIN_ID=172
export ROS_LOCALHOST_ONLY=0
```

Para hacerlo permanente puede añadirse a `~/.bashrc`.

---

# Actualizar el repositorio

Si el repositorio ya existe en el JetBot:

```bash
cd ~/g02_prii3_ws

git checkout main
git pull

git status
```

Si es necesario clonarlo de nuevo:

```bash
cd ~

git clone -b main https://github.com/jmarvid05/g02_prii3_ws.git

cd ~/g02_prii3_ws

git branch
git status
```

El repositorio debe quedar en:

```text
* main
```

---

# Sprint 2

## Arrancar la base del JetBot

En el JetBot:

```bash
source /opt/ros/foxy/setup.bash
source ~/ros2_ws/install/setup.bash

export ROS_DOMAIN_ID=172
export ROS_LOCALHOST_ONLY=0

ros2 launch jetbot_pro_ros2 jetbot.py
```

Esta terminal debe permanecer abierta.

## Preparar el proyecto

```bash
cd ~/g02_prii3_ws

source /opt/ros/foxy/setup.bash
source ~/ros2_ws/install/setup.bash

export ROS_DOMAIN_ID=172
export ROS_LOCALHOST_ONLY=0

colcon build --packages-select g02_prii3_move_jetbot

source install/setup.bash
```

## Movimiento autónomo

```bash
ros2 launch g02_prii3_move_jetbot draw_number_jetbot.launch.py
```

Valores ajustados durante las pruebas con el robot real:

```text
Curva:    linear 0.12   angular -0.55   75 ciclos
Diagonal: linear 0.12   angular  0.00   35 ciclos
Giro:     linear 0.00   angular  0.80   34 ciclos
Base:     linear 0.12   angular  0.00   33 ciclos
```

Servicios:

```bash
ros2 service call /detener_dibujo std_srvs/srv/Trigger "{}"

ros2 service call /reanudar_dibujo std_srvs/srv/Trigger "{}"

ros2 service call /reiniciar_dibujo std_srvs/srv/Trigger "{}"
```

---

## LiDAR

El LiDAR publica en:

```text
/scan
```

Comprobaciones:

```bash
ros2 topic type /scan
ros2 interface show sensor_msgs/msg/LaserScan
ros2 topic echo /scan --once
ros2 topic hz /scan
```

### Filtro

```text
/scan
  ↓
laser_filter
  ↓
/filtered_scan
```

Ejecutar:

```bash
ros2 run g02_prii3_move_jetbot laser_filter
```

Modificar parámetros:

```bash
ros2 param set /laser_filter laser_angle 60.0
ros2 param set /laser_filter distance 2.0
```

---

## Collision avoidance

Flujo:

```text
/filtered_scan
      ↓
collision_avoidance
      ↓
   /cmd_vel
```

Funcionamiento:

```text
obstáculo delante
→ robot detenido

camino libre
→ continúa el movimiento
```

Ejecutar:

```bash
ros2 launch g02_prii3_move_jetbot collision_avoidance_jetbot.launch.py
```

Valores iniciales utilizados:

```text
distance = 0.30 m
front_angle_deg = 30
front_offset_deg = 180
```

---

## Cámara

Topic utilizado:

```text
/camera/image_raw
```

Comprobar:

```bash
ros2 topic hz /camera/image_raw
```

Desde el portátil:

```bash
ros2 run rqt_image_view rqt_image_view
```

Visión del Sprint 2:

```bash
ros2 launch g02_prii3_move_jetbot vision_jetbot.launch.py
```

---

# Sprint 3

## SLAM real

En el JetBot:

```bash
source /opt/ros/foxy/setup.bash
source ~/ros2_ws/install/setup.bash

export ROS_DOMAIN_ID=172
export ROS_LOCALHOST_ONLY=0

ros2 launch jetbot_pro_ros2 slam.py
```

El launch del profesor inicia los nodos necesarios para realizar SLAM con el JetBot.

## RViz para SLAM

Desde el portátil:

```bash
source /opt/ros/humble/setup.bash

export ROS_DOMAIN_ID=172
export ROS_LOCALHOST_ONLY=0

ros2 run rviz2 rviz2 -d ~/slam.rviz
```

## Guardar el mapa

Sin cerrar `slam.py`:

```bash
ros2 run nav2_map_server map_saver_cli -f ~/map
```

Esto genera:

```text
map.yaml
map.pgm
```

## Copiar el mapa al portátil

```bash
scp jetbot@172.16.190.172:~/map.yaml ~/
scp jetbot@172.16.190.172:~/map.pgm ~/
```

El mapa real utilizado actualmente en el repositorio se encuentra en:

```text
mapas/jetbot_real/map.yaml
mapas/jetbot_real/map.pgm
```

---

## Copiar el mapa del repositorio al JetBot

Desde el portátil:

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws

scp mapas/jetbot_real/map.yaml \
jetbot@172.16.190.172:~/

scp mapas/jetbot_real/map.pgm \
jetbot@172.16.190.172:~/
```

El `nav.py` utilizado para navegación real espera:

```text
/home/jetbot/map.yaml
```

---

## Navegación real

En el JetBot:

```bash
source /opt/ros/foxy/setup.bash
source ~/ros2_ws/install/setup.bash

export ROS_DOMAIN_ID=172
export ROS_LOCALHOST_ONLY=0

ros2 launch jetbot_pro_ros2 nav.py
```

Desde el portátil puede abrirse RViz con:

```bash
ros2 run rviz2 rviz2 -d ~/nav2.rviz
```

También puede utilizarse:

```bash
ros2 run rviz2 rviz2 \
-d $(ros2 pkg prefix nav2_bringup)/share/nav2_bringup/rviz/nav2_default_view.rviz
```

---

## `nav.py`

La copia utilizada como referencia en el proyecto está en:

```text
src/g02_prii3_nav_jetbot/launch/nav.py
```

Para copiarla al paquete del profesor en el JetBot:

```bash
scp src/g02_prii3_nav_jetbot/launch/nav.py \
jetbot@172.16.190.172:/home/jetbot/ros2_ws/jetbot_pro_ros2/launch/
```

Después, en el JetBot:

```bash
cd ~/ros2_ws

colcon build

source install/setup.bash
```

---

## Navegación predefinida

El nodo del proyecto es:

```text
g02_prii3_nav_jetbot predefined_navigation
```

Todavía deben introducirse las coordenadas definitivas obtenidas sobre el mapa real antes de realizar la prueba final.

No ejecutar mientras las coordenadas estén configuradas como:

```text
0.0, 0.0
```

---

## Navegación autónoma con ArUco

El paquete contiene:

```text
aruco_detection
autonomous_navigation
```

y el launch:

```text
autonomous_navigation.launch.py
```

La lógica preparada es:

```text
ir a la entrada
→ esperar a llegar
→ empezar a aceptar ArUcos
→ detectar el ID
→ navegar al destino correspondiente
```

Antes de probarlo con el robot real deben obtenerse las coordenadas reales de:

```text
pose intermedia delante del ArUco
destino final
```

No ejecutar la navegación autónoma mientras estas coordenadas estén a `0.0`.

---

# Comprobaciones ROS 2

Nodos:

```bash
ros2 node list
```

Topics:

```bash
ros2 topic list
```

LiDAR:

```bash
ros2 topic info /scan -v
ros2 topic info /filtered_scan -v
```

Movimiento:

```bash
ros2 topic info /cmd_vel -v
ros2 topic echo /cmd_vel
```

ArUco:

```bash
ros2 topic echo /aruco_info
```

Acción de navegación:

```bash
ros2 action list | grep navigate_to_pose
```

---

# Parar el robot

Para cerrar un nodo:

```text
Ctrl+C
```

Si es necesario enviar una velocidad cero:

```bash
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist \
"{linear: {x: 0.0}, angular: {z: 0.0}}"
```

No deben ejecutarse varios nodos que publiquen movimiento sobre `/cmd_vel` al mismo tiempo.