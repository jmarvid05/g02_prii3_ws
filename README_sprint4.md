# Sprint 4 — Eurobot y ArUcos

**ROS 2 Humble · Gazebo · Nav2**  
**Sprint Review:** 17/12/2026

## Estado

- **PBI 4.1:** detector `detectar_arucos.py` probado en **Gazebo**. Detecta ArUcos 20–23 y 51–59, publica ID y centro (X, Y) en píxeles en un topic por marcador. Comprobado que el topic del ArUco 51 desaparece al quitar el robot. **Pendiente probar con cámara USB real**.
- **PBI 4.2:** `recorrer_arucos.py` programado para visitar los cuatro ArUcos y volver al centro usando Nav2 y coordenadas fijas. **Pendiente verificar el recorrido completo**.
- **PBI 4.3:** pendiente: navegación guiada por las coordenadas detectadas con la cámara.
- **PBI 4.4:** existe un launch para cámara USB + detector y recorrido opcional; falta integrar y comprobar Nav2 del robot real para la demostración completa.

## Preparación (portátil)

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws
source /opt/ros/humble/setup.bash
colcon build --packages-select eurobot_gazebo --symlink-install
source install/setup.bash
```

En **cada terminal nueva**, ejecutar primero:

```bash
source /opt/ros/humble/setup.bash
source ~/UNI/PROYECTOS3/g02_prii3_ws/install/setup.bash
```

Los ejecutables `detectar_arucos` y `recorrer_arucos` deben estar registrados en `src/eurobot_gazebo/setup.py`.

## Simulación — Gazebo

**Terminal 1 — Mundo:**

```bash
ros2 launch eurobot_gazebo eurobot_world.launch.py
```

**Terminal 2 — Detector de ArUcos:**

```bash
ros2 run eurobot_gazebo detectar_arucos --ros-args -p use_sim_time:=true -r /camera/image_raw:=/overhead_camera/image_raw
```

**Comprobar detección (otra terminal):**

```bash
ros2 topic list | grep aruco
ros2 topic echo /overhead_camera/aruco_20
ros2 topic echo /overhead_camera/aruco_51
```

Si se mueve un marcador, cambian sus coordenadas. Si deja de verse, el nodo elimina su publicador.

**Para probar el recorrido**, iniciar también Nav2 + RViz en otra terminal y después el nodo:

```bash
ros2 launch eurobot_gazebo navigation.launch.py
```

```bash
ros2 run eurobot_gazebo recorrer_arucos --ros-args -p use_sim_time:=true
```

### Destinos del recorrido

| Orden | Destino | X (m) | Y (m) |
|---|---|---:|---:|
| 1 | ArUco 20 | 0.6 | 1.4 |
| 2 | ArUco 21 | 2.4 | 1.4 |
| 3 | ArUco 22 | 0.6 | 0.6 |
| 4 | ArUco 23 | 2.4 | 0.6 |
| 5 | Centro | 1.5 | 1.0 |

El nodo envía cada destino con `/navigate_to_pose` en el frame `map` y espera su resultado antes de enviar el siguiente.

## Tablero real — Cámara USB cenital

Archivo: `src/eurobot_gazebo/launch/sprint4_real.launch.py`.

Si falta el controlador de cámara:

```bash
sudo apt install ros-humble-v4l2-camera
```

**Lanzar cámara USB y detector (sin mover el robot):**

```bash
ros2 launch eurobot_gazebo sprint4_real.launch.py
```

Si la cámara usa otro dispositivo:

```bash
ros2 launch eurobot_gazebo sprint4_real.launch.py dispositivo:=/dev/video2
```

**Comprobar:**

```bash
ros2 topic list | grep aruco
ros2 topic echo /overhead_camera/aruco_20
```

**Recorrido opcional en robot real (NO ejecutar hasta preparar Nav2 real):**

```bash
ros2 launch eurobot_gazebo sprint4_real.launch.py mover_robot:=true
```

> **Importante:** este launch inicia cámara, detector y, opcionalmente, `recorrer_arucos`, pero **no arranca Nav2 ni los controladores del robot real**. Antes de usar `mover_robot:=true` deben funcionar la odometría, las TF y Nav2 real; también hay que verificar que el sistema `map` del tablero coincide con las coordenadas de simulación. Las coordenadas publicadas por el detector están en **píxeles**, no en metros.

**Diferencia entre apartados:** PBI 4.2 navega por objetivos fijos y odometría; PBI 4.3 deberá usar los datos de la cámara para guiar al robot.
