from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    # Paths to the launch files
    jetbot_launch = os.path.join(
        get_package_share_directory('jetbot_pro_ros2'),
        'launch',
        'jetbot.py'
    )
    nav2_launch = os.path.join(
        get_package_share_directory('nav2_bringup'),
        'launch',
        'bringup_launch.py',
    )

    param_file = LaunchConfiguration(
        'params_file',
        default=os.path.join(
            get_package_share_directory('jetbot_pro_ros2'),
            'param',
            'nav.yaml'))       

    # map_file = '/home/jetbot/ros2_ws/jetbot_pro_ros2/map.yaml'
    # map_file = '/home/jetbot/ros2_ws/jetbot_pro_ros2/map_f1l3.yaml'
    map_file = '/home/jetbot/map.yaml'

    return LaunchDescription([
        IncludeLaunchDescription(PythonLaunchDescriptionSource(jetbot_launch)),
        IncludeLaunchDescription(PythonLaunchDescriptionSource(nav2_launch),
            launch_arguments={
                'map': map_file,
                'use_sim_time': 'False',
                'autostart': 'False',
                'params_file': param_file,
                # 'log_level': "debug"
                }.items()),
    ])

