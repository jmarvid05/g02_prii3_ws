from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    return LaunchDescription([

        # Detecta los ArUcos.
        Node(
            package='g02_prii3_nav_jetbot',
            executable='aruco_detection',
            output='screen'
        ),

        # Realiza la navegación autónoma.
        Node(
            package='g02_prii3_nav_jetbot',
            executable='autonomous_navigation',
            output='screen'
        ),

    ])