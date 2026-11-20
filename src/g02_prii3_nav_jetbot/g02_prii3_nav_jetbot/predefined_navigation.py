import rclpy

from rclpy.node import Node
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose


class PredefinedNavigation(Node):

    def __init__(self):
        super().__init__('predefined_navigation')

        # Cliente para mandar destinos a Nav2.
        self.client = ActionClient(
            self,
            NavigateToPose,
            'navigate_to_pose'
        )

        # Destino real.
        # Lo cambiaremos en clase con las coordenadas del mapa real.
        self.x = 0.0
        self.y = 0.0

        self.enviar_destino()


    def enviar_destino(self):

        # Esperamos a que Nav2 esté preparado.
        self.client.wait_for_server()

        # Creamos el destino.
        goal = NavigateToPose.Goal()

        goal.pose.header.frame_id = 'map'

        goal.pose.pose.position.x = self.x
        goal.pose.pose.position.y = self.y

        goal.pose.pose.orientation.w = 1.0

        self.get_logger().info(
            f'Destino: X={self.x}, Y={self.y}'
        )

        # Enviamos el destino a Nav2.
        self.client.send_goal_async(goal)


def main(args=None):

    rclpy.init(args=args)

    node = PredefinedNavigation()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()