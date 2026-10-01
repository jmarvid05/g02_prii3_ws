TURTLEBOT3 - CASA Y CAMARA

1. Abrir la casa:

source /opt/ros/humble/setup.bash
export TURTLEBOT3_MODEL=waffle_pi
ros2 launch turtlebot3_gazebo turtlebot3_house.launch.py


2. Controlar con teclado (otra terminal):

source /opt/ros/humble/setup.bash
export TURTLEBOT3_MODEL=waffle_pi
ros2 run turtlebot3_teleop teleop_keyboard


3. Ver la camara POV (otra terminal):

source /opt/ros/humble/setup.bash
ros2 run rqt_image_view rqt_image_view

Seleccionar el topic de la camara, por ejemplo:
/camera/image_raw

4. Cerrar

Ctrl + c para matar la terminal y usar comandos: 
pkill gzclient
pkill gzserver