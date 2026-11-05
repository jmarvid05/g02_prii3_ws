# JetBot — SLAM, guardado de mapas y navegación con RViz

Esta guía resume el flujo para trabajar con el **JetBot real**:

1. Arrancar la base del JetBot y sus sensores.
2. Comprobar la comunicación ROS 2 entre JetBot y portátil.
3. Recorrer un entorno mientras se genera un mapa con SLAM.
4. Guardar el mapa dentro del repositorio.
5. Cargar ese mapa más adelante.
6. Localizar el robot con **2D Pose Estimate**.
7. Marcar un destino con **Nav2 Goal** para que el robot navegue automáticamente.

> **Importante:** los comandos de `turtlebot3_cartographer` y `turtlebot3_navigation2` que usamos en simulación son específicos de TurtleBot3. Para el JetBot real necesitamos una configuración adaptada a sus frames y topics (`/scan`, `/odom`, `/tf`, `/cmd_vel`).

---

## 1. Conectarse al JetBot

Desde el portátil:

```bash
ssh jetbot@172.16.190.184
```

Comprobar el dominio ROS:

```bash
echo $ROS_DOMAIN_ID
echo $ROS_LOCALHOST_ONLY
```

Debe aparecer:

```text
184
0
```

---

## 2. Arrancar la base del JetBot

### Terminal 1 — JetBot

```bash
source /opt/ros/foxy/setup.bash
source ~/jetbot_ws/install/setup.bash

export ROS_DOMAIN_ID=184
export ROS_LOCALHOST_ONLY=0

ros2 launch jetbot_pro_ros2 jetbot.py
```

Dejar esta terminal abierta.

La base debe publicar, entre otros:

```text
/scan
/odom
/tf
/tf_static
```

y aceptar velocidades mediante:

```text
/cmd_vel
```

---

## 3. Comprobar sensores desde el portátil

### Terminal 2 — Portátil

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws
source /opt/ros/humble/setup.bash
source install/setup.bash

export ROS_DOMAIN_ID=184
export ROS_LOCALHOST_ONLY=0
```

Comprobar topics:

```bash
ros2 topic list | grep -E 'scan|odom|cmd_vel|tf'
```

Comprobar LiDAR:

```bash
ros2 topic hz /scan
```

Comprobar odometría:

```bash
ros2 topic echo /odom --once
```

Antes de continuar deben existir al menos:

```text
/scan
/odom
/tf
/tf_static
/cmd_vel
```

---

# PARTE A — CREAR UN MAPA NUEVO

## 4. Ejecutar SLAM en el portátil

El SLAM se ejecuta en el portátil usando los datos publicados por el JetBot.

La configuración debe utilizar:

```text
LiDAR:       /scan
Odometría:   /odom
TF:          /tf
Frame mapa:  map
Frame odom:  odom
Frame robot: base_link o el frame base real del JetBot
```

Antes de lanzar SLAM conviene comprobar el árbol TF:

```bash
ros2 run tf2_ros tf2_echo odom base_link
```

> Si el JetBot utiliza otro nombre para su frame base, hay que usar ese nombre en la configuración.

> No utilizar directamente el launch de Cartographer de TurtleBot3 sin adaptar sus parámetros.

---

## 5. Mover el JetBot mientras se crea el mapa

Durante el mapeado, recorrer el entorno lentamente para que el LiDAR detecte paredes y obstáculos desde distintas posiciones.

El robot se puede controlar mediante un nodo de teleoperación que publique en:

```text
/cmd_vel
```

Mientras se mueve, RViz irá mostrando el mapa que genera SLAM.

Conviene:

- recorrer todos los pasillos;
- hacer giros suaves;
- acercarse a las zonas sin explorar;
- volver a pasar por zonas conocidas para ayudar a cerrar el mapa.

---

## 6. Guardar el mapa dentro del repositorio

Crear la carpeta si no existe:

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws
mkdir -p mapas
```

Guardar el mapa:

```bash
ros2 run nav2_map_server map_saver_cli \
-f ~/UNI/PROYECTOS3/g02_prii3_ws/mapas/jetbot_mapa
```

Se crearán:

```text
mapas/jetbot_mapa.pgm
mapas/jetbot_mapa.yaml
```

Comprobar:

```bash
ls -l mapas/
```

El `.pgm` contiene la imagen del mapa y el `.yaml` sus parámetros.

