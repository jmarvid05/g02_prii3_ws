#!/usr/bin/env python3

import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():

    # Usa el reloj de simulación.
    use_sim_time = LaunchConfiguration(
        'use_sim_time',
        default='true'
    )

    # Carpeta instalada de nuestro paquete.
    package_share = get_package_share_directory(
        'f1l3_gazebo'
    )

    # Mundo F1L3.
    world = os.path.join(
        package_share,
        'worlds',
        'f1l3.world'
    )

    # Carpeta donde están nuestros ArUcos.
    models = os.path.join(
        package_share,
        'models'
    )

    # Mantiene también otros modelos que ya tenga Gazebo.
    old_model_path = os.environ.get(
        'GAZEBO_MODEL_PATH',
        ''
    )

    if old_model_path:
        model_path = models + os.pathsep + old_model_path
    else:
        model_path = models

    # Launches de TurtleBot3.
    turtlebot_launch = os.path.join(
        get_package_share_directory('turtlebot3_gazebo'),
        'launch'
    )

    # Launches de Gazebo.
    gazebo_launch = os.path.join(
        get_package_share_directory('gazebo_ros'),
        'launch'
    )

    return LaunchDescription([

        # Usa Waffle Pi porque necesitamos cámara.
        SetEnvironmentVariable(
            'TURTLEBOT3_MODEL',
            'waffle_pi'
        ),

        # Permite que Gazebo encuentre nuestros ArUcos.
        SetEnvironmentVariable(
            'GAZEBO_MODEL_PATH',
            model_path
        ),

        # Lanza Gazebo con el mundo F1L3.
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(
                    gazebo_launch,
                    'gzserver.launch.py'
                )
            ),
            launch_arguments={
                'world': world
            }.items(),
        ),

        # Abre la interfaz gráfica de Gazebo.
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(
                    gazebo_launch,
                    'gzclient.launch.py'
                )
            ),
        ),

        # Publica el estado del TurtleBot.
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(
                    turtlebot_launch,
                    'robot_state_publisher.launch.py'
                )
            ),
            launch_arguments={
                'use_sim_time': use_sim_time
            }.items(),
        ),
    ])