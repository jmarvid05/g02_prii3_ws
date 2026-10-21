import math

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data

from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


class CollisionAvoidance(Node):

    def __init__(self):
        super().__init__('collision_avoidance')

        # Publicador de velocidad
        self.publisher_ = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        # Suscriptor al LiDAR
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            qos_profile_sensor_data
        )

        # Timer para ejecutar el movimiento cada 0.1 s
        self.timer = self.create_timer(
            0.1,
            self.move_robot
        )

        # Estados del dibujo del numero 2
        self.estado = 0
        self.contador = 0

        # Distancia minima a partir de la cual paramos
        self.distancia_seguridad = 0.45

        # Indica si hay un obstaculo delante
        self.obstaculo = False

        self.get_logger().info(
            'Collision avoidance iniciado'
        )

    def scan_callback(self, msg):

        # Angulo frontal que queremos comprobar
        angulo_frontal = math.radians(15)

        distancias_frontales = []

        for i, distancia in enumerate(msg.ranges):

            angulo = msg.angle_min + i * msg.angle_increment

            # Convertimos cualquier angulo a un valor entre -pi y +pi.
            angulo_normalizado = math.atan2(
            math.sin(angulo),
            math.cos(angulo)
        )

        # Solo utilizamos las medidas situadas delante del robot.
        if -angulo_frontal <= angulo_normalizado <= angulo_frontal:

            if math.isfinite(distancia):
                distancias_frontales.append(distancia)

        if distancias_frontales:
            distancia_minima = min(distancias_frontales)
        else:
            distancia_minima = math.inf

        habia_obstaculo = self.obstaculo

        self.obstaculo = (
            distancia_minima < self.distancia_seguridad
        )

        if self.obstaculo and not habia_obstaculo:
            self.get_logger().info(
                'Obstaculo detectado. Robot detenido.'
            )

        elif not self.obstaculo and habia_obstaculo:
            self.get_logger().info(
                'Obstaculo desaparecido. Reanudando marcha.'
            )

    def move_robot(self):

        msg = Twist()

        # Si hay obstaculo no avanzamos ni incrementamos
        # el contador de la trayectoria.
        if self.obstaculo:
            self.publisher_.publish(msg)
            return

        # Estado 0: primera curva del numero 2
        if self.estado == 0:

            msg.linear.x = 0.12
            msg.angular.z = -0.55

            self.contador += 1

            if self.contador >= 70:
                self.estado = 1
                self.contador = 0

        # Estado 1: diagonal
        elif self.estado == 1:

            msg.linear.x = 0.12
            msg.angular.z = 0.0

            self.contador += 1

            if self.contador >= 55:
                self.estado = 2
                self.contador = 0

        # Estado 2: giro hacia la izquierda
        elif self.estado == 2:

            msg.linear.x = 0.0
            msg.angular.z = 0.8

            self.contador += 1

            if self.contador >= 28:
                self.estado = 3
                self.contador = 0

        # Estado 3: base del numero 2
        elif self.estado == 3:

            msg.linear.x = 0.12
            msg.angular.z = 0.0

            self.contador += 1

            if self.contador >= 40:
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
        stop = Twist()
        node.publisher_.publish(stop)

        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()