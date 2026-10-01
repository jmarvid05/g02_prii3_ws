# g02_prii3_ws/sprint2

Workspace de ROS 2 del grupo 02 para la asignatura Robots Inteligentes.

## Requisitos

- Ubuntu 22.04 LTS
- ROS 2 Humble
- Python 3
- TurtleBot3
- Gazebo
- RViz2

## Paquete

El workspace contiene el paquete:

g02_prii3_move_turtlebot

Este paquete controla un TurtleBot3 de forma autónoma para realizar la trayectoria correspondiente al número 2.

También incluye:

- Publicación de velocidad en `/cmd_vel`
- Lectura de odometría desde `/odom`
- Generación de un rastro de la trayectoria en `/robot_path`
- Visualización del recorrido en RViz

## Compilación

Situarse en la raíz del workspace del sprint 2:

    cd ~/UNI/PROYECTOS3/g02_prii3_ws/sprint2 #o tu carpeta correspondiente

Cargar ROS 2 Humble:

    source /opt/ros/humble/setup.bash

Compilar:

    colcon build --packages-select g02_prii3_move_turtlebot

Cargar el workspace:

    source install/setup.bash

## Ejecución

Ejecutar la simulación desde un único fichero launch:

    ros2 launch g02_prii3_move_turtlebot draw_number.launch.py

El fichero launch inicia automáticamente:

- Gazebo
- Mundo vacío de TurtleBot3
- TurtleBot3 Burger
- Nodo `draw_number`
- Nodo `trail_node`
- RViz2

Se espera unos segundos antes de iniciar los nodos para dar tiempo a Gazebo a cargar correctamente.

## Nodo draw_number

El nodo:

    draw_number

publica mensajes de tipo:

    geometry_msgs/msg/Twist

en el topic:

    /cmd_vel

Los principales valores utilizados son:

    linear.x

para controlar la velocidad lineal del robot, y:

    angular.z

para controlar la velocidad angular.

La trayectoria se divide en diferentes estados para formar el número 2.

## Nodo trail_node

El nodo:

    trail_node

recibe la odometría del robot desde:

    /odom

y genera un mensaje de tipo:

    nav_msgs/msg/Path

que se publica en:

    /robot_path

Este topic permite visualizar en RViz el recorrido realizado por el TurtleBot3.

## RViz

RViz se inicia automáticamente desde el fichero launch utilizando una configuración guardada.

La configuración utiliza:

    Fixed Frame: odom

y muestra:

    Path -> /robot_path

De esta forma se puede visualizar el rastro generado por el movimiento del robot.

## Ejecución manual de los nodos

Si se desea ejecutar únicamente el nodo de movimiento:

    ros2 run g02_prii3_move_turtlebot draw_number

Para ejecutar únicamente el nodo del rastro:

    ros2 run g02_prii3_move_turtlebot trail_node

## Grupo

Grupo 02