# Mapeo de la clase con JetBot

## 1. JetBot — arrancar robot

Desde el portátil:

```bash
ssh jetbot@172.16.190.172
```

Dentro del JetBot:

```bash
export ROS_DOMAIN_ID=172
export ROS_LOCALHOST_ONLY=0

ros2 launch jetbot_pro_ros2 jetbot.py
```

Dejar esta terminal abierta.

---

## 2. JetBot — mando PlayStation

Abrir otra terminal:

```bash
ssh jetbot@172.16.190.172
```

Dentro del JetBot:

```bash
export ROS_DOMAIN_ID=172
export ROS_LOCALHOST_ONLY=0

ros2 launch teleop_twist_joy teleop-launch.py \
joy_config:=ps3 \
joy_dev:=0
```

Quitar botón de habilitación:

```bash
ros2 param set /teleop_twist_joy_node require_enable_button false
```

Comprobar mando:

```bash
ros2 topic echo /joy
```

Comprobar movimiento enviado:

```bash
ros2 topic echo /cmd_vel
```

---

# 3. Portátil — preparar ROS

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws

source /opt/ros/humble/setup.bash
source install/setup.bash

export ROS_DOMAIN_ID=172
export ROS_LOCALHOST_ONLY=0
```

---

## 4. Comprobar sensores

### LiDAR

```bash
ros2 topic hz /scan
```

### Odometría

```bash
ros2 topic echo /odom --once
```

### TF

```bash
ros2 topic list | grep tf
```

Probar transformación:

```bash
ros2 run tf2_ros tf2_echo odom base_link
```

Antes de mapear deben funcionar:

```text
/scan
/odom
/tf
/tf_static
/cmd_vel
```

---

# 5. Portátil — iniciar SLAM

Abrir otra terminal:

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws

source /opt/ros/humble/setup.bash
source install/setup.bash

export ROS_DOMAIN_ID=172
export ROS_LOCALHOST_ONLY=0

ros2 launch slam_toolbox online_async_launch.py
```

Dejar abierta.

---

# 6. Portátil — abrir RViz

Otra terminal:

```bash
source /opt/ros/humble/setup.bash

export ROS_DOMAIN_ID=172
export ROS_LOCALHOST_ONLY=0

rviz2
```

En RViz:

```text
Fixed Frame → map
```

Añadir:

```text
Map       → /map
LaserScan → /scan
TF
RobotModel
```

---

# 7. Mapear la clase

Mover el JetBot con el mando PlayStation.

Recorrer:

```text
- paredes
- esquinas
- pasillos
- zonas abiertas
- volver por zonas ya recorridas
```

Mientras se mueve el robot, comprobar que el mapa se va creando en RViz.

---

# 8. Guardar el mapa

En el portátil:

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws

mkdir -p mapas
```

Guardar:

```bash
ros2 run nav2_map_server map_saver_cli \
-f ~/UNI/PROYECTOS3/g02_prii3_ws/mapas/clase_jetbot
```

Se crearán:

```text
mapas/clase_jetbot.pgm
mapas/clase_jetbot.yaml
```

Comprobar:

```bash
ls -l mapas/
```

---

# 9. ROS_DOMAIN_ID permanente

Tanto en el portátil como en el JetBot:

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

# Resumen

```text
JETBOT
Terminal 1 → jetbot.py
Terminal 2 → mando PlayStation

PORTÁTIL
Terminal 3 → comprobar sensores
Terminal 4 → slam_toolbox
Terminal 5 → RViz

FINAL
→ map_saver_cli
→ clase_jetbot.pgm
→ clase_jetbot.yaml
```

## Si SLAM da error con `base_footprint`

Comprobar primero:

```bash
ros2 run tf2_ros tf2_echo odom base_link
```

Si el JetBot usa `base_link` y SLAM busca `base_footprint`, habrá que usar una configuración específica de `slam_toolbox` para el JetBot.