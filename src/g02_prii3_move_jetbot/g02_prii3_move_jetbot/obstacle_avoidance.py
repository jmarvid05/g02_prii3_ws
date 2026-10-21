import math

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data

from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


class ObstacleAvoidance(Node):

    def __init__(self):
        super().__init__('obstacle_avoidance')

        # Topic del LiDAR.
        # Lo dejamos configurable porque tenemos que comprobar
        # el nombre exacto cuando usemos el JetBot real.
        self.declare_parameter('scan_topic', '/scan')

        scan_topic = (
            self.get_parameter('scan_topic')
            .get_parameter_value()
            .string_value
        )

        # Publicador de movimiento
        self.publisher_ = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        # Suscriptor al LiDAR
        self.subscription = self.create_subscription(
            LaserScan,
            scan_topic,
            self.scan_callback,
            qos_profile_sensor_data
        )

        # Ejecutamos el movimiento cada 0.1 segundos
        self.timer = self.create_timer(
            0.1,
            self.move_robot
        )

        # =====================================================
        # DIBUJO DEL NUMERO 2
        # =====================================================

        self.estado = 0
        self.contador = 0

        # =====================================================
        # DATOS DEL LIDAR
        # =====================================================

        self.distancia_frente = math.inf
        self.distancia_izquierda = math.inf
        self.distancia_derecha = math.inf

        # Cuando haya algo a menos de 50 cm delante,
        # comenzamos la esquiva.
        self.distancia_deteccion = 0.50

        # =====================================================
        # CONTROL DE LA ESQUIVA
        # =====================================================

        self.esquivando = False

        # 1 = izquierda
        # -1 = derecha
        self.direccion_esquiva = 0

        self.fase_esquiva = 'GIRO_SALIDA'

        self.contador_esquiva = 0

        # Valores iniciales.
        # Tendremos que comprobarlos fisicamente en el JetBot.
        self.ciclos_giro = 15
        self.ciclos_avance = 25

        self.get_logger().info(
            'Obstacle avoidance del JetBot iniciado'
        )

        self.get_logger().info(
            'Esperando LiDAR en: ' + scan_topic
        )

    def distancia_sector(self, msg, angulo_min, angulo_max):

        distancias = []

        for i, distancia in enumerate(msg.ranges):

            angulo = (
                msg.angle_min
                + i * msg.angle_increment
            )

            # Normalizamos el angulo entre -pi y +pi
            angulo = math.atan2(
                math.sin(angulo),
                math.cos(angulo)
            )

            if angulo_min <= angulo <= angulo_max:

                if math.isfinite(distancia):
                    distancias.append(distancia)

        if distancias:
            return min(distancias)

        return math.inf

    def scan_callback(self, msg):

        # Sector frontal: -20 a +20 grados
        self.distancia_frente = self.distancia_sector(
            msg,
            math.radians(-20),
            math.radians(20)
        )

        # Sector izquierdo: +20 a +90 grados
        self.distancia_izquierda = self.distancia_sector(
            msg,
            math.radians(20),
            math.radians(90)
        )

        # Sector derecho: -90 a -20 grados
        self.distancia_derecha = self.distancia_sector(
            msg,
            math.radians(-90),
            math.radians(-20)
        )

        # Si no estamos esquivando y aparece un obstaculo,
        # iniciamos la maniobra.
        if (
            not self.esquivando
            and self.distancia_frente < self.distancia_deteccion
        ):

            self.esquivando = True
            self.fase_esquiva = 'GIRO_SALIDA'
            self.contador_esquiva = 0

            # Elegimos el lado que tenga mas espacio libre.
            if self.distancia_izquierda >= self.distancia_derecha:

                self.direccion_esquiva = 1

                self.get_logger().info(
                    'Obstaculo detectado. Esquivando por la izquierda.'
                )

            else:

                self.direccion_esquiva = -1

                self.get_logger().info(
                    'Obstaculo detectado. Esquivando por la derecha.'
                )

    def evitar_obstaculo(self, msg):

        # =====================================================
        # FASE 1: GIRO DE SALIDA
        # =====================================================

        if self.fase_esquiva == 'GIRO_SALIDA':

            # El JetBot sigue avanzando mientras gira.
            msg.linear.x = 0.10

            msg.angular.z = (
                0.8 * self.direccion_esquiva
            )

            self.contador_esquiva += 1

            if self.contador_esquiva >= self.ciclos_giro:

                self.fase_esquiva = 'AVANCE'
                self.contador_esquiva = 0

                self.get_logger().info(
                    'Primera fase completada. Pasando el obstaculo.'
                )

        # =====================================================
        # FASE 2: PASAR JUNTO AL OBSTACULO
        # =====================================================

        elif self.fase_esquiva == 'AVANCE':

            msg.linear.x = 0.10
            msg.angular.z = 0.0

            self.contador_esquiva += 1

            if self.contador_esquiva >= self.ciclos_avance:

                self.fase_esquiva = 'GIRO_RETORNO'
                self.contador_esquiva = 0

                self.get_logger().info(
                    'Obstaculo superado. Recuperando orientacion.'
                )

        # =====================================================
        # FASE 3: RECUPERAR ORIENTACION
        # =====================================================

        elif self.fase_esquiva == 'GIRO_RETORNO':

            # Seguimos avanzando mientras recuperamos la direccion.
            msg.linear.x = 0.10

            # Giramos hacia el lado contrario.
            msg.angular.z = (
                -0.8 * self.direccion_esquiva
            )

            self.contador_esquiva += 1

            if self.contador_esquiva >= self.ciclos_giro:

                self.esquivando = False
                self.fase_esquiva = 'GIRO_SALIDA'
                self.contador_esquiva = 0

                self.get_logger().info(
                    'Esquiva terminada. Continuando el dibujo.'
                )

    def move_robot(self):

        msg = Twist()

        # =====================================================
        # EVITACION DE OBSTACULOS
        # =====================================================

        if self.esquivando:

            self.evitar_obstaculo(msg)

            self.publisher_.publish(msg)

            return

        # =====================================================
        # DIBUJO DEL NUMERO 2 EN EL JETBOT REAL
        # =====================================================

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

        # Estado 3: base del numero 2
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

    node = ObstacleAvoidance()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:

        # Dejamos el JetBot parado antes de cerrar.
        stop = Twist()
        node.publisher_.publish(stop)

        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()