
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():

    # Arranque del JetBot real.
    jetbot_launch = os.path.join(
        get_package_share_directory('jetbot_pro_ros2'),
        'launch',
        'jetbot.py'
    )

    # Arranque de Navigation2.
    nav2_launch = os.path.join(
        get_package_share_directory('nav2_bringup'),
        'launch',
        'bringup_launch.py'
    )

    # Parametros de navegacion del JetBot.
    param_file = LaunchConfiguration(
        'params_file',
        default=os.path.join(
            get_package_share_directory('jetbot_pro_ros2'),
            'param',
            'nav.yaml'
        )
    )

    # Mapa real F1L3 del repositorio.
    map_file = os.path.join(
        get_package_share_directory('g02_prii3_nav_jetbot'),
        'maps',
        'map.yaml'
    )

    return LaunchDescription([

        # 1. Arrancar el JetBot.
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(jetbot_launch)
        ),

        # 2. Arrancar Nav2 sin activacion automatica.
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(nav2_launch),
            launch_arguments={
                'map': map_file,
                'use_sim_time': 'False',
                'autostart': 'False',
                'params_file': param_file,
            }.items()
        ),

        # 3. Gestionar automaticamente la activacion de Nav2.
        Node(
            package='g02_prii3_nav_jetbot',
            executable='nav2_auto_start',
            output='screen'
        ),

    ])

