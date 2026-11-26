"""Sprint 4 en el tablero real: camara USB + ArUcos.

Por seguridad, el recorrido se activa solo con mover_robot:=true.
Antes de activarlo, el robot real debe tener Nav2, odometria y TF map->odom
configurados correctamente para el tablero Eurobot.
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('dispositivo', default_value='/dev/video0'),
        DeclareLaunchArgument('mover_robot', default_value='false'),

        # Camara cenital USB conectada al ordenador.
        Node(
            package='v4l2_camera',
            executable='v4l2_camera_node',
            name='camara_cenital',
            output='screen',
            parameters=[{'video_device': LaunchConfiguration('dispositivo')}],
            remappings=[('/image_raw', '/overhead_camera/image_raw')],
        ),

        # Tu detector actual se suscribe a /camera/image_raw.
        Node(
            package='eurobot_gazebo',
            executable='detectar_arucos',
            name='detectar_arucos',
            output='screen',
            parameters=[{'use_sim_time': False}],
            remappings=[('/camera/image_raw', '/overhead_camera/image_raw')],
        ),

        # Opcional: requiere que Nav2 del robot REAL ya este funcionando.
        Node(
            package='eurobot_gazebo',
            executable='recorrer_arucos',
            name='recorrer_arucos',
            output='screen',
            parameters=[{'use_sim_time': False}],
            condition=IfCondition(LaunchConfiguration('mover_robot')),
        ),
    ])
