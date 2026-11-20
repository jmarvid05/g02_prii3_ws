# Sprint 1 - Turtlesim

## Objetivo

Hacer que `turtlesim` dibuje el número **2** de forma autónoma y permitir detener, reanudar y reiniciar el dibujo mediante servicios ROS 2.

## Paquete

```text
g02_prii3_turtlesim
```

El nodo principal publica velocidades en:

```text
/turtle1/cmd_vel
```

utilizando mensajes:

```text
geometry_msgs/Twist
```

La trayectoria se divide en movimientos lineales y giros para formar el número 2.

## Compilación y ejecución

Desde la raíz del workspace:

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws

source /opt/ros/humble/setup.bash

colcon build --packages-select g02_prii3_turtlesim

source install/setup.bash

ros2 launch g02_prii3_turtlesim dibujar_2.launch.py
```

El launch inicia `turtlesim` y el nodo encargado de realizar el dibujo.

## Servicios

El nodo dispone de tres servicios:

```text
/detener_dibujo
/reanudar_dibujo
/reiniciar_dibujo
```

En otra terminal:

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws

source /opt/ros/humble/setup.bash
source install/setup.bash
```

### Detener

```bash
ros2 service call /detener_dibujo std_srvs/srv/Trigger "{}"
```

### Reanudar

```bash
ros2 service call /reanudar_dibujo std_srvs/srv/Trigger "{}"
```

### Reiniciar

```bash
ros2 service call /reiniciar_dibujo std_srvs/srv/Trigger "{}"
```

## Comprobaciones

```bash
ros2 node list
ros2 topic info /turtle1/cmd_vel
ros2 service list
```

## Código principal

```text
src/g02_prii3_turtlesim/g02_prii3_turtlesim/dibujar_2.py
```