# Sprint 2 - Movimiento, LiDAR y vision

## Objetivo del Sprint

Para el Grupo 02:

1. Separar codigo de simulacion y robot real.
2. Dibujar autonomamente el numero **2**.
3. Detener el robot al detectar un obstaculo delante y reanudar cuando desaparece.
4. Calibrar la camara y detectar ArUcos.
5. Mantener GitHub y los README actualizados.

El PBI 2.2 de esta version se centra en `collision_avoidance`.

---

# 1. Publisher y Subscriber

Es la comunicacion principal de ROS 2 que usamos:

```text
PUBLISHER ---- topic ----> SUBSCRIBER
   envia                    recibe
```

En nuestro proyecto:

```text
draw_number         -- /cmd_vel -------> controlador del robot
LiDAR               -- /scan ----------> laser_filter
laser_filter        -- /filtered_scan --> collision_avoidance
collision_avoidance -- /cmd_vel -------> controlador del robot
odometria           -- /odom ----------> trail_node
trail_node          -- /robot_path -----> RViz
camara              -- /camera/image_raw -> vision
```

Un mismo nodo puede ser subscriber y publisher. Por ejemplo `collision_avoidance` **recibe** el LiDAR y **publica** velocidades.

Los **servicios** son diferentes: sirven para hacer una peticion puntual y recibir una respuesta.

---

# 2. PBI 2.0 - Paquetes

```text
g02_prii3_move_turtlebot -> simulacion TurtleBot3 / ROS 2 Humble
g02_prii3_move_jetbot    -> JetBot real / ROS 2 Foxy
```

---

# 3. PBI 2.1 - Movimiento autonomo

## Como funciona

`draw_number` publica `geometry_msgs/msg/Twist` en `/cmd_vel`.

```text
tramo 1 -> curva
tramo 2 -> diagonal
tramo 3 -> giro
tramo 4 -> base
```

Cada tramo guarda:

```text
(linear.x, angular.z, numero de ciclos)
```

El timer se ejecuta cada `0.1 s`.

## Servicios

```text
/detener_dibujo   -> pausa y publica velocidad cero
/reanudar_dibujo  -> continua desde el mismo punto
/reiniciar_dibujo -> vuelve al primer tramo
```

## Rastro en RViz

`trail_node` es subscriber y publisher:

```text
/odom -> trail_node -> /robot_path -> RViz
```

## Comandos - simulacion del dibujo

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws
source /opt/ros/humble/setup.bash
colcon build --packages-select g02_prii3_move_turtlebot
source install/setup.bash
ros2 launch g02_prii3_move_turtlebot draw_number.launch.py
```

En otra terminal:

```bash
source /opt/ros/humble/setup.bash
source ~/UNI/PROYECTOS3/g02_prii3_ws/install/setup.bash
ros2 service call /detener_dibujo std_srvs/srv/Trigger "{}"
ros2 service call /reanudar_dibujo std_srvs/srv/Trigger "{}"
ros2 service call /reiniciar_dibujo std_srvs/srv/Trigger "{}"
```

---

# 4. PBI 2.2 - Collision avoidance

## Datos del LiDAR

El LiDAR publica:

```text
Topic: /scan
Tipo:  sensor_msgs/msg/LaserScan
```

Campos importantes:

- `angle_min`, `angle_max`: limites del escaneo.
- `angle_increment`: separacion angular entre medidas.
- `range_min`, `range_max`: distancia valida del sensor.
- `ranges[]`: distancias medidas.

### Comandos para comprobar el LiDAR

```bash
ros2 topic type /scan
ros2 interface show sensor_msgs/msg/LaserScan
ros2 topic echo /scan --once
ros2 topic hz /scan
```

## laser_filter.py

Es un ejemplo muy claro de publisher/subscriber:

```text
LiDAR -> /scan -> [SUBSCRIBER laser_filter PUBLISHER] -> /filtered_scan
```

Filtra por:

- `laser_angle`: angulo que queremos conservar.
- `distance`: distancia maxima que queremos conservar.

Cambiar parametros mientras funciona:

```bash
ros2 param set /laser_filter laser_angle 60.0
ros2 param set /laser_filter distance 2.0
```

Ver el resultado:

```bash
ros2 topic echo /filtered_scan --once
```

## collision_avoidance.py

Tambien es subscriber y publisher:

```text
/filtered_scan -> collision_avoidance -> /cmd_vel
       SUBSCRIBER                 PUBLISHER
