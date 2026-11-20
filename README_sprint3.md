# Sprint 3 - Navegación y ArUcos

## Objetivo

En el Sprint 3 se trabaja con navegación autónoma en simulación y con el JetBot real.

Los principales apartados son:

- Creación de paquetes de navegación.
- Detección de marcadores ArUco.
- SLAM y navegación con Navigation2.
- Navegación hacia una posición predefinida.
- Navegación autónoma según el ArUco detectado.
- Preparación de launches para las demostraciones.

---

# PBI 3.0 - Paquetes de navegación

Los paquetes creados son:

```text
g02_prii3_nav_turtlebot
g02_prii3_nav_jetbot
```

El primero se utiliza para simulación con TurtleBot3 y el segundo para el JetBot real.

## Compilar

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws

source /opt/ros/humble/setup.bash

colcon build \
--packages-select \
g02_prii3_nav_turtlebot \
g02_prii3_nav_jetbot \
--symlink-install

source install/setup.bash
```

Comprobar los ejecutables:

```bash
ros2 pkg executables g02_prii3_nav_turtlebot
ros2 pkg executables g02_prii3_nav_jetbot
```

---

# PBI 3.1 - Detección de ArUcos

Para el Sprint 3 se utiliza:

```text
DICT_4X4_100
```

El nodo publica todos los ArUcos detectados en:

```text
/aruco_info
```

utilizando mensajes:

```text
std_msgs/msg/String
```

Formato de ejemplo:

```text
ID: 5, X: 248, Y: 236
```

Si se detectan varios:

```text
ID: 5, X: ... , Y: ... | ID: 6, X: ... , Y: ...
```

Los valores `X` e `Y` representan el centro del marcador en la imagen.

---

## Prueba con cámara del portátil

Comprobar las cámaras disponibles:

```bash
v4l2-ctl --list-devices
ls -l /dev/video*
```

En las pruebas se utilizó:

```text
/dev/video1
```

### Terminal 1 - Cámara

```bash
source /opt/ros/humble/setup.bash

ros2 run v4l2_camera v4l2_camera_node \
--ros-args \
-p video_device:=/dev/video1 \
-r image_raw:=/camera/image_raw
```

### Terminal 2 - Detector

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws

source /opt/ros/humble/setup.bash
source install/setup.bash

ros2 run g02_prii3_nav_jetbot aruco_detection
```

### Terminal 3 - Comprobar detección

```bash
source /opt/ros/humble/setup.bash

ros2 topic echo /aruco_info
```

Se comprobó la detección del ArUco ID 37 y que las coordenadas cambian al mover el marcador.

Cuando no se detecta ningún marcador:

```text
[]
```

---

## ArUcos en simulación

Para disponer de cámara en TurtleBot3 se utiliza:

```bash
export TURTLEBOT3_MODEL=waffle_pi
```

### Preparar modelos ArUco de Gazebo

Los modelos están incluidos en:

```text
src/f1l3_gazebo/src/f1l3_gazebo/arucos_gazebo.zip
```

Si todavía no están instalados:

```bash
mkdir -p ~/.gazebo/models

unzip -o \
~/UNI/PROYECTOS3/g02_prii3_ws/src/f1l3_gazebo/src/f1l3_gazebo/arucos_gazebo.zip \
-d ~/.gazebo/models
```

Los marcadores utilizados en el escenario son:

```text
5
6
17
```

Para generar sus texturas con `DICT_4X4_100`:

```bash
python3 - <<'PY'
import cv2
import os

aruco = cv2.aruco
dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_100)

for marker_id in [5, 6, 17]:
    marker = aruco.drawMarker(dictionary, marker_id, 300)

    path = os.path.expanduser(
        f'~/.gazebo/models/aruco_{marker_id}/materials/textures/aruco_{marker_id}.png'
    )

    cv2.imwrite(path, marker)
    print(f'Generado: {path}')
PY
```

---

## Probar detección en simulación

### Terminal 1 - Gazebo

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws

source /opt/ros/humble/setup.bash
source install/setup.bash

export TURTLEBOT3_MODEL=waffle_pi

ros2 launch f1l3_gazebo f1l3_world.launch.py
```

### Terminal 2 - Detector

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws

source /opt/ros/humble/setup.bash
source install/setup.bash

ros2 run g02_prii3_nav_turtlebot aruco_detection
```

### Terminal 3 - Comprobar

```bash
source /opt/ros/humble/setup.bash

ros2 topic echo /aruco_info
```

