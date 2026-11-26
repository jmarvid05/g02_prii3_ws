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

Comprobar ejecutables:

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

El nodo:

```text
aruco_detection
```

recibe imágenes desde:

```text
/camera/image_raw
```

y publica los ArUcos detectados en:

```text
/aruco_info
```

utilizando:

```text
std_msgs/msg/String
```

Ejemplo:

```text
ID: 5, X: 248, Y: 236
```

Si aparecen varios marcadores:

```text
ID: 5, X: ... , Y: ... | ID: 6, X: ... , Y: ...
```

Los valores `X` e `Y` representan el centro del marcador en la imagen.

Cuando no se detecta ninguno:

```text
[]
```

---

## Cámara del portátil

Comprobar cámaras disponibles:

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

### Terminal 3 - Comprobar

```bash
source /opt/ros/humble/setup.bash

ros2 topic echo /aruco_info
```

Se comprobó correctamente la detección del ArUco ID 37 y el cambio de sus coordenadas al moverlo.

---

# ArUcos en simulación

Los modelos utilizados son:

```text
aruco_5
aruco_6
aruco_17
```

Los tres utilizan:

```text
DICT_4X4_100
```

Los modelos se encuentran directamente dentro del paquete:

```text
src/f1l3_gazebo/src/f1l3_gazebo/models/
```

Estructura:

```text
models/
├── aruco_5/
├── aruco_6/
└── aruco_17/
```

Por tanto, ya no es necesario instalar los modelos manualmente en:

```text
~/.gazebo/models
```

El launch `f1l3_world.launch.py` configura automáticamente:

```text
TURTLEBOT3_MODEL=waffle_pi
GAZEBO_MODEL_PATH
```

para utilizar el TurtleBot con cámara y encontrar los modelos ArUco incluidos en el paquete.

Se comprobó la detección correcta en simulación de:

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

ros2 launch f1l3_gazebo f1l3_world.launch.py
```

No es necesario hacer manualmente:

```text
export TURTLEBOT3_MODEL=waffle_pi
```

porque el propio launch lo configura.

### Terminal 2 - SLAM

```bash
source /opt/ros/humble/setup.bash

export TURTLEBOT3_MODEL=waffle_pi

ros2 launch turtlebot3_cartographer cartographer.launch.py \
use_sim_time:=True
```

### Mover con mando Xbox

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

El mapa está almacenado en:

```text
mapas/f1l3_mapa.yaml
mapas/f1l3_mapa.pgm
```

También existe una copia dentro del paquete de navegación:

```text
src/g02_prii3_nav_turtlebot/maps/f1l3_mapa.yaml
src/g02_prii3_nav_turtlebot/maps/f1l3_mapa.pgm
```

Esta copia permite que los launches no dependan de rutas absolutas del workspace.

---

## Simulación - Navegación guiada

### Terminal 1 - Gazebo

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws

source /opt/ros/humble/setup.bash
source install/setup.bash

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
→ indicar la posición inicial

Nav2 Goal
→ seleccionar el destino
```

La navegación guiada ha sido probada correctamente.

---

## JetBot real: inicio automático y prueba guiada

El mapa real F1L3 está almacenado en:

```text
mapas/jetbot_real/map.yaml
mapas/jetbot_real/map.pgm
```

El launch del grupo usa la copia incluida en el paquete:

```text
src/g02_prii3_nav_jetbot/maps/map.yaml
```

Se ha incorporado `nav2_auto_start.py` para iniciar la localización, esperar
**2D Pose Estimate** en RViz, comprobar TF y activar después los nodos de
navegación. El `nav.py` del grupo conserva `autostart=False` y arranca este
nodo auxiliar.

**Comandos principales (JetBot por SSH):**

```bash
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash
source ~/g02_prii3_ws/install/setup.bash
export ROS_DOMAIN_ID=172 ROS_LOCALHOST_ONLY=0
ros2 launch g02_prii3_nav_jetbot nav.py
```

**RViz (portátil local):**

