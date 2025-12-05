from setuptools import find_packages, setup

package_name = 'ros_python'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='murtazam',
    maintainer_email='murtazam@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'publisher = ros_python.publisher:main',
            'subscriber = ros_python.subscriber:main',
            'parameter = ros_python.parameter:main',
            'turtlesim_kinematics = ros_python.turtlesim_kinematics:main'
        ],
    },
)