Se han detectado correctamente en simulación:

```text
ID 5
ID 6
ID 17
```

---

# PBI 3.2 - SLAM y navegación

## Simulación - Crear mapa

### Terminal 1 - Gazebo

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws

source /opt/ros/humble/setup.bash
source install/setup.bash

export TURTLEBOT3_MODEL=waffle_pi

ros2 launch f1l3_gazebo f1l3_world.launch.py
```

### Terminal 2 - SLAM

```bash
source /opt/ros/humble/setup.bash

export TURTLEBOT3_MODEL=waffle_pi

ros2 launch turtlebot3_cartographer cartographer.launch.py \
use_sim_time:=True
```

### Mover el robot

Puede utilizarse teleoperación para recorrer el escenario.

Con mando Xbox:

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws

source /opt/ros/humble/setup.bash
source install/setup.bash

ros2 launch teleop_twist_joy teleop-launch.py \
joy_dev:=0 \
config_filepath:=$HOME/UNI/PROYECTOS3/g02_prii3_ws/config/xbox_no_enable.yaml
```

### Guardar mapa

```bash
ros2 run nav2_map_server map_saver_cli \
-f ~/UNI/PROYECTOS3/g02_prii3_ws/mapas/f1l3_mapa
```

Se generan:

```text
mapas/f1l3_mapa.yaml
mapas/f1l3_mapa.pgm
```

---

## Simulación - Navegación guiada

### Terminal 1 - Gazebo

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws

source /opt/ros/humble/setup.bash
source install/setup.bash

export TURTLEBOT3_MODEL=waffle_pi

ros2 launch f1l3_gazebo f1l3_world.launch.py
```

### Terminal 2 - Navigation2

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws

source /opt/ros/humble/setup.bash
source install/setup.bash

export TURTLEBOT3_MODEL=waffle_pi

ros2 launch turtlebot3_navigation2 navigation2.launch.py \
use_sim_time:=True \
map:=$HOME/UNI/PROYECTOS3/g02_prii3_ws/mapas/f1l3_mapa.yaml
```

En RViz:

```text
2D Pose Estimate
→ indicar posición inicial

Nav2 Goal
→ seleccionar destino
```

---

## JetBot real

Para SLAM y navegación real se utilizan los launches proporcionados para el JetBot:

```text
slam.py
nav.py
```

El mapa real actual está almacenado en:

```text
mapas/jetbot_real/map.yaml
mapas/jetbot_real/map.pgm
```

Todos los comandos específicos del robot real están documentados en:

```text
README_JETBOT.md
```

---

# PBI 3.3 - Navegación predefinida

El nodo utilizado es:

```text
predefined_navigation
```

Su función es enviar automáticamente un objetivo fijo a Navigation2 mediante:

```text
nav2_msgs/action/NavigateToPose
```

---

## Simulación

Destino utilizado:

```text
X = 3.65
Y = -0.37
```

Primero deben estar abiertos Gazebo y Navigation2.

Después de realizar `2D Pose Estimate`, ejecutar:

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws

source /opt/ros/humble/setup.bash
source install/setup.bash

ros2 run g02_prii3_nav_turtlebot predefined_navigation
```

El robot navega automáticamente hasta la posición definida.

### Estado

```text
Simulación: probado correctamente
JetBot real: pendiente de introducir coordenadas reales y probar
```

Las coordenadas del JetBot no deben dejarse en `0.0` antes de realizar la prueba real.

---

# PBI 3.4 - Navegación autónoma con ArUco

El nodo utilizado es:

```text
autonomous_navigation
```

La lógica implementada es:

```text
inicio
↓
navegar hasta la entrada
↓
esperar a que Nav2 termine el recorrido
↓
activar lectura del ArUco
↓
detectar ID
↓
seleccionar destino
↓
navegar hasta destino final
```

Mientras el robot todavía está navegando hacia la entrada, los mensajes de `/aruco_info` son ignorados.

Esto evita detectar el marcador desde demasiado lejos.

---

## Simulación actual

La pose intermedia delante del ArUco 5 es:

```text
X = 3.24
Y = 1.71

