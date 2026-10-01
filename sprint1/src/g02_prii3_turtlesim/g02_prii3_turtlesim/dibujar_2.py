import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from std_srvs.srv import Trigger, Empty


class DibujarDos(Node):

    def __init__(self):
        super().__init__('dibujar_2')

        self.publisher_ = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel',
            10
        )

        self.create_service(
            Trigger,
            '/detener_dibujo',
            self.detener_callback
        )

        self.create_service(
            Trigger,
            '/reanudar_dibujo',
            self.reanudar_callback
        )

        self.create_service(
            Trigger,
            '/reiniciar_dibujo',
            self.reiniciar_callback
        )

        self.reset_client = self.create_client(
            Empty,
            '/reset'
        )

        self.periodo = 0.05

        self.acciones = [
            # Línea superior hacia la derecha
            (1.0, 0.0, 2.0),

            # Curva superior derecha
            (1.0, -1.0, 1.57),

            # Orientarse hacia abajo y a la izquierda
            (0.0, -1.0, 0.78),

            # Diagonal del 2
            (1.0, 0.0, 4.0),

            # Girar para quedar mirando a la derecha
            (0.0, 1.0, 2.35),

            # Línea inferior
            (1.0, 0.0, 2.5)
        ]

        self.accion_actual = 0
        self.tiempo_accion = 0.0
        self.pausado = False
        self.finalizado = False

        self.timer = self.create_timer(
            self.periodo,
            self.control
        )

        self.get_logger().info('Nodo para dibujar el numero 2 iniciado')


    def control(self):

        mensaje = Twist()

        if self.pausado or self.finalizado:
            self.publisher_.publish(mensaje)
            return

        if self.publisher_.get_subscription_count() == 0:
            self.publisher_.publish(mensaje)
            return

        lineal, angular, duracion = self.acciones[self.accion_actual]

        mensaje.linear.x = lineal
        mensaje.angular.z = angular

        self.publisher_.publish(mensaje)

        self.tiempo_accion += self.periodo

        if self.tiempo_accion >= duracion:

            self.accion_actual += 1
            self.tiempo_accion = 0.0

            if self.accion_actual >= len(self.acciones):

                self.finalizado = True

                self.publisher_.publish(Twist())

                self.get_logger().info(
                    'Dibujo del numero 2 finalizado'
                )


    def detener_callback(self, request, response):

        self.pausado = True

        self.publisher_.publish(Twist())

        response.success = True
        response.message = 'Dibujo detenido'

        return response


    def reanudar_callback(self, request, response):

        if self.finalizado:
            response.success = False
            response.message = 'El dibujo ya ha terminado'
            return response

        self.pausado = False

        response.success = True
        response.message = 'Dibujo reanudado'

        return response


    def reiniciar_callback(self, request, response):

        self.pausado = True

        self.publisher_.publish(Twist())

        if not self.reset_client.wait_for_service(timeout_sec=1.0):

            response.success = False
            response.message = 'No se encuentra el servicio /reset'

            return response

        peticion = Empty.Request()

        futuro = self.reset_client.call_async(peticion)

        futuro.add_done_callback(self.reset_terminado)

        response.success = True
        response.message = 'Reinicio solicitado'

        return response


    def reset_terminado(self, future):

        try:
            future.result()

            self.accion_actual = 0
            self.tiempo_accion = 0.0
            self.pausado = False
            self.finalizado = False

            self.get_logger().info(
                'Dibujo reiniciado'
            )

        except Exception as error:

            self.get_logger().error(
                'Error al reiniciar: %s' % str(error)
            )


def main(args=None):

    rclpy.init(args=args)

    nodo = DibujarDos()

    try:
        rclpy.spin(nodo)

    except KeyboardInterrupt:
        pass

    nodo.publisher_.publish(Twist())

    nodo.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
