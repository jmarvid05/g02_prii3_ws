# g02_prii3_ws - Grupo 02

Workspace ROS 2 del proyecto **Proyecto RII 3: Robots Inteligentes**.

El repositorio contiene el trabajo realizado durante los distintos sprints del proyecto, tanto para simulación como para el robot JetBot real.

## Documentación

- [Sprint 1](README_sprint1.md)  
  Turtlesim, movimiento y servicios ROS 2.

- [Sprint 2](README_sprint2.md)  
  TurtleBot3, JetBot, LiDAR, evitación de colisiones y visión.

- [Sprint 3](README_sprint3.md)  
  Navegación, SLAM, detección de ArUcos y navegación autónoma.

- [JetBot real](README_JETBOT.md)  
  Configuración, conexión, mapas y comandos específicos del JetBot.

- [Comandos rápidos del Sprint 3](COMANDOS_SPRINT3.md)
  Secuencias de arranque y comprobación en simulación y JetBot real.

## Paquetes principales

```text
src/
├── f1l3_gazebo
├── g02_prii3_move_jetbot
├── g02_prii3_move_turtlebot
├── g02_prii3_turtlesim
├── g02_prii3_nav_jetbot
└── g02_prii3_nav_turtlebot
```

### Navegación

Los paquetes utilizados en el Sprint 3 son:

```text
g02_prii3_nav_turtlebot
```

Navegación y detección de ArUcos en simulación.

```text
g02_prii3_nav_jetbot
```

Navegación y detección de ArUcos para el JetBot real. El lanzamiento `nav.py` incorpora `nav2_auto_start`, que automatiza la activación de Nav2 después de indicar la pose inicial desde RViz (pendiente de validación de la automatización con el robot físico).

## Compilación del workspace

Desde la raíz del proyecto:

```bash
source /opt/ros/humble/setup.bash

colcon build --symlink-install

source install/setup.bash
```

## Uso de Inteligencia Artificial

Se ha utilizado Inteligencia Artificial como herramienta de apoyo para organizar, revisar y documentar parte del código del proyecto.

El código se valida por etapas: la navegación guiada en el JetBot real fue probada; el nuevo arranque automático de Nav2 queda pendiente de prueba física.