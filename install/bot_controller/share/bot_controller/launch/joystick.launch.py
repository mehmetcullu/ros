from launch import LaunchDescription
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    stick_node = Node(
        package= "joy",
        executable= "joy_node",
        name= "stick",
        parameters=[os.path.join(get_package_share_directory("bot_controller"), "config", "stick_config.yaml")]
    )

    stick_teleop= Node(
        package= "joy_teleop",
        executable= "joy_teleop",
        name="stick_teleop",
        parameters=[os.path.join(get_package_share_directory("bot_controller"), "config", "stick_teleop.yaml")]
    )

    return LaunchDescription([
        stick_node,
        stick_teleop
    ])