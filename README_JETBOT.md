# JetBot real

Este documento contiene la configuración y los comandos específicos utilizados con el **JetBot real**.

## Datos del robot

```text
IP: 172.16.190.172
Usuario SSH: jetbot
ROS 2 (pruebas de Sprint 3): Humble
ROS_DOMAIN_ID: 172
ROS_LOCALHOST_ONLY: 0
```

## Conexión por SSH

Desde el portátil:

```bash
ssh jetbot@172.16.190.172
```

En las terminales ROS del portátil y del JetBot se utiliza:

```bash
export ROS_DOMAIN_ID=172
export ROS_LOCALHOST_ONLY=0
```

Para hacerlo permanente puede añadirse a `~/.bashrc`.

---

# Actualizar el repositorio

Si el repositorio ya existe en el JetBot:

```bash
cd ~/g02_prii3_ws

git checkout main
git pull

git status
```

Si es necesario clonarlo de nuevo:

```bash
cd ~

git clone -b main https://github.com/jmarvid05/g02_prii3_ws.git

cd ~/g02_prii3_ws

git branch
git status
```

El repositorio debe quedar en:

```text
* main
```

---

# Sprint 2

> Las instrucciones del Sprint 2 conservan algunas referencias históricas a Foxy; para la navegación del Sprint 3 con el JetBot se ha utilizado Humble.


## Arrancar la base del JetBot

En el JetBot:

```bash
source /opt/ros/foxy/setup.bash
source ~/ros2_ws/install/setup.bash

export ROS_DOMAIN_ID=172
export ROS_LOCALHOST_ONLY=0

ros2 launch jetbot_pro_ros2 jetbot.py
```

Esta terminal debe permanecer abierta.

## Preparar el proyecto

```bash
cd ~/g02_prii3_ws

source /opt/ros/foxy/setup.bash
source ~/ros2_ws/install/setup.bash

export ROS_DOMAIN_ID=172
export ROS_LOCALHOST_ONLY=0

colcon build --packages-select g02_prii3_move_jetbot

source install/setup.bash
```

## Movimiento autónomo

```bash
ros2 launch g02_prii3_move_jetbot draw_number_jetbot.launch.py
```

Valores ajustados durante las pruebas con el robot real:

```text
Curva:    linear 0.12   angular -0.55   75 ciclos
Diagonal: linear 0.12   angular  0.00   35 ciclos
Giro:     linear 0.00   angular  0.80   34 ciclos
Base:     linear 0.12   angular  0.00   33 ciclos
```

Servicios:

```bash
ros2 service call /detener_dibujo std_srvs/srv/Trigger "{}"

ros2 service call /reanudar_dibujo std_srvs/srv/Trigger "{}"

ros2 service call /reiniciar_dibujo std_srvs/srv/Trigger "{}"
```

---

## LiDAR

El LiDAR publica en:

```text
/scan
```

Comprobaciones:

```bash
ros2 topic type /scan
ros2 interface show sensor_msgs/msg/LaserScan
ros2 topic echo /scan --once
ros2 topic hz /scan
```

### Filtro

```text
/scan
  ↓
laser_filter
  ↓
/filtered_scan
```

Ejecutar:

```bash
ros2 run g02_prii3_move_jetbot laser_filter
```

Modificar parámetros:

```bash
ros2 param set /laser_filter laser_angle 60.0
ros2 param set /laser_filter distance 2.0
```

---

## Collision avoidance

Flujo:

```text
/filtered_scan
      ↓
collision_avoidance
      ↓
   /cmd_vel
```

Funcionamiento:

```text
obstáculo delante
→ robot detenido

camino libre
→ continúa el movimiento
```

Ejecutar:

```bash
ros2 launch g02_prii3_move_jetbot collision_avoidance_jetbot.launch.py
```

Valores iniciales utilizados:

```text
distance = 0.30 m
front_angle_deg = 30
front_offset_deg = 180
```

---

## Cámara

Topic utilizado:

```text
/camera/image_raw
```

Comprobar:

```bash
ros2 topic hz /camera/image_raw
```

Desde el portátil:

```bash
ros2 run rqt_image_view rqt_image_view
```

Visión del Sprint 2:

```bash
ros2 launch g02_prii3_move_jetbot vision_jetbot.launch.py
```

---

# Sprint 3

## SLAM real

En el JetBot:

```bash
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash

export ROS_DOMAIN_ID=172
export ROS_LOCALHOST_ONLY=0

ros2 launch jetbot_pro_ros2 slam.py
```

El launch del profesor inicia los nodos necesarios para realizar SLAM con el JetBot.

## RViz para SLAM

Desde el portátil:

```bash
source /opt/ros/humble/setup.bash

export ROS_DOMAIN_ID=172
export ROS_LOCALHOST_ONLY=0

ros2 run rviz2 rviz2 -d ~/slam.rviz
```

## Guardar el mapa

Sin cerrar `slam.py`:

```bash
ros2 run nav2_map_server map_saver_cli -f ~/map
```

Esto genera:

```text
map.yaml
map.pgm
```

## Copiar el mapa al portátil

