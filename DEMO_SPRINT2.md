# Demo Sprint 2 - Chuleta

## 1. Movimiento autonomo - simulacion

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 launch g02_prii3_move_turtlebot draw_number.launch.py
```

Servicios:

```bash
ros2 service call /detener_dibujo std_srvs/srv/Trigger "{}"
ros2 service call /reanudar_dibujo std_srvs/srv/Trigger "{}"
ros2 service call /reiniciar_dibujo std_srvs/srv/Trigger "{}"
```

## 2. Collision avoidance - simulacion

```bash
ros2 launch g02_prii3_move_turtlebot collision_avoidance.launch.py
```

Mostrar que:

```text
/scan -> laser_filter -> /filtered_scan -> collision_avoidance -> /cmd_vel
```

```bash
ros2 node info /laser_filter
ros2 node info /collision_avoidance
```

## 3. JetBot 02 / jetbot03M

```bash
ssh jetbot@172.16.190.184
```

Base:

```bash
source /opt/ros/foxy/setup.bash
source ~/jetbot_ws/install/setup.bash
export ROS_DOMAIN_ID=2
export ROS_LOCALHOST_ONLY=0
ros2 launch jetbot_pro_ros2 jetbot.py
```

Proyecto en otra terminal:

```bash
cd ~/g02_prii3_ws
source /opt/ros/foxy/setup.bash
source ~/jetbot_ws/install/setup.bash
source install/setup.bash
export ROS_DOMAIN_ID=2
export ROS_LOCALHOST_ONLY=0
ros2 launch g02_prii3_move_jetbot collision_avoidance_jetbot.launch.py
```

## Frase clave si preguntan Publisher / Subscriber

> Un publisher envia mensajes a un topic y un subscriber los recibe. En collision_avoidance recibimos LaserScan del LiDAR y publicamos Twist en /cmd_vel para controlar el robot.
