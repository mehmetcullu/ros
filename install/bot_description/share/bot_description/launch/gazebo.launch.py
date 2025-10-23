from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable, IncludeLaunchDescription
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.parameter_descriptions import ParameterValue
from ament_index_python.packages import get_package_share_directory
from pathlib import Path
import os

def generate_launch_description():

    # Paket yolunu al
    package_path = get_package_share_directory('bot_description')
    
    # Varsayılan URDF yolunu paket dizinine göre ayarla
    default_urdf_path = os.path.join(package_path, 'urdf', 'bot.urdf')

    # URDF dosyasının yolunu tanımla
    model_arg = DeclareLaunchArgument(
        name="model",
        default_value=default_urdf_path,
        description="Absolute path to robot URDF/XACRO file"
    )

    # xacro/urdf dosyasını robot_description parametresine dönüştür
    robot_description = ParameterValue(
        Command(['xacro ', LaunchConfiguration("model")]),
        value_type=str
    )

    # Robot State Publisher düğümü
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description}]
    )

    # Gazebo kaynak yolu
    gazebo_resource_path = SetEnvironmentVariable(
        name="GZ_SIM_RESOURCE_PATH",
        value=[str(Path(package_path).parent.resolve())]
    )

    # Gazebo'yu başlat
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("ros_gz_sim"),
                "launch",
                "gz_sim.launch.py"
            )
        ),
        launch_arguments=[("gz_args", [" -v 4", " -r", " empty.sdf"])]
    )
    
    # Robotu spawn et
    gz_spawn_entity = Node(
        package="ros_gz_sim",
        executable="create",
        output="screen",
        arguments=["-topic", "robot_description", "-name", "bot"]
    )

    return LaunchDescription([
        model_arg,
        robot_state_publisher,
        gazebo_resource_path,
        gazebo,
        gz_spawn_entity
    ])