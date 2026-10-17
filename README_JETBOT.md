# Ejecución en JetBot real

Este documento explica cómo ejecutar el nodo de dibujo en el **JetBot real**.

El JetBot utiliza **ROS 2 Foxy**.

## 1. Arrancar el JetBot

En una primera terminal:

```bash
source /opt/ros/foxy/setup.bash
source ~/jetbot_ws/install/setup.bash
ros2 launch jetbot_pro_ros2 jetbot.py
```

Esta terminal debe permanecer abierta mientras se ejecuta el robot.

## 2. Descargar o actualizar el proyecto

El repositorio del grupo debe estar disponible en:

```text
~/g02_prii3_ws
```

Si se clona desde cero:

```bash
cd ~
git clone https://github.com/jmarvid05/g02_prii3_ws.git
cd ~/g02_prii3_ws
```

Si ya existe y solo se quiere actualizar:

```bash
cd ~/g02_prii3_ws
git pull origin main
```

## 3. Compilar el paquete del JetBot

En una segunda terminal:

```bash
cd ~/g02_prii3_ws
source /opt/ros/foxy/setup.bash
source ~/jetbot_ws/install/setup.bash
colcon build --packages-select g02_prii3_move_jetbot
source install/setup.bash
```

## 4. Ejecutar el dibujo

Con la base del JetBot ya iniciada en la primera terminal:

```bash
cd ~/g02_prii3_ws
source /opt/ros/foxy/setup.bash
source ~/jetbot_ws/install/setup.bash
source install/setup.bash
ros2 launch g02_prii3_move_jetbot draw_number_jetbot.launch.py
```

## 5. Código utilizado en el JetBot

Código específico del robot real:

```text
src/g02_prii3_move_jetbot/g02_prii3_move_jetbot/draw_number_jetbot.py
```

La versión utilizada para simulación se mantiene en otro paquete:

```text
src/g02_prii3_move_turtlebot/g02_prii3_move_turtlebot/draw_number.py
```

De esta forma, los cambios realizados para adaptar el movimiento al robot físico no afectan a la simulación.

## 6. Valores ajustados para el robot real

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

## 7. Servicios de control del dibujo

El nodo `draw_number_jetbot` dispone de tres servicios ROS para controlar la trayectoria:

- `/detener_dibujo`: detiene temporalmente el movimiento del robot.
- `/reanudar_dibujo`: continúa el dibujo desde el punto en el que se había detenido.
- `/reiniciar_dibujo`: reinicia la trayectoria desde el primer estado.

Los tres servicios utilizan el tipo:

```text
std_srvs/srv/Trigger
```

Para detener el dibujo:

```bash
ros2 service call /detener_dibujo std_srvs/srv/Trigger "{}"
```

Para reanudar el dibujo:

```bash
ros2 service call /reanudar_dibujo std_srvs/srv/Trigger "{}"
```

Para reiniciar el dibujo:

```bash
ros2 service call /reiniciar_dibujo std_srvs/srv/Trigger "{}"
```

Al ejecutar cada servicio, el nodo muestra por terminal si el dibujo ha sido detenido, reanudado o reiniciado.

## 8. Editar el código

Para modificar el movimiento:

```bash
vim ~/g02_prii3_ws/src/g02_prii3_move_jetbot/g02_prii3_move_jetbot/draw_number_jetbot.py
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
source ~/jetbot_ws/install/setup.bash
colcon build --packages-select g02_prii3_move_jetbot
source install/setup.bash
```

Y volver a ejecutar:

```bash
ros2 launch g02_prii3_move_jetbot draw_number_jetbot.launch.py
```

## 9. Comprobaciones

Para comprobar los nodos activos:

```bash
ros2 node list
```

Deberían aparecer, entre otros:

```text
/jetbot
/draw_number
```

Para comprobar los servicios del dibujo:

```bash
ros2 service list
```

Deberían aparecer:

```text
/detener_dibujo
/reanudar_dibujo
/reiniciar_dibujo
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

## 10. Parar el robot

Para detener la ejecución:

```text
Ctrl+C
```

Si fuera necesario enviar manualmente velocidad cero:

```bash
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.0}, angular: {z: 0.0}}"
```

## Grupo

**Grupo 02**