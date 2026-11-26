# Sprint 3 · Comandos rápidos (Grupo 02)

ROS 2 Humble · TurtleBot3 · Gazebo · Nav2 · ArUcos

> **Preparación:** al abrir **cada terminal**, ejecutar:
>
> ```bash
> cd ~/UNI/PROYECTOS3/g02_prii3_ws
> source /opt/ros/humble/setup.bash
> source install/setup.bash
> ```

## 1. ArUcos + mando Xbox

Abrir **una terminal por comando**, en este orden:

**T1 — Simulación:**
```bash
ros2 launch f1l3_gazebo f1l3_world.launch.py
```

**T2 — Detector:**
```bash
ros2 run g02_prii3_nav_turtlebot aruco_detection
```

**T3 — Mando Xbox:**
```bash
ros2 launch teleop_twist_joy teleop-launch.py joy_dev:=0 config_filepath:=$HOME/UNI/PROYECTOS3/g02_prii3_ws/config/xbox_no_enable.yaml
```

**T4 — Ver detecciones:**
```bash
ros2 topic echo /aruco_info
```

Al mover el robot, deben cambiar los IDs y las coordenadas en píxeles. Si no ve ningún marcador, se publica `[]`.

## 2. Demo autónoma completa

**Cerrar antes la teleoperación con `Ctrl+C`** y detener las instancias anteriores para no duplicar nodos.

**T1 — Todo junto (Gazebo + Nav2 + RViz + ArUcos + autónomo):**
```bash
ros2 launch g02_prii3_nav_turtlebot simulation.launch.py
```

**T2 — Ver marcadores (opcional):**
```bash
ros2 topic echo /aruco_info
```

En **RViz**, pulsar **2D Pose Estimate** para marcar la pose inicial. El robot espera 5 s, va a la entrada `(3.24, 1.71)` y, al detectar el **ID 5**, envía el objetivo `(2.75, 14.42)`.

## 3. Navegación predefinida

**T1 — Mundo:**
```bash
ros2 launch f1l3_gazebo f1l3_world.launch.py
```

**T2 — Nav2 + RViz:**
```bash
export TURTLEBOT3_MODEL=waffle_pi
ros2 launch turtlebot3_navigation2 navigation2.launch.py use_sim_time:=True map:=$HOME/UNI/PROYECTOS3/g02_prii3_ws/mapas/f1l3_mapa.yaml
```

Marcar **2D Pose Estimate** en RViz y después:

**T3 — Enviar objetivo fijo:**
```bash
ros2 run g02_prii3_nav_turtlebot predefined_navigation
```

Destino: **(3.65, -0.37)**.

## 4. Comprobaciones rápidas

```bash
ros2 topic echo /aruco_info     # IDs y centros de ArUcos
ros2 topic list                 # Topics activos
ros2 node list                  # Nodos activos
ros2 action list -t             # Acciones Nav2
```

> **Importante:** no usar el mando Xbox al mismo tiempo que Nav2 navega; ambos pueden enviar órdenes de movimiento. El mando configurado no requiere mantener pulsado un botón de habilitación.

## 5. JetBot real — arranque automático

**T1 — JetBot por SSH (mantener abierto):**

```bash
cd ~/g02_prii3_ws
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash
source install/setup.bash
export ROS_DOMAIN_ID=172 ROS_LOCALHOST_ONLY=0
ros2 launch g02_prii3_nav_jetbot nav.py
```

**T2 — Portátil local (NO SSH):**

```bash
source /opt/ros/humble/setup.bash
export ROS_DOMAIN_ID=172 ROS_LOCALHOST_ONLY=0
rviz2 -d ~/UNI/PROYECTOS3/g02_prii3_ws/config/jetbot_f1l3.rviz
```

En RViz: **2D Pose Estimate**, comprobando que coincide con la posición real.
`nav2_auto_start` activa localización, espera la pose y TF y solicita la
activación de navegación, **sin ejecutar los dos servicios manualmente**.

**T3 — Verificar en otra terminal SSH:**

```bash
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash
source ~/g02_prii3_ws/install/setup.bash
export ROS_DOMAIN_ID=172 ROS_LOCALHOST_ONLY=0
for nodo in map_server amcl planner_server controller_server bt_navigator; do
    timeout 15s ros2 lifecycle get /$nodo
done
ros2 action list -t | grep navigate_to_pose
```

Se esperan nodos `active [3]`. **No enviar `2D Goal Pose` si la localización
no coincide con el robot real, si faltan TF o si no está preparada la parada.**

> **Estado:** navegación guiada probada con el JetBot real; nuevo arranque
> automático compilado en el portátil y pendiente de prueba física.
