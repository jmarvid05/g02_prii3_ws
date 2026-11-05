### Comando para detectar arucos en tiempo real
```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws
python3 calibracion/aruco_webcam.py
```

### Comprobar cámaras disponibles
```bash
v4l2-ctl --list-devices
ls -l /dev/video*
```
Cámara portatil = 1, cámara I3L7 = 5.

Terminal 1:
source /opt/ros/humble/setup.bash
source install/setup.bash
export TURTLEBOT3_MODEL=burger

ros2 launch f1l3_gazebo f1l3_world.launch.py

Terminal 2:
source /opt/ros/humble/setup.bash
source install/setup.bash
export TURTLEBOT3_MODEL=burger

ros2 launch turtlebot3_navigation2 navigation2.launch.py use_sim_time:=True map:=$HOME/UNI/PROYECTOS3/g02_prii3_ws/mapas/f1l3_mapa.yaml

