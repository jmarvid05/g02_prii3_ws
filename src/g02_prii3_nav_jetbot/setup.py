import os
from glob import glob

from setuptools import find_packages, setup

package_name = 'g02_prii3_nav_jetbot'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name]
        ),
        (
            'share/' + package_name,
            ['package.xml']
        ),
        (
            os.path.join('share', package_name, 'launch'),
            glob('launch/*.py')
        ),
        (
            os.path.join('share', package_name, 'maps'),
            glob('maps/*')
        ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='javiermv',
    maintainer_email='jmarvid@upv.edu.es',
    description='Navegacion y deteccion ArUco para el JetBot real',
    license='MIT',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'aruco_detection = g02_prii3_nav_jetbot.aruco_detection:main',
            'predefined_navigation = g02_prii3_nav_jetbot.predefined_navigation:main',
            'autonomous_navigation = g02_prii3_nav_jetbot.autonomous_navigation:main',
        ],
    },
)