```bash
source /opt/ros/humble/setup.bash
export ROS_DOMAIN_ID=172 ROS_LOCALHOST_ONLY=0
rviz2 -d ~/UNI/PROYECTOS3/g02_prii3_ws/config/jetbot_f1l3.rviz
```

Una vez aparezca el mapa, indicar la pose inicial real y comprobar la
localización antes de enviar destinos. **La navegación guiada con el JetBot
real se ha probado**; la automatización del nuevo nodo se ha compilado en el
portátil, pero su prueba física está pendiente. La prueba de ArUcos con la
cámara CSI del JetBot continúa pendiente.

Para la secuencia completa y las verificaciones, ver
[README_JETBOT.md](README_JETBOT.md) y
[COMANDOS_SPRINT3.md](COMANDOS_SPRINT3.md).

---

# PBI 3.3 - Navegación predefinida

El nodo utilizado es:

```text
predefined_navigation
```

Envía automáticamente un objetivo fijo mediante:

```text
nav2_msgs/action/NavigateToPose
```

## Simulación

Destino probado:

```text
X = 3.65
Y = -0.37
```

Con Gazebo y Navigation2 activos y después de realizar `2D Pose Estimate`:

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws

source /opt/ros/humble/setup.bash
source install/setup.bash

ros2 run g02_prii3_nav_turtlebot predefined_navigation
```

El TurtleBot navega automáticamente al destino.

Estado:

```text
Simulación: probado correctamente
JetBot real: pendiente de coordenadas reales y prueba física
```

No debe ejecutarse `predefined_navigation` del JetBot mientras sus coordenadas continúen en:

```text
0.0, 0.0
```

---

# PBI 3.4 - Navegación autónoma con ArUco

El nodo utilizado es:

```text
autonomous_navigation
```

La lógica implementada es:

```text
esperar 2D Pose Estimate
↓
esperar a que Navigation2 esté preparado
↓
navegar a la pose intermedia
↓
comprobar que Nav2 ha llegado correctamente
↓
activar lectura de ArUcos
↓
detectar ID
↓
seleccionar destino
↓
navegar al destino final
```

Los mensajes de `/aruco_info` se ignoran hasta que el robot ha llegado correctamente a la pose intermedia.

La llegada se comprueba mediante:

```text
GoalStatus.STATUS_SUCCEEDED
```

Esto evita detectar el ArUco desde demasiado lejos.

---

## Pose intermedia

Pose utilizada delante del ArUco 5:

```text
X = 3.24
Y = 1.71

orientation.z = 0.717
orientation.w = 0.697
```

Esta orientación deja el robot mirando hacia el marcador.

---

## ArUco 5

Actualmente se ha probado:

```text
ArUco ID 5
→ destino final
```

La comprobación del ID se realiza de forma exacta para evitar confundir:

```text
ID 5
```

con marcadores como:

```text
ID 50
ID 51
```

Destino temporal utilizado en simulación:

```text
X = 2.75
Y = 14.42
```

Los ArUcos 6 y 17 están correctamente disponibles y detectables en Gazebo, pero sus posiciones actuales dificultan completar con ellos la misma prueba de navegación.

La ampliación a tres IDs con tres destinos diferentes queda pendiente.

---

# Launch completo de simulación

El archivo:

```text
g02_prii3_nav_turtlebot/launch/simulation.launch.py
```

permite arrancar mediante una sola orden:

```text
Gazebo
Navigation2
RViz
aruco_detection
autonomous_navigation
```

El mapa se obtiene directamente desde el paquete:

```text
g02_prii3_nav_turtlebot/maps/f1l3_mapa.yaml
```

También se utiliza automáticamente:

```text
TURTLEBOT3_MODEL=waffle_pi
```

## Ejecutar demo completa

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws

source /opt/ros/humble/setup.bash
source install/setup.bash

ros2 launch g02_prii3_nav_turtlebot simulation.launch.py
```

Esperar a que se abran Gazebo y RViz.

El nodo mostrará:

