# Navegación — Simulación y JetBot real

# 1. SIMULACIÓN

## Terminal 1 — Gazebo

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
export TURTLEBOT3_MODEL=burger

ros2 launch f1l3_gazebo f1l3_world.launch.py
```

---

## Terminal 2 — Navigation2 + RViz + mapa guardado

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
2. Marcar posición y orientación
3. Nav2 Goal
4. Marcar destino
```

---

# 2. MANDOS EN SIMULACIÓN

## Comprobar mando conectado

```bash
source /opt/ros/humble/setup.bash

ros2 run joy joy_enumerate_devices
```

Normalmente:

```text
device_id = 0
```

---

## Mando Xbox

```bash
source /opt/ros/humble/setup.bash

ros2 launch teleop_twist_joy teleop-launch.py \
joy_dev:=0 \
config_filepath:=$HOME/UNI/PROYECTOS3/g02_prii3_ws/config/xbox_no_enable.yaml
```

### Archivo Xbox

Crear:

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws
mkdir -p config
vim config/xbox_no_enable.yaml
```

Contenido:

```yaml
teleop_twist_joy_node:
  ros__parameters:
    axis_linear:
      x: 1

    scale_linear:
      x: 0.5

    axis_angular:
      yaw: 0

    scale_angular:
      yaw: 1.0

    require_enable_button: false
```

---

## Mando PlayStation

```bash
source /opt/ros/humble/setup.bash

ros2 launch teleop_twist_joy teleop-launch.py \
joy_dev:=0 \
config_filepath:=$HOME/UNI/PROYECTOS3/g02_prii3_ws/config/playstation_no_enable.yaml
```

### Archivo PlayStation

Crear:

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws
mkdir -p config
vim config/playstation_no_enable.yaml
```

Contenido:

```yaml
teleop_twist_joy_node:
  ros__parameters:
    axis_linear:
      x: 1

    scale_linear:
      x: 0.5

    axis_angular:
      yaw: 0

    scale_angular:
      yaw: 1.0

    require_enable_button: false
```

---

## Comprobar `/cmd_vel`

```bash
ros2 topic echo /cmd_vel
```

---

# 3. CÁMARA EN RVIZ

Buscar topics:

```bash
ros2 topic list | grep -E 'camera|image'
```

En RViz añadir:

```text
Map        → /map
LaserScan  → /scan
TF
RobotModel
Image      → topic de cámara
```

---

# 4. JETBOT REAL

## Terminal 1 — Conectarse al JetBot

```bash
ssh jetbot@172.16.190.172
```

Arrancar robot:

```bash
export ROS_DOMAIN_ID=172
export ROS_LOCALHOST_ONLY=0

ros2 launch jetbot_pro_ros2 jetbot.py
```

Dejar abierta.

---

## Terminal 2 — Portátil

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws
source /opt/ros/humble/setup.bash
source install/setup.bash

export ROS_DOMAIN_ID=172
export ROS_LOCALHOST_ONLY=0
```

Comprobar comunicación:

```bash
ros2 topic list
```

LiDAR:

```bash
ros2 topic hz /scan
```

Odometría:

```bash
ros2 topic echo /odom --once
```

TF:

```bash
ros2 topic list | grep tf
```

---

# 5. MANDO XBOX CON JETBOT REAL

Mando conectado al portátil:

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

# 6. MANDO PLAYSTATION CON JETBOT REAL

Mando conectado al portátil:

```bash
source /opt/ros/humble/setup.bash

export ROS_DOMAIN_ID=172
export ROS_LOCALHOST_ONLY=0

ros2 launch teleop_twist_joy teleop-launch.py \
joy_dev:=0 \
config_filepath:=$HOME/UNI/PROYECTOS3/g02_prii3_ws/config/playstation_no_enable.yaml
```

Comprobar:

```bash
ros2 topic echo /cmd_vel
```

---

# 7. RViz CON JETBOT

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

# 8. NAVEGACIÓN AUTOMÁTICA JETBOT

Necesitamos:

```text
Map Server
AMCL
Nav2
```

En RViz:

```text
2D Pose Estimate
→ posición inicial

Nav2 Goal
→ destino
```

## PENDIENTE

Crear y probar el launch específico de Navigation2 para el JetBot real.

No usar directamente:

```bash
ros2 launch turtlebot3_navigation2 navigation2.launch.py
```

porque esa configuración es específica del TurtleBot3.

El JetBot deberá usar:

```text
/scan
/odom
/tf
/tf_static
/cmd_vel
```

y sus frames reales.

---

# 9. ROS DOMAIN = 172 PERMANENTE

Tanto el portátil como el JetBot deben usar:

```text
ROS_DOMAIN_ID=172
```

## Portátil

```bash
vim ~/.bashrc
```

Añadir al final:

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

## JetBot

Entrar:

```bash
ssh jetbot@172.16.190.172
```

Editar:

```bash
vim ~/.bashrc
```

Añadir:

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

# RESUMEN

## Simulación

```text
Terminal 1 → Gazebo
Terminal 2 → Navigation2 + RViz
Terminal 3 → Xbox o PlayStation
```

## Robot real

```text
JetBot     → jetbot.py
Portátil   → ROS_DOMAIN_ID=172
Portátil   → Xbox o PlayStation
Portátil   → RViz / Navigation2
```