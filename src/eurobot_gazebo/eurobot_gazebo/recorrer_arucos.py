import rclpy

from rclpy.node import Node
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose


class RecorrerArucos(Node):

    def __init__(self):
        super().__init__('recorrer_arucos')

        # Cliente para mandar destinos a Nav2.
        self.client = ActionClient(
            self,
            NavigateToPose,
            'navigate_to_pose'
        )

        # ArUco 20
        self.x1 = 0.6
        self.y1 = 1.4

        # ArUco 21
        self.x2 = 2.4
        self.y2 = 1.4

        # ArUco 22
        self.x3 = 0.6
        self.y3 = 0.6

        # ArUco 23
        self.x4 = 2.4
        self.y4 = 0.6

        # Centro
        self.x5 = 1.5
        self.y5 = 1.0

        self.destinos = [
            (self.x1, self.y1),
            (self.x2, self.y2),
            (self.x3, self.y3),
            (self.x4, self.y4),
            (self.x5, self.y5)
        ]

    def enviar_destino(self):
        self.client.wait_for_server()

        for x, y in self.destinos:
            goal = NavigateToPose.Goal()
            goal.pose.header.frame_id = 'map'
            goal.pose.header.stamp = self.get_clock().now().to_msg()
            goal.pose.pose.position.x = x
            goal.pose.pose.position.y = y
            goal.pose.pose.orientation.w = 1.0

            futuro = self.client.send_goal_async(goal)
            rclpy.spin_until_future_complete(self, futuro)

            handle = futuro.result()
            if not handle.accepted:
                break

            resultado = handle.get_result_async()
            rclpy.spin_until_future_complete(self, resultado)

            if resultado.result().status != 4:
                break

            print(f'Destino alcanzado: {x}, {y}')


def main(args=None):

    rclpy.init(args=args)

    node = RecorrerArucos()

    node.enviar_destino()

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()