# Ejecución en JetBot real

Este documento explica cómo ejecutar el nodo de dibujo en el **JetBot real**.

El JetBot utiliza **ROS 2 Foxy**.

---

## 1. Arrancar el JetBot

En una primera terminal:

```bash
source /opt/ros/foxy/setup.bash
source ~/jetbot_ws/install/setup.bash
ros2 launch jetbot_pro_ros2 jetbot.py
```

Esta terminal debe permanecer abierta mientras se ejecuta el robot.

---

## 2. Ejecutar el dibujo

En una segunda terminal:

```bash
cd ~/g02_prii3_ws
source /opt/ros/foxy/setup.bash
source ~/jetbot_ws/install/setup.bash
colcon build --packages-select g02_prii3_move_turtlebot
source install/setup.bash
ros2 launch g02_prii3_move_turtlebot draw_number_jetbot.launch.py
```

---

## 3. Código utilizado en el JetBot

Código específico del robot real:

```text
src/g02_prii3_move_turtlebot/g02_prii3_move_turtlebot/draw_number_jetbot.py
```

Versión utilizada para simulación:

```text
src/g02_prii3_move_turtlebot/g02_prii3_move_turtlebot/draw_number.py
```

De esta forma, los cambios realizados para adaptar el movimiento al robot físico no afectan a la simulación.

---

## 4. Valores ajustados para el robot real

### Estado 0 - Curva

```python
msg.linear.x = 0.12
msg.angular.z = -0.55
self.contador >= 75
```

### Estado 1 - Diagonal recta

```python
msg.linear.x = 0.12
msg.angular.z = 0.0
self.contador >= 35
```

### Estado 2 - Giro a la izquierda

```python
msg.linear.x = 0.0
msg.angular.z = 0.8
self.contador >= 34
```

### Estado 3 - Base recta

```python
msg.linear.x = 0.12
msg.angular.z = 0.0
self.contador >= 33
```

Estos valores fueron ajustados mediante pruebas con el JetBot real.

---

## 5. Editar el código

Para modificar el movimiento:

```bash
vim ~/g02_prii3_ws/src/g02_prii3_move_turtlebot/g02_prii3_move_turtlebot/draw_number_jetbot.py
```

Comandos básicos de Vim:

```text
i       editar
Esc     salir del modo edición
:wq     guardar y salir
```

Después de modificar el código, volver a compilar:

```bash
cd ~/g02_prii3_ws
source /opt/ros/foxy/setup.bash
colcon build --packages-select g02_prii3_move_turtlebot
source install/setup.bash
```

Y volver a ejecutar:

```bash
ros2 launch g02_prii3_move_turtlebot draw_number_jetbot.launch.py
```

---

## 6. Comprobaciones

Para comprobar los nodos activos:

```bash
ros2 node list
```

Deberían aparecer, entre otros:

```text
/jetbot
/draw_number
```

Para comprobar que el JetBot está suscrito al topic de movimiento:

```bash
ros2 node info /jetbot
```

El JetBot debe estar suscrito a:

```text
/cmd_vel
```

Para visualizar los comandos enviados al robot:

```bash
ros2 topic echo /cmd_vel
```

---

## 7. Parar el robot

Para detener la ejecución:

```text
Ctrl+C
```

Si fuera necesario enviar manualmente velocidad cero:

```bash
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.0}, angular: {z: 0.0}}"
```

---

## Grupo

**Grupo 02**
