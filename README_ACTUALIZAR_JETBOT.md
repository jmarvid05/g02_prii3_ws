# README - Actualizar proyecto en el JetBot

**Grupo 02 - Sprint 2**

## Datos del JetBot

- **Usuario:** `jetbot`
- **IP:** `172.16.190.184`
- **Repositorio:** `https://github.com/jmarvid05/g02_prii3_ws.git`
- **Rama:** `main`

---

## 1. Conectarse al JetBot

Desde el portátil:

```bash
ssh jetbot@172.16.190.184
```

---

## 2. Comprobar el repositorio actual

En el JetBot:

```bash
cd ~
ls
```

Si existe:

```text
~/g02_prii3_ws
```

podemos comprobar antes su estado:

```bash
cd ~/g02_prii3_ws
git status
git branch
```

---

## 3. Borrar el repositorio antiguo

Volver a la carpeta personal:

```bash
cd ~
```

Borrar completamente el repositorio antiguo:

```bash
rm -rf ~/g02_prii3_ws
```

Comprobar que ya no existe:

```bash
ls
```

---

## 4. Clonar el repositorio actualizado desde GitHub

```bash
cd ~

git clone -b main https://github.com/jmarvid05/g02_prii3_ws.git
```

Entrar en el nuevo repositorio:

```bash
cd ~/g02_prii3_ws
```

Comprobar:

```bash
git branch
git status
```

Debe aparecer:

```text
* main
```

y el repositorio debe estar limpio.

---

## 5. Comprobar que no hay códigos obsoletos

```bash
find src -name "*.py" | sort
```

En el Sprint 2 deben estar, entre otros:

```text
g02_prii3_move_jetbot/
- draw_number_jetbot.py
- laser_filter.py
- collision_avoidance.py
- camera_rectification.py
- aruco_detection.py
```

No debe aparecer `obstacle_avoidance.py` como código del Sprint 2 actual.

---

## 6. Cargar ROS 2 Foxy y el workspace base del JetBot

```bash
source /opt/ros/foxy/setup.bash
source ~/jetbot_ws/install/setup.bash

export ROS_DOMAIN_ID=184
export ROS_LOCALHOST_ONLY=0
```

---

## 7. Compilar el paquete del JetBot

Como acabamos de clonar el repositorio, la compilación parte limpia.

```bash
cd ~/g02_prii3_ws

source /opt/ros/foxy/setup.bash
source ~/jetbot_ws/install/setup.bash

colcon build --packages-select g02_prii3_move_jetbot --symlink-install
```

Cuando termine:

```bash
source install/setup.bash
```

---

## 8. Comprobar los ejecutables

```bash
ros2 pkg executables g02_prii3_move_jetbot
```

Deben aparecer:

```text
g02_prii3_move_jetbot aruco_detection
g02_prii3_move_jetbot camera_rectification
g02_prii3_move_jetbot collision_avoidance
g02_prii3_move_jetbot draw_number_jetbot
g02_prii3_move_jetbot laser_filter
```

---

## 9. Arrancar la base del JetBot

### Terminal 1

```bash
source /opt/ros/foxy/setup.bash
source ~/jetbot_ws/install/setup.bash

export ROS_DOMAIN_ID=184
export ROS_LOCALHOST_ONLY=0

ros2 launch jetbot_pro_ros2 jetbot.py
```

Dejar esta terminal abierta.

---

## 10. Comprobar el LiDAR

En otra terminal del JetBot:

```bash
source /opt/ros/foxy/setup.bash
source ~/jetbot_ws/install/setup.bash

export ROS_DOMAIN_ID=184
export ROS_LOCALHOST_ONLY=0

ros2 topic list | grep scan
```

Comprobar frecuencia:

```bash
ros2 topic hz /scan
```

---

## 11. Probar `draw_number`

### Terminal 2

```bash
cd ~/g02_prii3_ws

source /opt/ros/foxy/setup.bash
source ~/jetbot_ws/install/setup.bash
source install/setup.bash

export ROS_DOMAIN_ID=184
export ROS_LOCALHOST_ONLY=0

ros2 launch g02_prii3_move_jetbot draw_number_jetbot.launch.py
```

---

## 12. Probar `collision_avoidance`

> **Importante:** no ejecutar `draw_number` y `collision_avoidance` al mismo tiempo, porque ambos publican en `/cmd_vel`.

Detener primero `draw_number` con:

```text
Ctrl+C
```

Después ejecutar:

```bash
cd ~/g02_prii3_ws

source /opt/ros/foxy/setup.bash
source ~/jetbot_ws/install/setup.bash
source install/setup.bash

export ROS_DOMAIN_ID=184
export ROS_LOCALHOST_ONLY=0

ros2 launch g02_prii3_move_jetbot collision_avoidance_jetbot.launch.py
```

Este launch realiza el flujo:

```text
/scan
  ↓
laser_filter
  ↓
/filtered_scan
  ↓
collision_avoidance
  ↓
/cmd_vel
```

---

## 13. Comprobar nodos y topics

```bash
ros2 node list
ros2 topic list
```

Comprobar cada nodo:

```bash
ros2 node info /laser_filter
ros2 node info /collision_avoidance
```

Comprobar los topics:

```bash
ros2 topic info /scan -v
ros2 topic info /filtered_scan -v
ros2 topic info /cmd_vel -v
```

---

## 14. Actualizaciones futuras

Una vez que el JetBot ya tenga esta versión limpia, para futuras actualizaciones no hace falta borrar y volver a clonar.

```bash
cd ~/g02_prii3_ws
git switch main
git pull origin main
```

Después recompilar:

```bash
source /opt/ros/foxy/setup.bash
source ~/jetbot_ws/install/setup.bash

rm -rf build install log

colcon build --packages-select g02_prii3_move_jetbot --symlink-install

source install/setup.bash
```

---

# Resumen rápido

Instalación limpia:

```bash
ssh jetbot@172.16.190.184

cd ~
rm -rf ~/g02_prii3_ws

git clone -b main https://github.com/jmarvid05/g02_prii3_ws.git

cd ~/g02_prii3_ws

source /opt/ros/foxy/setup.bash
source ~/jetbot_ws/install/setup.bash

colcon build --packages-select g02_prii3_move_jetbot --symlink-install

source install/setup.bash
```
