import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class DrawNumber(Node):

    def __init__(self):
        super().__init__('draw_number')

        self.publisher_ = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        self.timer = self.create_timer(
            0.1,
            self.move_robot
        )

        self.estado = 0
        self.contador = 0

    def move_robot(self):
        msg = Twist()

        # ESTADO 0: curva
        if self.estado == 0:
            msg.linear.x = 0.12
            msg.angular.z = -0.55

            self.contador += 1

            if self.contador >= 70:
                self.estado = 1
                self.contador = 0

        # ESTADO 1: diagonal recta
        elif self.estado == 1:
            msg.linear.x = 0.12
            msg.angular.z = 0.0

            self.contador += 1

            if self.contador >= 55:
                self.estado = 2
                self.contador = 0

        # ESTADO 2: giro a la izquierda
        elif self.estado == 2:
            msg.linear.x = 0.0
            msg.angular.z = 0.8

            self.contador += 1

            if self.contador >= 28:
                self.estado = 3
                self.contador = 0

        # ESTADO 3: base recta
        elif self.estado == 3:
            msg.linear.x = 0.12
            msg.angular.z = 0.0

            self.contador += 1

            if self.contador >= 40:
                self.estado = 4
                self.contador = 0

        # ESTADO 4: parar
        else:
            msg.linear.x = 0.0
            msg.angular.z = 0.0

        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)

    node = DrawNumber()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()