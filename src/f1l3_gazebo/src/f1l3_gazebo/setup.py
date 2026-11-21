import os

from glob import glob
from setuptools import setup


package_name = 'f1l3_gazebo'


# Añade todos los archivos de una carpeta al paquete.
def package_files(directory):

    paths = []

    for path, directories, filenames in os.walk(directory):

        files = []

        for filename in filenames:
            files.append(
                os.path.join(path, filename)
            )

        if files:
            paths.append(
                (
                    os.path.join('share', package_name, path),
                    files
                )
            )

    return paths


data_files = [
    (
        'share/ament_index/resource_index/packages',
        ['resource/' + package_name]
    ),
    (
        'share/' + package_name,
        ['package.xml']
    ),
    (
        os.path.join('share', package_name, 'worlds'),
        glob('worlds/*.world')
    ),
    (
        os.path.join('share', package_name, 'launch'),
        glob('launch/*.py')
    ),
]

# Instala los modelos ArUco.
data_files += package_files('models')


setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=data_files,
    install_requires=['setuptools'],
    zip_safe=True,
    description='Custom F1L3 world for Gazebo simulation with TurtleBot3',
    license='Apache License 2.0',
    tests_require=['pytest'],
)