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

        # Coordenadas finales.
        self.x = 3.65
        self.y = -0.37

        self.enviar_destino()


    def enviar_destino(self):

        # Esperamos a que Nav2 esté preparado.
        self.client.wait_for_server()

        # Creamos el destino.
        goal = NavigateToPose.Goal()

        goal.pose.header.frame_id = 'map'

        goal.pose.pose.position.x = self.x
        goal.pose.pose.position.y = self.y

        # Orientación final.
        goal.pose.pose.orientation.w = 1.0

        self.get_logger().info(
            f'Destino: X={self.x}, Y={self.y}'
        )

        # Mandamos el destino a Nav2.
        self.client.send_goal_async(goal)


def main(args=None):

    rclpy.init(args=args)

    node = PredefinedNavigation()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()