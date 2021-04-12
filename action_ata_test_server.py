import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node

from action_ata_test.action import Test

aforo = 30

class TestActionServer(Node):

    def __init__(self):
        super().__init__('test_action_server')
        self._action_server = ActionServer(
            self,
            Test,
            'test',
            self.execute_callback)

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')
        
        feedback_msg = Test.Feedback()
        
        result = Test.Result()
        
        global aforo;
        
        if(goal_handle.request.new_customers > 0):
        	if((aforo - goal_handle.request.new_customers) >= 0):
        		aforo = aforo - goal_handle.request.new_customers
        		feedback_msg = "EL aforo disponible ahora es de "+str(aforo)
        		result.msg_final = "Hay espacio y se va a proceder a acompañar a los clientes a su mesa"
        		result.aforo_disponible = aforo
        	else:
        		feedback_msg = "EL aforo disponible ahora es de "+str(aforo)
        		result.msg_final = "No hay espacio"
        		result.aforo_disponible = aforo
        		
        elif(goal_handle.request.old_customers > 0):
        	if((aforo + goal_handle.request.old_customers) <= 30):
        		aforo = aforo + goal_handle.request.old_customers
        		feedback_msg = "EL aforo disponible ahora es de "+str(aforo)
        		result.msg_final = "Se han marchado clientes y hay más espacio"
        		result.aforo_disponible = aforo
        	else:
        		feedback_msg = "EL aforo disponible ahora es de "+str(aforo)
        		result.msg_final = "No hay clientes ocupando espacio, por lo que no es posible que se levante nadie"
        		result.aforo_disponible = aforo
        	
        else:
        	feedback_msg = "No se ha introducido un valor valido"
        	goal_handle.publish_feedback(feedback_msg)
        
        goal_handle.succeed()
        
        return result


def main(args=None):
    rclpy.init(args=args)

    test_action_server = TestActionServer()

    rclpy.spin(test_action_server)


if __name__ == '__main__':
    main()

