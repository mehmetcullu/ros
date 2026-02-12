#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
from geometry_msgs.msg import TwistStamped
from sensor_msgs.msg import JointState
from rclpy.time import Time
from rclpy.constants import S_TO_NS

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
        #BURASI
        self.initialized_ = False

        # Publisher ve Subscriber
        self.wheel_cmd_pub_ = self.create_publisher(Float64MultiArray, "simple_velocity_controller/commands", 10)
        self.vel_sub_ = self.create_subscription(TwistStamped, "simple_velocity_controller/cmd_vel", self.velCallback, 10)
        self.joint_sub_ = self.create_subscription(JointState, "joint_states", self.jointCallback, 10)

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

        self.get_logger().info(f"Linear: {linear_vel:.4f}, Angular: {angular_vel:.4f}")

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