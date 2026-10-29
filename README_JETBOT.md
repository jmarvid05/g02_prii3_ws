# JetBot 02 / jetbot03M

## Datos

```text
IP: 172.16.190.184
Usuario SSH: jetbot
ROS 2: Foxy
ROS_DOMAIN_ID: 184
```

## Conectar por SSH

```bash
ssh jetbot@172.16.190.184
```

## Idea ROS usada

```text
PUBLISHER ---- topic ----> SUBSCRIBER
```

En el JetBot:

```text
collision_avoidance SUBSCRIBE /filtered_scan
collision_avoidance PUBLISH   /cmd_vel
laser_filter        SUBSCRIBE /scan
laser_filter        PUBLISH   /filtered_scan
```

El controlador base del JetBot esta suscrito a `/cmd_vel`.

---

# 1. Terminal 1 - arrancar la base

```bash
source /opt/ros/foxy/setup.bash
source ~/jetbot_ws/install/setup.bash
export ROS_DOMAIN_ID=184
export ROS_LOCALHOST_ONLY=0
ros2 launch jetbot_pro_ros2 jetbot.py
```

Dejar esta terminal abierta.

# 2. Terminal 2 - preparar el proyecto

```bash
cd ~/g02_prii3_ws
source /opt/ros/foxy/setup.bash
source ~/jetbot_ws/install/setup.bash
colcon build --packages-select g02_prii3_move_jetbot
source install/setup.bash
export ROS_DOMAIN_ID=184
export ROS_LOCALHOST_ONLY=0
```

# 3. Movimiento autonomo

```bash
ros2 launch g02_prii3_move_jetbot draw_number_jetbot.launch.py
```

Valores del robot real:

```text
Curva:    linear 0.12  angular -0.55  75 ciclos
Diagonal: linear 0.12  angular  0.00  35 ciclos
Giro:     linear 0.00  angular  0.80  34 ciclos
Base:     linear 0.12  angular  0.00  33 ciclos
```

Servicios:

```bash
ros2 service call /detener_dibujo std_srvs/srv/Trigger "{}"
ros2 service call /reanudar_dibujo std_srvs/srv/Trigger "{}"
ros2 service call /reiniciar_dibujo std_srvs/srv/Trigger "{}"
```

# 4. LiDAR y filtro

Comprobar el sensor:

```bash
ros2 topic type /scan
ros2 interface show sensor_msgs/msg/LaserScan
ros2 topic echo /scan --once
ros2 topic hz /scan
```

El filtro hace:

```text
/scan -> laser_filter -> /filtered_scan
```

Ejecucion manual:

```bash
ros2 run g02_prii3_move_jetbot laser_filter
```

Parametros:

```bash
ros2 param set /laser_filter laser_angle 60.0
ros2 param set /laser_filter distance 2.0
```

# 5. Collision avoidance

Funcionamiento:

```text
/filtered_scan -> collision_avoidance -> /cmd_vel

obstaculo delante -> Twist = 0 y contador congelado
camino libre      -> continua el dibujo
```

Ejecucion recomendada, con filtro incluido:

```bash
ros2 launch g02_prii3_move_jetbot collision_avoidance_jetbot.launch.py
```

Valores iniciales:

```text
distance = 0.30 m
front_angle_deg = 30
front_offset_deg = 180
```

# 6. Comprobar publishers/subscribers

```bash
ros2 node info /laser_filter
ros2 node info /collision_avoidance
ros2 topic info /scan -v
ros2 topic info /filtered_scan -v
ros2 topic info /cmd_vel -v
```

# 7. Camara

Topic usado:

```text
/camera/image_raw
```

Comprobar stream:

```bash
ros2 topic hz /camera/image_raw
```

Ver desde el portatil:

```bash
ros2 run rqt_image_view rqt_image_view
```

Vision del proyecto:

```bash
ros2 launch g02_prii3_move_jetbot vision_jetbot.launch.py
```

# 8. Parar el robot

Cerrar el nodo:

```text
Ctrl+C
```

Parada manual de emergencia desde ROS:

```bash
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.0}, angular: {z: 0.0}}"
```

> No ejecutar dos nodos de movimiento al mismo tiempo: competirian publicando sobre `/cmd_vel`.
