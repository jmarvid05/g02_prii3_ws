from setuptools import find_packages, setup

package_name = 'g02_prii3_move_turtlebot'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/draw_number.launch.py','launch/draw_number_jetbot.launch.py']),
        ('share/' + package_name + '/config', ['config/draw_number.rviz']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='javiermv',
    maintainer_email='jmarvid@upv.edu.es',
    description='Movimiento autonomo del TurtleBot3',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'draw_number = g02_prii3_move_turtlebot.draw_number:main',
            'draw_number_jetbot = g02_prii3_move_turtlebot.draw_number_jetbot:main',
            'trail_node = g02_prii3_move_turtlebot.trail_node:main',
        ],
    },
)
