import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node


def generate_launch_description():

    # Paquete de navegación del proyecto.
    nav_package = get_package_share_directory(
        'g02_prii3_nav_turtlebot'
    )

    # Mundo F1L3.
    gazebo_package = get_package_share_directory(
        'f1l3_gazebo'
    )

    # Navigation2 de TurtleBot3.
    nav2_package = get_package_share_directory(
        'turtlebot3_navigation2'
    )

    # Mapa de simulación.
    map_file = os.path.join(
        nav_package,
        'maps',
        'f1l3_mapa.yaml'
    )

    # Parámetros de Navigation2.
    params_file = os.path.join(
        nav2_package,
        'param',
        'humble',
        'waffle.yaml'
    )

    return LaunchDescription([

        # Modelo utilizado en simulación.
        SetEnvironmentVariable(
            'TURTLEBOT3_MODEL',
            'waffle_pi'
        ),

        # Mundo F1L3.
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(
                    gazebo_package,
                    'launch',
                    'f1l3_world.launch.py'
                )
            )
        ),

        # Navigation2 + RViz.
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(
                    nav2_package,
                    'launch',
                    'navigation2.launch.py'
                )
            ),
            launch_arguments={
                'use_sim_time': 'True',
                'map': map_file,
                'params_file': params_file
            }.items()
        ),

        # Detector de ArUcos.
        Node(
            package='g02_prii3_nav_turtlebot',
            executable='aruco_detection',
            output='screen'
        ),

        # Navegación autónoma.
        Node(
            package='g02_prii3_nav_turtlebot',
            executable='autonomous_navigation',
            output='screen'
        ),

    ])