```bash
scp jetbot@172.16.190.172:~/map.yaml ~/
scp jetbot@172.16.190.172:~/map.pgm ~/
```

El mapa real utilizado actualmente en el repositorio se encuentra en:

```text
mapas/jetbot_real/map.yaml
mapas/jetbot_real/map.pgm
```

---

## Arranque automatizado de Nav2 (Sprint 3)

El `nav.py` del **paquete del grupo** arranca la base JetBot y Nav2 con
`autostart=False`. El nodo `nav2_auto_start.py` gestiona los servicios de
localización y navegación en este orden:

```text
nav.py -> activar map_server y AMCL -> esperar 2D Pose Estimate
       -> comprobar TF map -> base_footprint -> activar navegación
```

No es necesario copiar `nav.py` dentro de `jetbot_pro_ros2`, ni colocar
`map.yaml` en `/home/jetbot/`: el mapa se obtiene desde el propio paquete
`g02_prii3_nav_jetbot/maps/map.yaml` (junto con `map.pgm`).

### Terminal 1 — JetBot por SSH

Antes de ejecutar los comandos, actualizar el repositorio y compilar el paquete
si han cambiado sus archivos:

```bash
cd ~/g02_prii3_ws
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash
colcon build --packages-select g02_prii3_nav_jetbot --symlink-install
source ~/g02_prii3_ws/install/setup.bash
export ROS_DOMAIN_ID=172 ROS_LOCALHOST_ONLY=0
ros2 launch g02_prii3_nav_jetbot nav.py
```

Dejar esta terminal abierta. **No lanzar `jetbot.py` por separado**, pues
`nav.py` ya lo incluye. El nodo auxiliar debe activar primero la localización
y pedir que se establezca la pose inicial.

### Terminal 2 — Portátil local (RViz)

```bash
source /opt/ros/humble/setup.bash
export ROS_DOMAIN_ID=172 ROS_LOCALHOST_ONLY=0
rviz2 -d ~/UNI/PROYECTOS3/g02_prii3_ws/config/jetbot_f1l3.rviz
```

En RViz, el mapa `/map` utiliza **Reliable + Transient Local** y el LiDAR
`/scan`, **Best Effort**. Marcar la posición y orientación reales del robot
con **2D Pose Estimate**. El sistema debe esperar a recibir esta pose y disponer
de TF antes de activar el resto de Nav2.

### Comprobar en otra terminal SSH

```bash
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash
source ~/g02_prii3_ws/install/setup.bash
export ROS_DOMAIN_ID=172 ROS_LOCALHOST_ONLY=0
for nodo in map_server amcl planner_server controller_server bt_navigator; do
    echo "=== $nodo ==="
    timeout 15s ros2 lifecycle get /$nodo
done
ros2 action list -t | grep navigate_to_pose
```

Los cinco nodos deben indicar `active [3]` antes de enviar objetivos. Comprobar
además que los datos del LiDAR coinciden con las paredes del entorno real y
que existe una forma de detener el robot. Si alguno falla, revisar el log de
`nav.py` y **no enviar destinos**.

**Estado de las pruebas:** el mapa real F1L3, la localización y la navegación
manual desde RViz se probaron en el JetBot. El nuevo arranque automático
`nav2_auto_start.py` está compilado en el portátil, pero **aún no se ha probado
físicamente en el JetBot**. La cámara CSI y la demostración autónoma con ArUcos
quedan pendientes de validación.

---

## Navegación predefinida

El nodo del proyecto es:

```text
g02_prii3_nav_jetbot predefined_navigation
```

Todavía deben introducirse las coordenadas definitivas obtenidas sobre el mapa real antes de realizar la prueba final.

No ejecutar mientras las coordenadas estén configuradas como:

```text
0.0, 0.0
```

---

## Navegación autónoma con ArUco

El paquete contiene:

```text
aruco_detection
autonomous_navigation
```

y el launch:

```text
autonomous_navigation.launch.py
```

La lógica preparada es:

```text
ir a la entrada
→ esperar a llegar
→ empezar a aceptar ArUcos
→ detectar el ID
→ navegar al destino correspondiente
```

Antes de probarlo con el robot real deben obtenerse las coordenadas reales de:

```text
pose intermedia delante del ArUco
destino final
```

No ejecutar la navegación autónoma mientras estas coordenadas estén a `0.0`.

---

# Comprobaciones ROS 2

Nodos:

```bash
ros2 node list
```

Topics:

```bash
ros2 topic list
```

LiDAR:

```bash
ros2 topic info /scan -v
ros2 topic info /filtered_scan -v
```

Movimiento:

```bash
ros2 topic info /cmd_vel -v
ros2 topic echo /cmd_vel
```

ArUco:

```bash
ros2 topic echo /aruco_info
```

Acción de navegación:

```bash
ros2 action list | grep navigate_to_pose
```

---

# Parar el robot

Para cerrar un nodo:

```text
Ctrl+C
```

Si es necesario enviar una velocidad cero:

```bash
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist \
"{linear: {x: 0.0}, angular: {z: 0.0}}"
```

No deben ejecutarse varios nodos que publiquen movimiento sobre `/cmd_vel` al mismo tiempo.