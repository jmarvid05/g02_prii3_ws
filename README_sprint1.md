# g02_prii3_ws - Sprint 1

Workspace de ROS 2 del grupo 02 para la asignatura Robots Inteligentes.

## Requisitos

- Ubuntu 22.04 LTS
- ROS 2 Humble
- Python 3
- turtlesim

## Paquete

El Sprint 1 utiliza el paquete:

`g02_prii3_turtlesim`

Este paquete controla turtlesim de forma autónoma para dibujar el número 2.

También dispone de servicios ROS 2 para:

- Detener el dibujo
- Reanudar el dibujo
- Reiniciar el dibujo

## Comandos juntos

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws
source /opt/ros/humble/setup.bash
colcon build --packages-select g02_prii3_turtlesim
source install/setup.bash
ros2 launch g02_prii3_turtlesim dibujar_2.launch.py
```

## Compilación

Situarse en la raíz del workspace:

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws
```

Cargar ROS 2 Humble:

```bash
source /opt/ros/humble/setup.bash
```

Compilar:

```bash
colcon build --packages-select g02_prii3_turtlesim
```

Cargar el workspace:

```bash
source install/setup.bash
```

## Ejecución

Ejecutar turtlesim y el nodo de control desde un único fichero launch:

```bash
ros2 launch g02_prii3_turtlesim dibujar_2.launch.py
```

La tortuga dibujará automáticamente el número 2.

## Servicios

En otra terminal:

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
```

Detener el dibujo:

```bash
ros2 service call /detener_dibujo std_srvs/srv/Trigger "{}"
```

Reanudar el dibujo:

```bash
ros2 service call /reanudar_dibujo std_srvs/srv/Trigger "{}"
```

Reiniciar el dibujo:

```bash
ros2 service call /reiniciar_dibujo std_srvs/srv/Trigger "{}"
```

## Grupo

Grupo 02