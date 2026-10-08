# g02_prii3_ws/sprint1

Workspace de ROS 2 del grupo 02 para la asignatura Robots Inteligentes.

## Requisitos

- Ubuntu 22.04 LTS
- ROS 2 Humble
- Python 3

## Paquete

El workspace contiene el paquete:

g02_prii3_turtlesim

Este paquete controla turtlesim de forma autónoma para dibujar el número 2.

También dispone de servicios ROS 2 para:

- Detener el dibujo
- Reanudar el dibujo
- Reiniciar el dibujo

## Compilación

Situarse en la raíz del workspace:

    cd ~/UNI/PROYECTOS3/g02_prii3_ws #o tu carpeta correspondiente

Cargar ROS 2 Humble:

    source /opt/ros/humble/setup.bash

Compilar:

    colcon build --packages-select g02_prii3_turtlesim

Cargar el workspace:

    source install/setup.bash

## Ejecución

Ejecutar turtlesim y el nodo de control desde un único fichero launch:

    ros2 launch g02_prii3_turtlesim dibujar_2.launch.py

La tortuga dibujará automáticamente el número 2.

## Servicios

En otra terminal:

    cd g02_prii3_ws/sprint1
    source /opt/ros/humble/setup.bash
    source install/setup.bash

Detener el dibujo:

    ros2 service call /detener_dibujo std_srvs/srv/Trigger "{}"

Reanudar el dibujo:

    ros2 service call /reanudar_dibujo std_srvs/srv/Trigger "{}"

Reiniciar el dibujo:

    ros2 service call /reiniciar_dibujo std_srvs/srv/Trigger "{}"

## Grupo

Grupo 02