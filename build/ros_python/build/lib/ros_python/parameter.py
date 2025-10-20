import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import SetParametersResult
from rclpy.parameter import Parameter

class Parameters(Node):
    def __init__(self):
        super().__init__("parameter")

        self.declare_parameter("int_param", 28)
        self.declare_parameter("string_param", "Memo")
        self.add_on_set_parameters_callback(self.paramChangeCallback)
    
    def paramChangeCallback(self, params):
        result=SetParametersResult()

        for param in params:
            if param.name=="int_param" and param.type_==Parameter.Type.INTEGER:
                self.get_logger().info("Param changed to %d" % param.value)
                result.successful=True
            
            if param.name=="string_param" and param.type_==Parameter.Type.STRING:
                self.get_logger().info("Param changed to %s" % param.value)
                result.successful=True
        return result
    
def main():
    rclpy.init()
    parameter=Parameters()
    rclpy.spin(parameter)
    
    parameter.destroy_node
    rclpy.shutdown()

if __name__=='__main__':
    main()