---

# PARTE B — NAVEGAR USANDO UN MAPA GUARDADO

## 7. Arrancar de nuevo el JetBot

### Terminal 1 — JetBot

```bash
source /opt/ros/foxy/setup.bash
source ~/jetbot_ws/install/setup.bash

export ROS_DOMAIN_ID=184
export ROS_LOCALHOST_ONLY=0

ros2 launch jetbot_pro_ros2 jetbot.py
```

Dejar esta terminal abierta.

---

## 8. Comprobar comunicación desde el portátil

### Terminal 2 — Portátil

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws
source /opt/ros/humble/setup.bash
source install/setup.bash

export ROS_DOMAIN_ID=184
export ROS_LOCALHOST_ONLY=0
```

Comprobar:

```bash
ros2 topic hz /scan
ros2 topic echo /odom --once
```

---

## 9. Cargar Navigation2 con el mapa

Navigation2 debe ejecutarse con una configuración adaptada al JetBot y cargar:

```text
~/UNI/PROYECTOS3/g02_prii3_ws/mapas/jetbot_mapa.yaml
```

La configuración debe trabajar con:

```text
map
odom
base_link
/scan
/odom
/cmd_vel
```

y utilizar AMCL para localizar el robot dentro del mapa.

> Igual que con SLAM, no debemos usar directamente la configuración de TurtleBot3 sin adaptar los frames, dimensiones y parámetros del JetBot.

---

## 10. Indicar la posición inicial en RViz

Cuando Navigation2 y RViz estén funcionando:

1. Pulsar **2D Pose Estimate**.
2. Hacer clic sobre la posición real del JetBot en el mapa.
3. Arrastrar la flecha indicando hacia dónde está mirando.
4. Soltar.

AMCL comparará el LiDAR con el mapa guardado para ajustar la localización.

El `LaserScan` debe coincidir aproximadamente con las paredes del mapa.

---

## 11. Enviar un destino al JetBot

Cuando el robot esté bien localizado:

1. Pulsar **Nav2 Goal**.
2. Hacer clic en una zona libre del mapa.
3. Arrastrar la flecha para indicar la orientación final.
4. Soltar.

Flujo simplificado:

```text
Mapa guardado
     +
LiDAR
     +
Odometría
     ↓
AMCL localiza el JetBot
     ↓
Nav2 Goal
     ↓
Planner calcula la ruta
     ↓
Controller genera velocidades
     ↓
/cmd_vel
     ↓
JetBot se mueve
```

---

## 12. Comprobaciones útiles

Ver nodos:

```bash
ros2 node list
```

Ver topics principales:

```bash
ros2 topic list | grep -E 'scan|odom|cmd_vel|tf|map'
```

Comprobar LiDAR:

```bash
ros2 topic hz /scan
```

Comprobar transformación:

```bash
ros2 run tf2_ros tf2_echo odom base_link
```

Comprobar publishers de velocidad:

```bash
ros2 topic info /cmd_vel
```

---

## Importante

Durante el mapeado podemos controlar el robot manualmente.
```bash
source /opt/ros/humble/setup.bash
export ROS_DOMAIN_ID=184
export ROS_LOCALHOST_ONLY=0
```

ros2 run teleop_twist_keyboard teleop_twist_keyboard

Durante la navegación automática, detener cualquier teleoperación antes de enviar un objetivo con Navigation2.

No deben estar a la vez dos nodos intentando controlar:

```text
/cmd_vel
```

Flujo completo:

```text
JETBOT + LiDAR + ODOM
        ↓
       SLAM
        ↓
    CREAR MAPA
        ↓
    GUARDAR MAPA
        ↓
  CARGAR MAPA + AMCL
        ↓
  2D Pose Estimate
        ↓
     Nav2 Goal
        ↓
 NAVEGACIÓN AUTOMÁTICA
```

---

## Pendiente para dejarlo completamente operativo en el JetBot

Para tener este procedimiento completamente automatizado dentro del proyecto falta preparar y probar una configuración específica del JetBot para:

- SLAM;
- AMCL;
- Navigation2;
- frames correctos del JetBot;
- dimensiones/footprint del robot;
- conexión de Navigation2 con `/cmd_vel`.

Una vez comprobados esos parámetros, se pueden añadir launch files propios al paquete `g02_prii3_move_jetbot` para arrancar SLAM y navegación con un solo comando.
