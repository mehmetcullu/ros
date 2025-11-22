from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare
import os

def generate_launch_description():

    # Paket yolunu dinamik olarak al
    package_path = FindPackageShare('bot_description')
    
    # Varsayılan URDF yolunu paket dizinine göre ayarla
    default_urdf_path = PathJoinSubstitution([
        package_path, 'urdf', 'bot.urdf'
    ])

    # URDF dosyasının yolunu tanımla
    model_arg = DeclareLaunchArgument(
        name="model",
        default_value=default_urdf_path,
        description="Absolute path to robot URDF/XACRO file"
    )

    # xacro/urdf dosyasını robot_description parametresine dönüştür
    robot_description = ParameterValue(
        Command([
            'xacro ',
            LaunchConfiguration("model")
        ]),
        value_type=str
    )

    # Robot State Publisher düğümü
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description}]
    )

    # Joint State Publisher GUI düğümü
    joint_state_publisher_gui = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
    )

    # RViz düğümü
    rviz_config_path = PathJoinSubstitution([
        package_path, 'rviz_model', 'display.rviz'
    ])
    
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", rviz_config_path]
    )

    return LaunchDescription([
        model_arg,
        robot_state_publisher,
        joint_state_publisher_gui,
        rviz_node
    ])