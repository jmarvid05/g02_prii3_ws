import math

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data

from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


class CollisionAvoidance(Node):

    def __init__(self):
        super().__init__('collision_avoidance')

        # Permite cambiar el topic del LiDAR sin modificar el codigo
        self.declare_parameter('scan_topic', '/scan')

        scan_topic = (
            self.get_parameter('scan_topic')
            .get_parameter_value()
            .string_value
        )

        # Publicador de velocidad del JetBot
        self.publisher_ = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        # Lectura del LiDAR
        self.subscription = self.create_subscription(
            LaserScan,
            scan_topic,
            self.scan_callback,
            qos_profile_sensor_data
        )

        # Movimiento cada 0.1 segundos
        self.timer = self.create_timer(
            0.1,
            self.move_robot
        )

        # Estados del dibujo del numero 2
        self.estado = 0
        self.contador = 0

        # Distancia a la que detenemos el robot
        self.distancia_seguridad = 0.35

        # False = camino libre
        # True = obstaculo delante
        self.obstaculo = False

        self.get_logger().info(
            'Collision avoidance del JetBot iniciado'
        )

        self.get_logger().info(
            'Esperando LiDAR en: ' + scan_topic
        )

    def scan_callback(self, msg):

        # Miramos 15 grados a cada lado del frente
        angulo_frontal = math.radians(15)

        distancias_frontales = []

        for i, distancia in enumerate(msg.ranges):

            angulo = (
                msg.angle_min
                + i * msg.angle_increment
            )

            # Normalizamos el angulo entre -pi y +pi
            angulo_normalizado = math.atan2(
                math.sin(angulo - math.pi),
                math.cos(angulo - math.pi)
            )

            # Solo analizamos el sector situado delante
            if (
                -angulo_frontal
                <= angulo_normalizado
                <= angulo_frontal
            ):

                if math.isfinite(distancia):
                    distancias_frontales.append(distancia)

        # Si no hay ninguna lectura valida delante,
        # consideramos el camino libre
        if distancias_frontales:
            distancia_minima = min(distancias_frontales)
        else:
            distancia_minima = math.inf

        habia_obstaculo = self.obstaculo

        self.obstaculo = (
            distancia_minima
            < self.distancia_seguridad
        )

        # Mostramos el mensaje solo cuando cambia el estado
        if self.obstaculo and not habia_obstaculo:

            self.get_logger().info(
                'Obstaculo detectado. JetBot detenido.'
            )

        elif not self.obstaculo and habia_obstaculo:

            self.get_logger().info(
                'Obstaculo desaparecido. Reanudando marcha.'
            )

    def move_robot(self):

        msg = Twist()

        # Si hay un obstaculo:
        # velocidad 0 y congelamos la trayectoria
        if self.obstaculo:

            self.publisher_.publish(msg)
            return

        # Estado 0: curva superior
        if self.estado == 0:

            msg.linear.x = 0.12
            msg.angular.z = -0.55

            self.contador += 1

            if self.contador >= 75:
                self.estado = 1
                self.contador = 0

        # Estado 1: diagonal
        elif self.estado == 1:

            msg.linear.x = 0.12
            msg.angular.z = 0.0

            self.contador += 1

            if self.contador >= 35:
                self.estado = 2
                self.contador = 0

        # Estado 2: giro inferior
        elif self.estado == 2:

            msg.linear.x = 0.0
            msg.angular.z = 0.8

            self.contador += 1

            if self.contador >= 34:
                self.estado = 3
                self.contador = 0

        # Estado 3: base
        elif self.estado == 3:

            msg.linear.x = 0.12
            msg.angular.z = 0.0

            self.contador += 1

            if self.contador >= 33:
                self.estado = 4
                self.contador = 0

        # Dibujo terminado
        else:

            msg.linear.x = 0.0
            msg.angular.z = 0.0

        self.publisher_.publish(msg)


def main(args=None):

    rclpy.init(args=args)

    node = CollisionAvoidance()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:

        # Intentamos dejar el robot parado al cerrar el nodo
        stop = Twist()
        node.publisher_.publish(stop)

        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()