```

Algoritmo:

```text
1. Recibe LaserScan.
2. Mira el sector frontal.
3. Busca la distancia valida mas pequena.
4. Si distancia < distancia de seguridad:
      publica Twist = 0
      NO aumenta el contador del dibujo
5. Cuando desaparece el obstaculo:
      vuelve a publicar la trayectoria
      continua desde el mismo punto
```

Valores iniciales:

```text
Simulacion: distancia = 0.45 m, frente = 30 grados
JetBot:     distancia = 0.30 m, frente = 30 grados
JetBot LiDAR: front_offset_deg = 180
```

## Comandos - collision avoidance en simulacion

El launch abre Gazebo, el filtro LiDAR, `collision_avoidance`, el rastro y RViz:

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws
source /opt/ros/humble/setup.bash
colcon build --packages-select g02_prii3_move_turtlebot
source install/setup.bash
ros2 launch g02_prii3_move_turtlebot collision_avoidance.launch.py
```

Para la demostracion, coloca un objeto delante del TurtleBot3 en Gazebo:

```text
camino libre -> dibuja el 2
objeto delante -> se para
retirar objeto -> continua desde el mismo punto
```

### Comprobar publishers y subscribers

```bash
ros2 node info /collision_avoidance
ros2 node info /laser_filter
ros2 topic info /scan -v
ros2 topic info /filtered_scan -v
ros2 topic info /cmd_vel -v
```

---

# 5. JetBot real

## Datos del robot

```text
JetBot 02 / jetbot03M
IP: 172.16.190.184
Usuario: jetbot
ROS 2: Foxy
ROS_DOMAIN_ID: 2
```

Conectar:

```bash
ssh jetbot@172.16.190.184
```

## Terminal 1 - base del JetBot

```bash
source /opt/ros/foxy/setup.bash
source ~/jetbot_ws/install/setup.bash
export ROS_DOMAIN_ID=2
export ROS_LOCALHOST_ONLY=0
ros2 launch jetbot_pro_ros2 jetbot.py
```

## Terminal 2 - compilar proyecto

```bash
cd ~/g02_prii3_ws
source /opt/ros/foxy/setup.bash
source ~/jetbot_ws/install/setup.bash
colcon build --packages-select g02_prii3_move_jetbot
source install/setup.bash
export ROS_DOMAIN_ID=2
export ROS_LOCALHOST_ONLY=0
```

## Dibujar el 2

```bash
ros2 launch g02_prii3_move_jetbot draw_number_jetbot.launch.py
```

## Collision avoidance

El launch ejecuta:

```text
/scan -> laser_filter -> /filtered_scan -> collision_avoidance -> /cmd_vel
```

```bash
ros2 launch g02_prii3_move_jetbot collision_avoidance_jetbot.launch.py
```

> Ejecutar un solo nodo de movimiento a la vez. No ejecutar `draw_number` y `collision_avoidance` simultaneamente porque ambos publican en `/cmd_vel`.

---

# 6. PBI 2.3 - Calibracion y ArUco

Esta parte ya se presento por separado, pero se conserva en el repositorio.

Flujo:

```text
comprobar_tablero.py
        -> calibrar_filtrado.py
        -> CameraModel.yml
        -> rectificar_imagen.py
        -> aruco_pose.py
```

Los nodos ROS de vision se suscriben a:

```text
/camera/image_raw
```

## Comandos - prueba con imagenes guardadas

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws
python3 calibracion/comprobar_tablero.py
python3 calibracion/calibrar_filtrado.py
python3 calibracion/rectificar_imagen.py
python3 calibracion/aruco_pose.py
```

## Comandos - simular stream de camara ROS

Terminal 1:

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
python3 calibracion/publicar_imagen_ros.py
```

Terminal 2:

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 launch g02_prii3_move_jetbot vision_jetbot.launch.py
```

---

# 7. PBI 2.4 - GitHub

Comprobar antes de subir:

```bash
git status
git diff
```

Subir cambios:

```bash
git add -A
git commit -m "Finaliza Sprint 2"
git pull --rebase origin main
git push origin main
```

Comprobacion final:

```bash
git status
```

---

# 8. Comandos rapidos para la defensa

```bash
# Ver nodos, topics y servicios
ros2 node list
ros2 topic list
ros2 service list

# Saber quien publica y quien se suscribe
ros2 topic info /cmd_vel -v
ros2 topic info /scan -v
ros2 topic info /filtered_scan -v

# Ver informacion de un nodo
ros2 node info /collision_avoidance
ros2 node info /laser_filter

# Ver una lectura LiDAR
ros2 topic echo /scan --once
```
