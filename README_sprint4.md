# Sprint 4 - Navegación con ArUcos (Eurobot)

**Proyecto RII 3 - Robots Inteligentes | Grupo 02**  
**Entorno:** ROS 2 Humble, Gazebo, TurtleBot3 y Nav2  
**Sprint Review:** 17 de diciembre de 2026

## Objetivo

Detectar marcadores ArUco y conseguir que el robot recorra los cuatro marcadores del tablero Eurobot y vuelva al centro. El Sprint incluye navegación mediante odometría y, posteriormente, mediante la cámara cenital.

## Estado del Sprint

| Apartado | Trabajo | Estado |
|---|---|---|
| PBI 4.1 | Detección de ArUcos 20-23 con cámara cenital y publicación de coordenadas por topic | Pendiente |
| PBI 4.2 | Recorrido autónomo por los cuatro ArUcos y vuelta al centro usando mapa y odometría | Nodo de simulación programado; pendiente de probar y adaptar al robot real |
| PBI 4.3 | Recorrido utilizando las posiciones de la cámara cenital | Pendiente |
| PBI 4.4 | Demostración desde un único launch, presentación, integración en `main` y README final | Pendiente |

## PBI 4.2 - Recorrido autónomo en simulación

El nodo `recorrer_arucos.py` está en:

```text
src/eurobot_gazebo/eurobot_gazebo/recorrer_arucos.py
```

Envía los objetivos mediante la acción `/navigate_to_pose` (`nav2_msgs/action/NavigateToPose`) en el marco `map`. Espera el resultado antes de mandar el siguiente destino. Si el destino es rechazado o falla, se detiene el recorrido.

### Coordenadas

| Orden | Destino | X (m) | Y (m) |
|---|---|---:|---:|
| 1 | ArUco 20 | 0.6 | 1.4 |
| 2 | ArUco 21 | 2.4 | 1.4 |
| 3 | ArUco 22 | 0.6 | 0.6 |
| 4 | ArUco 23 | 2.4 | 0.6 |
| 5 | Centro | 1.5 | 1.0 |

Son las coordenadas de referencia indicadas en `worlds/eurobot.world`. El robot aparece inicialmente en el centro por defecto.

## Comandos para ejecutar `recorrer_arucos`

Ejecutar **en el portátil**, dentro del workspace `g02_prii3_ws`.

### 1. Compilar (al modificar el código o `setup.py`)

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws
source /opt/ros/humble/setup.bash
colcon build --packages-select eurobot_gazebo --symlink-install
source install/setup.bash
```

El archivo `src/eurobot_gazebo/setup.py` debe registrar el ejecutable:

```python
entry_points={
    'console_scripts': [
        'recorrer_arucos = eurobot_gazebo.recorrer_arucos:main',
    ],
},
```

### 2. Terminal 1 - Abrir Gazebo

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 launch eurobot_gazebo eurobot_world.launch.py
```

### 3. Terminal 2 - Abrir Nav2 y RViz

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 launch eurobot_gazebo navigation.launch.py
```

Esperar a que los nodos de Nav2 estén activos. Este launch usa el mapa Eurobot y una transformación fija `map -> odom`: **no hace falta pulsar `2D Pose Estimate` en RViz**.

### 4. Terminal 3 - Ejecutar el recorrido

```bash
cd ~/UNI/PROYECTOS3/g02_prii3_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 run eurobot_gazebo recorrer_arucos --ros-args -p use_sim_time:=true
```

**Recorrido esperado:** ArUco 20 -> ArUco 21 -> ArUco 22 -> ArUco 23 -> Centro.

Los objetivos se envían **desde el código**, no desde RViz. Dejar RViz abierto para visualizar el mapa, la planificación y el progreso.

## Comprobaciones útiles

```bash
ros2 pkg executables eurobot_gazebo  # Debe aparecer recorrer_arucos
ros2 action list -t                 # Debe aparecer /navigate_to_pose
ros2 topic list                     # Topics publicados
ros2 topic echo /odom               # Odometría del robot
```

Si aparece `Package 'eurobot_gazebo' not found`, comprobar que el paquete se ha compilado y que se ha ejecutado `source install/setup.bash` **en esa terminal**.

## Pendiente

- Probar el recorrido completo en Gazebo y ajustar los destinos si alguno no es alcanzable.
- Trasladar la navegación al robot real y verificar su localización en el tablero.
- Implementar la detección de ArUcos mediante la cámara cenital (PBI 4.1).
- Utilizar los datos de la cámara para navegar (PBI 4.3).
- Unificar la demostración en un único fichero `launch` y actualizar el README principal (PBI 4.4).

> **Nota:** el mundo facilitado incluye las coordenadas de los ArUcos 20-23 en comentarios, pero todavía no representa visualmente los cuatro marcadores. La ruta programada utiliza esas coordenadas, no la detección visual.