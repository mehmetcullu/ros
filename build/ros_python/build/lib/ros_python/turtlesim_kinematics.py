import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose

class TurtlesimKinematics(Node):
    def __init__(self):
        super().__init__("turtle_sim_kinematics")

        self.turtle1_pose_sub_ = self.create_subscription(Pose, "/turtle1/pose", self.turtle1PoseCallback, 10)
        self.turtle2_pose_sub_ = self.create_subscription(Pose, "/turtle2/pose", self.turtle2PoseCallback, 10)

        self.last_turtle1_pose_= Pose()
        self.last_turtle2_pose_= Pose()
    
    def turtle1PoseCallback(self, msg):
        self.last_turtle1_pose_=msg

    def turtle2PoseCallback(self, msg):
        self.last_turtle2_pose_=msg    

        Tx=self.last_turtle2_pose_.x - self.last_turtle1_pose_.x
        Ty=self.last_turtle2_pose_.y - self.last_turtle1_pose_.y

        self.get_logger().info("""\n
                                    Translation Vector turtle1 -> turtle2\n
                                    Tx: %f \n
                                    Ty: %f \n""" % (Tx,Ty))

def main():
    rclpy.init()
    turtle_sim_kinematics=TurtlesimKinematics()
    rclpy.spin(turtle_sim_kinematics)
    turtle_sim_kinematics.destroynode()
    rclpy.shutdown()

if __name__=='__main__':
    main()