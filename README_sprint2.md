# g02_prii3_ws - Sprint 2

Workspace de ROS 2 del grupo 02 para la asignatura Robots Inteligentes.

## Requisitos

Para la simulación:

- Ubuntu 22.04 LTS
- ROS 2 Humble
- Python 3
- TurtleBot3
- Gazebo
- RViz2

Para el JetBot real se utiliza ROS 2 Foxy. Las instrucciones específicas se encuentran en `README_JETBOT.md`.

## Paquetes

El Sprint 2 utiliza dos paquetes:

- `g02_prii3_move_turtlebot`: contiene los nodos utilizados para la simulación con TurtleBot3 en Gazebo.
- `g02_prii3_move_jetbot`: contiene los nodos destinados al robot real JetBot.

La parte de simulación incluye:

- Publicación de velocidad en `/cmd_vel`
- Lectura de odometría desde `/odom`
- Generación de un rastro de la trayectoria en `/robot_path`
- Visualización del recorrido en RViz
- Servicios para detener, reanudar y reiniciar el dibujo

## Comandos juntos para simulación

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws
source /opt/ros/humble/setup.bash
colcon build --packages-select g02_prii3_move_turtlebot
source install/setup.bash
ros2 launch g02_prii3_move_turtlebot draw_number.launch.py
```

## Compilación de la simulación

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
colcon build --packages-select g02_prii3_move_turtlebot
```

Cargar el workspace:

```bash
source install/setup.bash
```

## Ejecución de la simulación

Ejecutar la simulación desde un único fichero launch:

```bash
ros2 launch g02_prii3_move_turtlebot draw_number.launch.py
```

El fichero launch inicia automáticamente:

- Gazebo
- Mundo vacío de TurtleBot3
- TurtleBot3 Burger
- Nodo `draw_number`
- Nodo `trail_node`
- RViz2

Se espera unos segundos antes de iniciar los nodos para dar tiempo a Gazebo a cargar correctamente.

## Nodo draw_number en simulación

El nodo `draw_number` publica mensajes de tipo:

```text
geometry_msgs/msg/Twist
```

en el topic:

```text
/cmd_vel
```

Los principales valores utilizados son:

```text
linear.x
angular.z
```

La trayectoria se divide en diferentes estados para formar el número 2.

### Servicios de control del dibujo

El nodo `draw_number` dispone de tres servicios ROS que permiten controlar la ejecución de la trayectoria:

- `/detener_dibujo`: detiene temporalmente el movimiento del robot.
- `/reanudar_dibujo`: continúa el dibujo desde el punto en el que se había detenido.
- `/reiniciar_dibujo`: reinicia la trayectoria y comienza de nuevo desde el primer estado.

Los tres servicios utilizan el tipo:

```text
std_srvs/srv/Trigger
```

Para detener el dibujo:

```bash
ros2 service call /detener_dibujo std_srvs/srv/Trigger "{}"
```

Para reanudar el dibujo:

```bash
ros2 service call /reanudar_dibujo std_srvs/srv/Trigger "{}"
```

Para reiniciar el dibujo:

```bash
ros2 service call /reiniciar_dibujo std_srvs/srv/Trigger "{}"
```

Al ejecutar cada servicio, el nodo muestra por terminal si el dibujo ha sido detenido, reanudado o reiniciado.

## Nodo trail_node

El nodo `trail_node` recibe la odometría del robot desde:

```text
/odom
```

y genera un mensaje de tipo:

```text
nav_msgs/msg/Path
```

que se publica en:

```text
/robot_path
```

Este topic permite visualizar en RViz el recorrido realizado por el TurtleBot3.

## RViz

RViz se inicia automáticamente desde el fichero launch utilizando una configuración guardada.

La configuración utiliza:

```text
Fixed Frame: odom
```

y muestra:

```text
Path -> /robot_path
```

De esta forma se puede visualizar el rastro generado por el movimiento del robot.

## Ejecución manual de los nodos de simulación

Si se desea ejecutar únicamente el nodo de movimiento:

```bash
ros2 run g02_prii3_move_turtlebot draw_number
```

Para ejecutar únicamente el nodo del rastro:

```bash
ros2 run g02_prii3_move_turtlebot trail_node
```

## JetBot real

El código destinado al robot real se encuentra en el paquete:

```text
g02_prii3_move_jetbot
```

Las instrucciones de compilación, ejecución y comprobación del JetBot real se encuentran en:

```text
README_JETBOT.md
```

## Grupo

Grupo 02