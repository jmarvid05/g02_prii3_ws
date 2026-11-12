# README — Sprint 3 Robots Inteligentes

Guía corta de los comandos usados en **simulación** y con el **JetBot real**.

---

# 1. ROS DOMAIN — JetBot real

En el portátil y en el JetBot:

```bash
export ROS_DOMAIN_ID=172
export ROS_LOCALHOST_ONLY=0
```

Para dejarlo permanente:

```bash
vim ~/.bashrc
```

Añadir al final:

```bash
export ROS_DOMAIN_ID=172
export ROS_LOCALHOST_ONLY=0
```

Aplicar:

```bash
source ~/.bashrc
```

Comprobar:

```bash
echo $ROS_DOMAIN_ID
```

Debe salir:

```text
172
```

---

# 2. SIMULACIÓN — F1L3

## Terminal 1 — Gazebo

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
export TURTLEBOT3_MODEL=burger

ros2 launch f1l3_gazebo f1l3_world.launch.py
```

## Terminal 2 — SLAM

```bash
source /opt/ros/humble/setup.bash
export TURTLEBOT3_MODEL=burger

ros2 launch turtlebot3_cartographer cartographer.launch.py use_sim_time:=True
```

## Terminal 3 — Teleop

```bash
source /opt/ros/humble/setup.bash
export TURTLEBOT3_MODEL=burger

ros2 run turtlebot3_teleop teleop_keyboard
```

## Guardar mapa

```bash
ros2 run nav2_map_server map_saver_cli -f ~/UNI/PROYECTOS3/g02_prii3_ws/mapas/f1l3_mapa
```

## Navegación

```bash
ros2 launch turtlebot3_navigation2 navigation2.launch.py use_sim_time:=True map:=$HOME/UNI/PROYECTOS3/g02_prii3_ws/mapas/f1l3_mapa.yaml
```

En RViz:

```text
2D Pose Estimate
→ marcar posición inicial

Nav2 Goal
→ marcar destino
```

---

# 3. JETBOT REAL — SLAM

El material del profesor usa directamente:

```bash
ros2 launch jetbot_pro_ros2 slam.py
```

Este launch arranca los nodos necesarios de:

```text
- control del JetBot
- joystick
- navegación
- SLAM
```

## Terminal 1 — JetBot

Entrar:

```bash
ssh jetbot@172.16.190.172
```

Después:

```bash
export ROS_DOMAIN_ID=172
export ROS_LOCALHOST_ONLY=0

ros2 launch jetbot_pro_ros2 slam.py
```

Dejar esta terminal abierta.

## Terminal 2 — Portátil / RViz

```bash
source /opt/ros/humble/setup.bash
export ROS_DOMAIN_ID=172
export ROS_LOCALHOST_ONLY=0

ros2 run rviz2 rviz2 -d ~/slam.rviz
```

Mover el JetBot con el mando PlayStation conectado físicamente al robot.

---

# 4. GUARDAR MAPA REAL

**Sin cerrar `slam.py`**, abrir otra terminal en el JetBot:

```bash
ros2 run nav2_map_server map_saver_cli -f ~/map
```

Se generan:

```text
~/map.pgm
~/map.yaml
```

## Copiar mapa al portátil

Desde el portátil:

```bash
scp jetbot@172.16.190.172:~/map* ~/
```

Opcionalmente, moverlo al repositorio:

```bash
mv ~/map.pgm ~/UNI/PROYECTOS3/g02_prii3_ws/mapas/
mv ~/map.yaml ~/UNI/PROYECTOS3/g02_prii3_ws/mapas/
```

---

# 5. JETBOT REAL — NAVEGACIÓN

El material del profesor usa:

```bash
ros2 launch jetbot_pro_ros2 nav.py
```

## Terminal 1 — JetBot

```bash
ssh jetbot@172.16.190.172
```

Después:

```bash
export ROS_DOMAIN_ID=172
export ROS_LOCALHOST_ONLY=0

