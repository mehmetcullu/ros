import rclpy
from rclpy.node import Node
from tf2_ros.static_transform_broadcaster import StaticTransformBroadcaster
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped


class TFKinematic(Node):
    def __init__(self):
        super().__init__("tf_kinematics")

        self.static_broadcaster_ = StaticTransformBroadcaster(self)
        self.dynamic_tf_broadcaster_= TransformBroadcaster(self)

        self.static_transform_stamped_ = TransformStamped()
        self.dynamic_transform_stamped_ = TransformStamped()
        self.static_transform_stamped_.header.stamp = self.get_clock().now().to_msg()
        self.static_transform_stamped_.header.frame_id = "bot_base"
        self.static_transform_stamped_.child_frame_id = "bot_top"
        self.static_transform_stamped_.transform.translation.x = 0.0
        self.static_transform_stamped_.transform.translation.y = 0.0
        self.static_transform_stamped_.transform.translation.z = 0.3
        self.static_transform_stamped_.transform.rotation.x = 0.0
        self.static_transform_stamped_.transform.rotation.y = 0.0
        self.static_transform_stamped_.transform.rotation.z = 0.0
        self.static_transform_stamped_.transform.rotation.w = 1.0

        self.static_broadcaster_.sendTransform(self.static_transform_stamped_)
        

        self.get_logger().info("Publishing static transform between %s and %s" % 
                               (self.static_transform_stamped_.header.frame_id, self.static_transform_stamped_.child_frame_id))
        
        #0.1 sn sıklığında publishler
        self.timer_ = self.create_timer(0.1, self.timerCallBack)


        #odom bot_basei simültane değiştiriyor bu da static botbasei yukarıda etkiliyor. Whose parent of bot_top
        def timerCallBack():
            self.static_transform_stamped_.header.stamp = self.get_clock().now().to_msg()
            self.static_transform_stamped_.header.frame_id = "odom"
            self.static_transform_stamped_.child_frame_id = "bot_base"
            self.static_transform_stamped_.transform.translation.x = 0.0
            self.static_transform_stamped_.transform.translation.y = 0.0
            self.static_transform_stamped_.transform.translation.z = 0.3
            self.static_transform_stamped_.transform.rotation.x = 0.0
            self.static_transform_stamped_.transform.rotation.y = 0.0
            self.static_transform_stamped_.transform.rotation.z = 0.0
            self.static_transform_stamped_.transform.rotation.w = 1.0

            self.dynamic_tf_broadcaster_.sendTransform(self.static_transform_stamped_)

def main():
    rclpy.init()
    simple_tf_kinematics = TFKinematic()
    rclpy.spin(simple_tf_kinematics)
    simple_tf_kinematics.destroy_node()
    rclpy.shutdown()

if __name__== '__main__':
    main()