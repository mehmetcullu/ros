#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
from geometry_msgs.msg import TwistStamped, TransformStamped
from sensor_msgs.msg import JointState
from rclpy.time import Time
from rclpy.constants import S_TO_NS
from nav_msgs.msg import Odometry
import math
from tf_transformations import quaternion_from_euler
from tf2_ros import TransformBroadcaster


class SimpleController(Node):
    def __init__(self):
        super().__init__("simple_controller")

        # Parametreler
        self.declare_parameter("wheel_radius", 0.033)
        self.declare_parameter("wheel_separation", 0.17)

        self.wheel_radius = self.get_parameter("wheel_radius").get_parameter_value().double_value
        self.wheel_separation = self.get_parameter("wheel_separation").get_parameter_value().double_value

        self.get_logger().info("Using wheel_radius: %f" % self.wheel_radius)
        self.get_logger().info("Using wheel_separation: %f" % self.wheel_separation)

        # Odometry değişkenleri
        self.right_wheel_prev_pos_ = 0.0
        self.left_wheel_prev_pos_ = 0.0
        self.prev_time_ = self.get_clock().now()
        self.initialized_ = False

        self.x_ = 0.0
        self.y_ = 0.0
        self.theta_ = 0.0

        # Publisher ve Subscriber
        self.wheel_cmd_pub_ = self.create_publisher(Float64MultiArray, "simple_velocity_controller/commands", 10)
        self.vel_sub_ = self.create_subscription(TwistStamped, "simple_velocity_controller/cmd_vel", self.velCallback, 10)
        self.joint_sub_ = self.create_subscription(JointState, "joint_states", self.jointCallback, 10)
        self.odom_pub_ =self.create_publisher(Odometry, "bot_controller/odom", 10)


        self.odom_msg_= Odometry()
        self.odom_msg_.header.frame_id = "odom"
        self.odom_msg_.child_frame_id = "base_footprint"
        self.odom_msg_.pose.pose.orientation.x = 0.0
        self.odom_msg_.pose.pose.orientation.y = 0.0
        self.odom_msg_.pose.pose.orientation.z = 0.0
        self.odom_msg_.pose.pose.orientation.w = 1.0

        self.br_ = TransformBroadcaster(self)
        self.tf_stamped_=TransformStamped()
        self.tf_stamped_.header.frame_id= "odom"
        self.tf_stamped_.child_frame_id= "base_footprint"

    def velCallback(self, msg):
        # Diferansiyel Sürüş Ters Kinematiği (NumPy Olmadan)
        # linear_x: Robotun ileri hızı (v)
        # angular_z: Robotun dönüş hızı (omega)
        v = msg.twist.linear.x
        w = msg.twist.angular.z

        # Tekerlek hızlarını (rad/s) hesapla:
        # Formül: 
        # vr = (2v + w*L) / (2r)
        # vl = (2v - w*L) / (2r)
        
        vr = (2 * v + w * self.wheel_separation) / (2 * self.wheel_radius)
        vl = (2 * v - w * self.wheel_separation) / (2 * self.wheel_radius)

        wheel_speed_msg = Float64MultiArray()
        wheel_speed_msg.data = [float(vr), float(vl)]
        self.wheel_cmd_pub_.publish(wheel_speed_msg)

    def jointCallback(self, msg):
        # 2. Zaman farkı kontrolü
        curr_time = Time.from_msg(msg.header.stamp)
        duration = curr_time - self.prev_time_
        dt = duration.nanoseconds / 1e9 # Doğrudan float bölmesi

        if dt <= 0.0001: # Çok küçük veya sıfır dt'yi engelle
            return

        # 3. Pozisyon farkları
        dp_left = msg.position[1] - self.left_wheel_prev_pos_
        dp_right = msg.position[0] - self.right_wheel_prev_pos_

        # 4. Hız hesaplama (Sen acc demene rağmen bunlar aslında omega/hız)
        omega_left = dp_left / dt
        omega_right = dp_right / dt

        # 5. İleri Kinematik
        linear_vel = (self.wheel_radius * (omega_right + omega_left)) / 2.0
        angular_vel = (self.wheel_radius * (omega_right - omega_left)) / self.wheel_separation

        # Güncellemeler
        self.left_wheel_prev_pos_ = msg.position[1]
        self.right_wheel_prev_pos_ = msg.position[0]
        self.prev_time_ = curr_time

        d_s = (self.wheel_radius * dp_right + self.wheel_radius * dp_left) / 2
        d_theta= (self.wheel_radius * dp_right - self.wheel_radius * dp_left)/ self.wheel_separation
        
        self.theta_ += d_theta
        self.x_ += d_s * math.cos(self.theta_)
        self.y_ += d_s * math.sin(self.theta_)

        q = quaternion_from_euler(0, 0, self.theta_)
        self.odom_msg_.pose.pose.orientation.x = q[0]
        self.odom_msg_.pose.pose.orientation.y = q[1]
        self.odom_msg_.pose.pose.orientation.z = q[2]
        self.odom_msg_.pose.pose.orientation.w = q[3]
        self.odom_msg_.header.stamp= self.get_clock().now().to_msg()
        self.odom_msg_.pose.pose.position.x=self.x_
        self.odom_msg_.pose.pose.position.y=self.y_
        self.odom_msg_.twist.twist.linear.x= linear_vel
        self.odom_msg_.twist.twist.angular.z= angular_vel

        self.tf_stamped_.transform.translation.x= self.x_
        self.tf_stamped_.transform.translation.y= self.y_
        self.tf_stamped_.transform.rotation.x= q[0]
        self.tf_stamped_.transform.rotation.y= q[1]
        self.tf_stamped_.transform.rotation.z= q[2]
        self.tf_stamped_.transform.rotation.w= q[3]
        self.tf_stamped_.header.stamp= self.get_clock().now().to_msg()        

        self.get_logger().info(f"Linear: {linear_vel:.4f}, Angular: {angular_vel:.4f}")
        self.get_logger().info(f"x: {self.x_:.4f}, y: {self.y_:.4f}, theta: {self.theta_:.4f}")
        
        self.odom_pub_.publish(self.odom_msg_)
        self.br_.sendTransform(self.tf_stamped_)

def main():
    rclpy.init()
    simple_controller=SimpleController()
    try:
        rclpy.spin(simple_controller)
    except KeyboardInterrupt:
        pass
    finally:
        simple_controller.destroy_node()
        rclpy.shutdown()

if __name__=='__main__':
    main()