ros2 launch jetbot_pro_ros2 nav.py
```

## Terminal 2 — Portátil / RViz Navigation2

Opción del profesor:

```bash
source /opt/ros/humble/setup.bash
export ROS_DOMAIN_ID=172
export ROS_LOCALHOST_ONLY=0

ros2 run rviz2 rviz2 -d $(ros2 pkg prefix nav2_bringup)/share/nav2_bringup/rviz/nav2_default_view.rviz
```

Si tenemos el fichero `nav.rviz`:

```bash
ros2 run rviz2 rviz2 -d ~/nav.rviz
```

En RViz:

```text
Nav2 Goal
→ marcar destino
→ indicar orientación final
```

> El material proporcionado no muestra en estas instrucciones un parámetro para pasar directamente `map.yaml` a `nav.py`, así que no se añade ningún comando inventado para ello.

---

# 6. MANDO PLAYSTATION — JETBOT

El mando va conectado físicamente al JetBot.

Comprobar:

```bash
ls /dev/input/js*
```

Lanzarlo manualmente si hace falta:

```bash
ros2 launch teleop_twist_joy teleop-launch.py joy_config:=ps3 joy_dev:=0
```

Quitar botón de habilitación:

```bash
ros2 param set /teleop_twist_joy_node require_enable_button false
```

Comprobar:

```bash
ros2 topic echo /joy
ros2 topic echo /cmd_vel
```

---

# 7. CÁMARA EN RViz

Buscar topics:

```bash
ros2 topic list | grep -E 'camera|image'
```

En RViz:

```text
Add
→ Image
→ seleccionar topic de imagen
```

---

# 8. PAQUETES DEL SPRINT 3

Crear:

```text
g02_prii3_nav_jetbot
g02_prii3_nav_turtlebot
```

---

# 9. PBIs DEL SPRINT 3

## PBI 3.1 — ArUco

```text
- Detectar ArUcos DICT_4X4_100
- Publicar ID + coordenadas en un topic propio
- Comprobar con ros2 topic echo
```

## PBI 3.2 — SLAM + navegación guiada

```text
- Real
- Simulación
- Navegación guiada desde RViz
```

## PBI 3.3 — Navegación predefinida

Nodo:

```text
predefined_navigation
```

Debe llevar al robot:

```text
pose inicial predefinida
→ pose final predefinida
```

En real y simulación.

## PBI 3.4 — Navegación autónoma

Nodo:

```text
autonomous_navigation
```

Secuencia:

```text
pasillo
→ puerta del laboratorio
→ detectar ArUco
→ elegir destino según ID
→ navegar hasta la pose final
```

Tres ArUcos distintos:

```text
ArUco 1 → pose final 1
ArUco 2 → pose final 2
ArUco 3 → pose final 3
```

## PBI 3.5 — Git

```text
- Workspace final en main
- README actualizado
```

## PBI 3.6 — Demo

```text
Las demostraciones deben poder ejecutarse desde un único launch.
```

---

# 10. COMANDOS DE COMPROBACIÓN

```bash
ros2 node list
ros2 topic list
ros2 topic hz /scan
ros2 topic echo /odom --once
ros2 topic echo /cmd_vel
ros2 topic echo /map --once
ros2 topic list | grep tf
```

---

# RESUMEN RÁPIDO

## Simulación

```text
f1l3_gazebo
→ Cartographer
→ guardar mapa
→ Navigation2
→ Nav2 Goal
```

## Robot real — mapear

```text
JETBOT:
ros2 launch jetbot_pro_ros2 slam.py

PC:
ros2 run rviz2 rviz2 -d ~/slam.rviz

JETBOT:
ros2 run nav2_map_server map_saver_cli -f ~/map
```

## Robot real — navegar

```text
JETBOT:
ros2 launch jetbot_pro_ros2 nav.py

PC:
ros2 run rviz2 rviz2 -d ~/nav.rviz

RViz:
Nav2 Goal
```
