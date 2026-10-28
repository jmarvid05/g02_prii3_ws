# Sprint 1 - Turtlesim

## Objetivo

Hacer que turtlesim dibuje el numero **2** y poder **detener, reanudar y reiniciar** el dibujo.

## Como funciona

El nodo `dibujar_2` tiene un **publisher**:

```text
dibujar_2 -- geometry_msgs/Twist --> /turtle1/cmd_vel --> turtlesim
```

- `linear.x`: avance.
- `angular.z`: giro.
- La trayectoria se divide en acciones con una duracion.

Ademas ofrece tres **servicios** `std_srvs/srv/Trigger`:

```text
/detener_dibujo
/reanudar_dibujo
/reiniciar_dibujo
```

## Comandos - ejecucion

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws
source /opt/ros/humble/setup.bash
colcon build --packages-select g02_prii3_turtlesim
source install/setup.bash
ros2 launch g02_prii3_turtlesim dibujar_2.launch.py
```

## Comandos - servicios

En otra terminal:

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
```

```bash
ros2 service call /detener_dibujo std_srvs/srv/Trigger "{}"
ros2 service call /reanudar_dibujo std_srvs/srv/Trigger "{}"
ros2 service call /reiniciar_dibujo std_srvs/srv/Trigger "{}"
```

## Comandos - comprobar ROS

```bash
ros2 node list
ros2 topic info /turtle1/cmd_vel
ros2 service list
```

## Codigo principal

```text
src/g02_prii3_turtlesim/g02_prii3_turtlesim/dibujar_2.py
```
