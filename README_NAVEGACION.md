# Navegación — Simulación y JetBot real

## 1. SIMULACIÓN

### Terminal 1 — Gazebo

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
export TURTLEBOT3_MODEL=burger

ros2 launch f1l3_gazebo f1l3_world.launch.py
```

---

### Terminal 2 — Navigation2 + RViz + mapa guardado

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
export TURTLEBOT3_MODEL=burger

ros2 launch turtlebot3_navigation2 navigation2.launch.py \
use_sim_time:=True \
map:=$HOME/UNI/PROYECTOS3/g02_prii3_ws/mapas/f1l3_mapa.yaml
```

En RViz:

```text
1. 2D Pose Estimate
2. Marcar posición y orientación del robot
3. Nav2 Goal
4. Marcar destino
```

---

### Terminal 3 — Mando Xbox

```bash
source /opt/ros/humble/setup.bash

ros2 launch teleop_twist_joy teleop-launch.py \
joy_dev:=0 \
config_filepath:=$HOME/UNI/PROYECTOS3/g02_prii3_ws/config/xbox_no_enable.yaml
```

Comprobar:

```bash
ros2 topic echo /cmd_vel
```

---

## Cámara en RViz

Ver topics de cámara:

```bash
ros2 topic list | grep -E 'camera|image'
```

En RViz:

```text
Add
→ Image
→ Topic de la cámara
```

También se pueden añadir:

```text
Map        → /map
LaserScan  → /scan
TF
RobotModel
Image      → topic de cámara
```

---

# 2. JETBOT REAL

## Terminal 1 — Conectarse al JetBot

```bash
ssh jetbot@172.16.190.172
```

Arrancar el robot:

```bash
export ROS_DOMAIN_ID=172
export ROS_LOCALHOST_ONLY=0

ros2 launch jetbot_pro_ros2 jetbot.py
```

Dejar esta terminal abierta.

---

## Terminal 2 — Portátil

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws
source /opt/ros/humble/setup.bash
source install/setup.bash

export ROS_DOMAIN_ID=172
export ROS_LOCALHOST_ONLY=0
```

Comprobar dominio:

```bash
echo $ROS_DOMAIN_ID
```

Debe salir:

```text
172
```

Comprobar conexión:

```bash
ros2 topic list
```

Comprobar LiDAR:

```bash
ros2 topic hz /scan
```

Comprobar odometría:

```bash
ros2 topic echo /odom --once
```

Comprobar TF:

```bash
ros2 topic list | grep tf
```

---

## Terminal 3 — Mando Xbox desde el portátil

```bash
source /opt/ros/humble/setup.bash

export ROS_DOMAIN_ID=172
export ROS_LOCALHOST_ONLY=0

ros2 launch teleop_twist_joy teleop-launch.py \
joy_dev:=0 \
config_filepath:=$HOME/UNI/PROYECTOS3/g02_prii3_ws/config/xbox_no_enable.yaml
```

Comprobar:

```bash
ros2 topic echo /cmd_vel
```

---

## RViz con JetBot

```bash
source /opt/ros/humble/setup.bash

export ROS_DOMAIN_ID=172
export ROS_LOCALHOST_ONLY=0

rviz2
```

Añadir:

```text
TF
LaserScan → /scan
RobotModel
Image → topic de cámara
```

Buscar cámara:

```bash
ros2 topic list | grep -E 'camera|image'
```

---

# Navegación automática JetBot

Para navegar sobre un mapa guardado necesitamos arrancar:

```text
Map Server
AMCL
Nav2
```

Después en RViz:

```text
2D Pose Estimate
→ posición inicial

Nav2 Goal
→ destino
```

## PENDIENTE

Crear/probar el launch específico de Navigation2 para el JetBot real.

No usar directamente:

```bash
ros2 launch turtlebot3_navigation2 navigation2.launch.py
```

porque esa configuración es para TurtleBot3.

La configuración del JetBot deberá utilizar:

```text
/scan
/odom
/tf
/tf_static
/cmd_vel
```

y los frames reales del JetBot.

---

# ROS DOMAIN

Para trabajar con el JetBot real:

```bash
export ROS_DOMAIN_ID=172
export ROS_LOCALHOST_ONLY=0
```

Tanto el portátil como el JetBot deben usar:

```text
ROS_DOMAIN_ID=172
```

---

# Dejar ROS_DOMAIN_ID=172 permanente

Así no hace falta escribir los `export` cada vez que se abre una terminal.

## Portátil

Abrir:

```bash
vim ~/.bashrc
```

Al final del archivo añadir:

```bash
export ROS_DOMAIN_ID=172
export ROS_LOCALHOST_ONLY=0
```

Guardar en Vim:

```text
Esc
:wq
Enter
```

Aplicar los cambios:

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

## JetBot

Entrar por SSH:

```bash
ssh jetbot@172.16.190.172
```

Abrir:

```bash
vim ~/.bashrc
```

Al final añadir:

```bash
export ROS_DOMAIN_ID=172
export ROS_LOCALHOST_ONLY=0
```

Guardar:

```text
Esc
:wq
Enter
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

## Resultado

Después de hacerlo en los dos equipos:

```bash
echo $ROS_DOMAIN_ID
```

debe mostrar:

```text
172
```

tanto en el portátil como en el JetBot.
