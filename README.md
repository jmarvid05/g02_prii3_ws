# g02_prii3_ws - Grupo 02

Workspace ROS 2 de **Proyecto RII 3: Robots Inteligentes**.

## Documentacion

- `README_sprint1.md`: Turtlesim y servicios.
- `README_sprint2.md`: TurtleBot3, JetBot, LiDAR, collision avoidance y vision.
- `README_JETBOT.md`: comandos especificos del robot real.
- `CODIGOS_RESUMEN.md`: para que sirve cada script.
- `DEMO_SPRINT2.md`: chuleta corta para la Sprint Review.

## Idea ROS 2 que usamos en todo el proyecto

```text
PUBLISHER ---- topic ----> SUBSCRIBER
   envia                    recibe
```

Ejemplos del proyecto:

```text
draw_number        -- /cmd_vel ------> controlador del robot
LiDAR              -- /scan ---------> laser_filter
laser_filter       -- /filtered_scan -> collision_avoidance
collision_avoidance -- /cmd_vel ------> controlador del robot
odometria          -- /odom ---------> trail_node
trail_node         -- /robot_path ---> RViz
camara             -- /camera/image_raw -> nodos de vision
```

Los servicios `/detener_dibujo`, `/reanudar_dibujo` y `/reiniciar_dibujo` son distintos a los topics: son peticiones puntuales con respuesta.

## JetBot del grupo

```text
JetBot 02 / jetbot03M
IP: 172.16.190.184
SSH: ssh jetbot@172.16.190.184
ROS_DOMAIN_ID: 2
```

## Uso de Inteligencia Artificial

Se ha utilizado IA como apoyo para organizar, revisar y documentar parte del codigo. Todo el codigo final se ha adaptado y probado dentro del proyecto.