orientation.z = 0.717
orientation.w = 0.697
```

Esta orientación deja al TurtleBot mirando hacia el marcador.

El comportamiento probado actualmente es:

```text
ArUco ID 5
→ destino final
```

Destino utilizado temporalmente en simulación:

```text
X = 2.75
Y = 14.42
```

Los ArUcos 6 y 17 están presentes en el escenario, pero sus posiciones actuales dificultan realizar la prueba completa de navegación hasta ellos.

La ampliación a tres destinos queda pendiente.

---

## Launch de navegación autónoma

El launch:

```text
g02_prii3_nav_turtlebot/launch/autonomous_navigation.launch.py
```

arranca:

```text
aruco_detection
autonomous_navigation
```

Para realizar la prueba desde cero:

### Terminal 1 - Gazebo

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws

source /opt/ros/humble/setup.bash
source install/setup.bash

export TURTLEBOT3_MODEL=waffle_pi

ros2 launch f1l3_gazebo f1l3_world.launch.py
```

### Terminal 2 - Navigation2

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws

source /opt/ros/humble/setup.bash
source install/setup.bash

export TURTLEBOT3_MODEL=waffle_pi

ros2 launch turtlebot3_navigation2 navigation2.launch.py \
use_sim_time:=True \
map:=$HOME/UNI/PROYECTOS3/g02_prii3_ws/mapas/f1l3_mapa.yaml
```

En RViz realizar:

```text
2D Pose Estimate
```

### Terminal 3 - Navegación autónoma

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws

source /opt/ros/humble/setup.bash
source install/setup.bash

ros2 launch g02_prii3_nav_turtlebot autonomous_navigation.launch.py
```

Salida esperada:

```text
Yendo hacia el ArUco...
Robot delante del ArUco. Esperando ID...
ArUco 5 detectado. Yendo a la mesa.
```

El flujo completo ha sido probado correctamente en simulación.

---

## JetBot real

También están preparados:

```text
g02_prii3_nav_jetbot/autonomous_navigation.py
g02_prii3_nav_jetbot/launch/autonomous_navigation.launch.py
```

El launch arranca:

```text
aruco_detection
autonomous_navigation
```

Antes de utilizarlo deben introducirse las coordenadas obtenidas en el mapa real:

```text
pose intermedia:
X
Y
orientation.z
orientation.w

destino final:
X
Y
```

No ejecutar la navegación autónoma del JetBot mientras esas coordenadas sigan configuradas como `0.0`.

---

# PBI 3.5 - Repositorio

La entrega final debe mantenerse en la rama:

```text
main
```

Antes de la entrega:

```bash
git status
git branch
```

Revisar que:

```text
- el código necesario esté incluido
- build/ no esté versionado
- install/ no esté versionado
- log/ no esté versionado
- los README estén actualizados
- no existan copias temporales innecesarias
```

---

# PBI 3.6 - Demostraciones

Actualmente existe un launch para la navegación autónoma que inicia:

```text
aruco_detection
autonomous_navigation
```

El objetivo final es dejar las demostraciones necesarias preparadas mediante archivos launch para reducir el número de comandos manuales durante la presentación.

La integración completa de Gazebo + Navigation2 + nodos del proyecto en un único launch queda pendiente.

---

# Comandos útiles

## Topics

```bash
ros2 topic list
```

ArUco:

```bash
ros2 topic echo /aruco_info
```

Cámara:

```bash
ros2 topic hz /camera/image_raw
```

Mapa:

```bash
ros2 topic echo /map --once
```

Odometría:

```bash
ros2 topic echo /odom --once
```

## Acciones

```bash
ros2 action list
```

Comprobar Navigation2:

```bash
ros2 action list | grep navigate_to_pose
```

## Nodos

```bash
ros2 node list
```

---

# Estado actual

```text
PBI 3.0
✅ Paquetes de navegación creados

PBI 3.1
✅ Detección DICT_4X4_100
✅ Publicación /aruco_info
✅ Probado con cámara del portátil
✅ Probado en simulación
⏳ Prueba con cámara del JetBot real

PBI 3.2
✅ SLAM en simulación
✅ Mapa de simulación
✅ Navegación guiada en simulación
✅ Mapa real disponible
⏳ Prueba final de navegación con JetBot real

PBI 3.3
✅ Navegación predefinida en simulación
⏳ Coordenadas y prueba con JetBot real

PBI 3.4
✅ Flujo autónomo con ArUco 5 en simulación
✅ Espera a llegar antes de aceptar el ArUco
✅ Launch detector + navegación autónoma
⏳ Tres ArUcos con tres destinos
⏳ Coordenadas y prueba con JetBot real

PBI 3.5
⏳ Limpieza final del repositorio y README

PBI 3.6
⏳ Launches finales para las demostraciones
```

## JetBot

La configuración completa del JetBot real se encuentra en:

```text
README_JETBOT.md
```