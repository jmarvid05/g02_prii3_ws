import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_srvs.srv import Trigger


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
        self.pausado = False

        self.create_service(
            Trigger,
            'detener_dibujo',
            self.detener_dibujo
        )

        self.create_service(
            Trigger,
            'reanudar_dibujo',
            self.reanudar_dibujo
        )

        self.create_service(
            Trigger,
            'reiniciar_dibujo',
            self.reiniciar_dibujo
        )

    def detener_dibujo(self, request, response):
        self.pausado = True

        msg = Twist()
        self.publisher_.publish(msg)

        self.get_logger().info('Dibujo detenido')

        response.success = True
        response.message = 'Dibujo detenido'

        return response

    def reanudar_dibujo(self, request, response):
        self.pausado = False

        self.get_logger().info('Dibujo reanudado')

        response.success = True
        response.message = 'Dibujo reanudado'

        return response

    def reiniciar_dibujo(self, request, response):
        self.estado = 0
        self.contador = 0
        self.pausado = False

        msg = Twist()
        self.publisher_.publish(msg)

        self.get_logger().info('Dibujo reiniciado')

        response.success = True
        response.message = 'Dibujo reiniciado'

        return response

    def move_robot(self):
        msg = Twist()

        # Si el dibujo esta detenido, el robot permanece parado
        if self.pausado:
            self.publisher_.publish(msg)
            return

        # ESTADO 0: curva
        if self.estado == 0:
            msg.linear.x = 0.12
            msg.angular.z = -0.55

            self.contador += 1

            if self.contador >= 75:
                self.estado = 1
                self.contador = 0

        # ESTADO 1: diagonal recta
        elif self.estado == 1:
            msg.linear.x = 0.12
            msg.angular.z = 0.0

            self.contador += 1

            if self.contador >= 35:
                self.estado = 2
                self.contador = 0

        # ESTADO 2: giro a la izquierda
        elif self.estado == 2:
            msg.linear.x = 0.0
            msg.angular.z = 0.8

            self.contador += 1

            if self.contador >= 34:
                self.estado = 3
                self.contador = 0

        # ESTADO 3: base recta
        elif self.estado == 3:
            msg.linear.x = 0.12
            msg.angular.z = 0.0

            self.contador += 1

            if self.contador >= 33:
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