```text
Esperando 2D Pose Estimate en RViz...
```

En RViz utilizar:

```text
2D Pose Estimate
```

Después el nodo espera unos segundos para permitir que AMCL y Navigation2 terminen de activarse.

Salida esperada:

```text
Pose inicial recibida desde RViz.
Esperando a que Nav2 esté preparado...
Yendo hacia el ArUco...
Destino aceptado. Navegando...
Robot delante del ArUco.
Esperando ID del ArUco...
ArUco 5 detectado.
Yendo a la mesa del profesor...
```

El flujo completo ha sido probado correctamente en simulación.

---

# JetBot real - Navegación autónoma

Están preparados:

```text
g02_prii3_nav_jetbot/autonomous_navigation.py
g02_prii3_nav_jetbot/launch/autonomous_navigation.launch.py
```

El launch arranca:

```text
aruco_detection
autonomous_navigation
```

Antes de utilizarlo deben introducirse las coordenadas obtenidas sobre el mapa real:

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

No ejecutar mientras esas coordenadas continúen a `0.0`.

La prueba física queda pendiente.

---

# PBI 3.5 - Repositorio

La entrega final se mantiene en:

```text
main
```

Los README se han reorganizado en:

```text
README.md
README_sprint1.md
README_sprint2.md
README_sprint3.md
README_JETBOT.md
```

Los mapas utilizados actualmente son:

```text
mapas/
├── f1l3_mapa.yaml
├── f1l3_mapa.pgm
└── jetbot_real/
    ├── map.yaml
    └── map.pgm
```

Antes de cada entrega:

```bash
git status
git branch
```

Comprobar que:

```text
- build/ no esté versionado
- install/ no esté versionado
- log/ no esté versionado
- no existan README duplicados
- no existan mapas antiguos innecesarios
- el código compile correctamente
```

---

# PBI 3.6 - Demostraciones

## Simulación

La demostración autónoma completa puede ejecutarse con una sola orden:

```bash
ros2 launch g02_prii3_nav_turtlebot simulation.launch.py
```

Este launch inicia:

```text
Gazebo
Navigation2
RViz
detector ArUco
navegación autónoma
```

Estado:

```text
Simulación: launch completo probado correctamente
JetBot real: pendiente de prueba física y coordenadas reales
```

---

# Comandos útiles

## ArUco

```bash
ros2 topic echo /aruco_info
```

## Cámara

```bash
ros2 topic hz /camera/image_raw
```

## Mapa

```bash
ros2 topic echo /map --once
```

## Odometría

```bash
ros2 topic echo /odom --once
```

## Pose inicial

```bash
ros2 topic echo /initialpose
```

## Acciones Nav2

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
✅ DICT_4X4_100
✅ Publicación /aruco_info
✅ Probado con cámara del portátil
✅ ArUcos 5, 6 y 17 integrados en f1l3_gazebo
✅ Probado en simulación
⏳ Prueba con cámara del JetBot real

PBI 3.2
✅ SLAM en simulación
✅ Mapa de simulación
✅ Navegación guiada en simulación
✅ Mapa real disponible
⏳ Prueba final con JetBot real

PBI 3.3
✅ Navegación predefinida en simulación
⏳ Coordenadas y prueba con JetBot real

PBI 3.4
✅ Navegación autónoma con ArUco 5 en simulación
✅ Espera a 2D Pose Estimate
✅ Espera a que Nav2 esté preparado
✅ Comprueba llegada correcta
✅ Lectura exacta del ID 5
✅ Destino final automático
⏳ Tres ArUcos con tres destinos
⏳ Coordenadas y prueba con JetBot real

PBI 3.5
✅ README reorganizados
✅ Mapas antiguos eliminados
✅ Estructura del repositorio revisada
⏳ Commit final de los últimos cambios

PBI 3.6
✅ Launch completo de simulación
⏳ Demostración final con JetBot real
```

## JetBot

La configuración y los comandos específicos del robot real están en:

```text
README_JETBOT.md
```