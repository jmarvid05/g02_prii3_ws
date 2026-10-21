import math

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data

from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


class ObstacleAvoidance(Node):

    def __init__(self):
        super().__init__('obstacle_avoidance')

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

        # Movimiento cada 0.1 segundos
        self.timer = self.create_timer(
            0.1,
            self.move_robot
        )

        # -----------------------------
        # DIBUJO DEL NUMERO 2
        # -----------------------------

        self.estado = 0
        self.contador = 0

        # -----------------------------
        # DATOS DEL LIDAR
        # -----------------------------

        self.distancia_frente = math.inf
        self.distancia_izquierda = math.inf
        self.distancia_derecha = math.inf

        # Si aparece algo a menos de 50 cm,
        # iniciamos la maniobra de esquiva
        self.distancia_deteccion = 0.50

        # -----------------------------
        # CONTROL DE LA ESQUIVA
        # -----------------------------

        self.esquivando = False

        # 1 = izquierda
        # -1 = derecha
        self.direccion_esquiva = 0

        # Fases posibles:
        # GIRO_SALIDA
        # AVANCE
        # GIRO_RETORNO
        self.fase_esquiva = 'GIRO_SALIDA'

        self.contador_esquiva = 0

        # Duracion de cada fase.
        # El timer funciona cada 0.1 segundos.
        self.ciclos_giro = 15
        self.ciclos_avance = 25

        self.get_logger().info(
            'Obstacle avoidance iniciado'
        )

    def distancia_sector(self, msg, angulo_min, angulo_max):

        distancias = []

        for i, distancia in enumerate(msg.ranges):

            angulo = (
                msg.angle_min
                + i * msg.angle_increment
            )

            # Normalizamos entre -pi y +pi
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

        # -----------------------------
        # FRENTE
        # -20 grados a +20 grados
        # -----------------------------

        self.distancia_frente = self.distancia_sector(
            msg,
            math.radians(-20),
            math.radians(20)
        )

        # -----------------------------
        # IZQUIERDA
        # +20 grados a +90 grados
        # -----------------------------

        self.distancia_izquierda = self.distancia_sector(
            msg,
            math.radians(20),
            math.radians(90)
        )

        # -----------------------------
        # DERECHA
        # -90 grados a -20 grados
        # -----------------------------

        self.distancia_derecha = self.distancia_sector(
            msg,
            math.radians(-90),
            math.radians(-20)
        )

        # Solo iniciamos una nueva esquiva
        # si actualmente no estamos haciendo otra
        if (
            not self.esquivando
            and self.distancia_frente < self.distancia_deteccion
        ):

            self.esquivando = True
            self.fase_esquiva = 'GIRO_SALIDA'
            self.contador_esquiva = 0

            # Elegimos el lado con mayor espacio
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

            # Avanzamos mientras nos apartamos
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
        # FASE 2: AVANZAR PARA SUPERAR EL OBSTACULO
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
        # FASE 3: RECUPERAR LA ORIENTACION
        # =====================================================

        elif self.fase_esquiva == 'GIRO_RETORNO':

            # Seguimos avanzando
            msg.linear.x = 0.10

            # Giramos al lado contrario
            msg.angular.z = (
                -0.8 * self.direccion_esquiva
            )

            self.contador_esquiva += 1

            # Giramos exactamente el mismo tiempo
            # que en GIRO_SALIDA
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
        # SI ESTAMOS ESQUIVANDO
        # =====================================================

        if self.esquivando:

            self.evitar_obstaculo(msg)

            self.publisher_.publish(msg)

            return

        # =====================================================
        # DIBUJO NORMAL DEL NUMERO 2
        # =====================================================

        # Estado 0: primera curva
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

        # Estado 2: giro inferior
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

    node = ObstacleAvoidance()

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