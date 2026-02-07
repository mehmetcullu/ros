import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
from geometry_msgs.msg import TwistStamped
from sensor_msgs.msg import JointState
import numpy as np
from rclpy.time import Time
from rclpy.constants import S_TO_NS

class SimpleController(Node):
    def __init__(self):
        super().__init__("simple_controller")

        self.declare_parameter("wheel_radius", 0.033)
        self.declare_parameter("wheel_separation", 0.17)

        self.wheel_radius= self.get_parameter("wheel_radius").get_parameter_value.double_value
        self.wheel_seperation= self.get_parameter("wheel_seperation").get_parameter_value.double_value

        self.get_logger().info("Using wheel_radius %f" % self.wheel_radius)
        self.get_logger().info("Using wheel_seperation %f" % self.wheel_seperation)

        #Odometry için Velocity ve Angular Velocity için Last ve Previous için gerekli
        self.right_wheel_prev_pos_ = 0.0
        self.left_wheel_prev_pos_ = 0.0

        self.prev_time_ = self.get_clock().now()

        self.wheel_cmd_pub_ =self.create_publisher(Float64MultiArray, "simple_velocity_controller/commands", 10)
        self.vel_sub_ =self.create_subscription(TwistStamped, "simple_velocity_controller/cmd_vel", self.velCallback,10)

        #Gazebo veya encoderlardan gelecek verileri dinleyecek subscription
        self.joint_sub_ = self.create_subscription(JointState, "joint_states", self.jointCallback, 10)

        self.speed_conversion_= np.array(
            [self.wheel_radius/2, self.wheel_radius/2],
            [self.wheel_radius/self.wheel_seperation, self.wheel_radius/self.wheel_seperation]
            )
        self.get_logger().info("The conversation matrix is %f" % self.speed_conversion_)



    def velCallback(self, msg):
        robot_speed=np.array([msg.twist.lineer.x],
                             [msg.twist.angular.z])
        
        wheel_speed= np.matmul(np.linalg.inv(self.speed_conversion_), robot_speed)
        wheel_speed_msg=Float64MultiArray()
        wheel_speed_msg.data=[wheel_speed[1,0], wheel_speed[0,0]]
        self.wheel_cmd_pub_.publish(wheel_speed_msg)

    #hız farkı/ zaman farkı ,
    def jointCallback(self, msg):
        dp_left_ = msg.position[1] - self.left_wheel_prev_pos_
        dp_right_ = msg.position[0] - self.right_wheel_prev_pos_
        dt = Time.from_msg(msg.header.stamp) - self.prev_time_

        #Update new positions
        self.left_wheel_prev_pos_ = msg.position[1]
        self.right_wheel_prev_pos_ = msg.position[0]
        self.prev_time_ = Time.from_msg(msg.header.stamp)

        acc_left =dp_left_ / (dt.nanoseconds / S_TO_NS)
        acc_right =dp_right_ / (dt.nanoseconds / S_TO_NS)

        #calculate linear and angular velocity
        linear_vel= (self.wheel_radius * acc_right + self.wheel_radius * acc_left) / 2 
        angular_vel= (self.wheel_radius * acc_right + self.wheel_radius * acc_left) / self.wheel_seperation

        self.get_logger().info("Linear velocity: %s \n Angular velocity: %s" % (linear_vel, angular_vel))

def main():
    rclpy.init()
    simple_controller=SimpleController()
    rclpy.spin(simple_controller)
    simple_controller.destroy_node()
    rclpy.shutdown

if __name__=='__main__':
    main()