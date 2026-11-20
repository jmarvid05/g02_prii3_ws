import rclpy

from rclpy.node import Node
from rclpy.action import ActionClient

from action_msgs.msg import GoalStatus
from nav2_msgs.action import NavigateToPose
from std_msgs.msg import String


class AutonomousNavigation(Node):

    def __init__(self):
        super().__init__('autonomous_navigation')

        # Cliente para mandar destinos a Nav2.
        self.client = ActionClient(
            self,
            NavigateToPose,
            'navigate_to_pose'
        )

        # Recibe los ArUcos detectados.
        self.create_subscription(
            String,
            '/aruco_info',
            self.aruco_callback,
            10
        )

        # Pose delante del ArUco.
        # Se rellenará con las coordenadas reales.
        self.entrada_x = 0.0
        self.entrada_y = 0.0
        self.entrada_z = 0.0
        self.entrada_w = 1.0

        # Destino final.
        # Se rellenará con las coordenadas reales.
        self.destino_x = 0.0
        self.destino_y = 0.0

        # Al principio se ignoran los ArUcos.
        self.puede_leer_aruco = False

        # Evita mandar varias veces el destino final.
        self.aruco_detectado = False

        # El primer paso es ir delante del ArUco.
        self.enviar_entrada()


    def enviar_entrada(self):

        # Espera a que Nav2 esté preparado.
        self.client.wait_for_server()

        # Crea el objetivo de navegación.
        goal = NavigateToPose.Goal()

        # Las coordenadas pertenecen al mapa.
        goal.pose.header.frame_id = 'map'

        # Posición delante del ArUco.
        goal.pose.pose.position.x = self.entrada_x
        goal.pose.pose.position.y = self.entrada_y

        # Orientación para quedar mirando al ArUco.
        goal.pose.pose.orientation.z = self.entrada_z
        goal.pose.pose.orientation.w = self.entrada_w

        self.get_logger().info(
            'Yendo hacia el ArUco...'
        )

        # Manda el objetivo a Nav2.
        future = self.client.send_goal_async(goal)

        # Comprueba si Nav2 acepta el objetivo.
        future.add_done_callback(
            self.entrada_aceptada
        )


    def entrada_aceptada(self, future):

        # Respuesta de Nav2.
        goal_handle = future.result()

        # Si Nav2 rechaza el destino, no continúa.
        if not goal_handle.accepted:

            self.get_logger().info(
                'Destino rechazado.'
            )

            return

        self.get_logger().info(
            'Destino aceptado. Navegando...'
        )

        # Espera a que termine la navegación.
        result_future = goal_handle.get_result_async()

        result_future.add_done_callback(
            self.entrada_completada
        )


    def entrada_completada(self, future):

        # Obtiene el resultado final de Nav2.
        resultado = future.result()

        # Comprueba que realmente haya llegado.
        if resultado.status != GoalStatus.STATUS_SUCCEEDED:

            self.get_logger().info(
                'No se ha podido llegar al ArUco.'
            )

            return

        # El robot ya ha llegado a la entrada.
        self.get_logger().info(
            'Robot delante del ArUco.'
        )

        # Ahora sí empieza a aceptar ArUcos.
        self.puede_leer_aruco = True

        self.get_logger().info(
            'Esperando ID del ArUco...'
        )


    def aruco_callback(self, msg):

        # Ignora ArUcos mientras va hacia la entrada.
        if not self.puede_leer_aruco:
            return

        # Si ya ha usado un ArUco, no vuelve a actuar.
        if self.aruco_detectado:
            return

        # De momento se prueba con el ArUco 5.
        if 'ID: 5' in msg.data:

            self.get_logger().info(
                'ArUco 5 detectado.'
            )

            self.get_logger().info(
                'Yendo al destino final...'
            )

            # Evita repetir el destino.
            self.aruco_detectado = True

            self.enviar_destino()


    def enviar_destino(self):

        # Crea el destino final.
        goal = NavigateToPose.Goal()

        goal.pose.header.frame_id = 'map'

        # Coordenadas reales del destino.
        goal.pose.pose.position.x = self.destino_x
        goal.pose.pose.position.y = self.destino_y

        # Orientación final sencilla.
        goal.pose.pose.orientation.w = 1.0

        # Manda el destino a Nav2.
        self.client.send_goal_async(goal)


def main(args=None):

    # Inicializa ROS 2.
    rclpy.init(args=args)

    # Crea el nodo.
    node = AutonomousNavigation()

    # Mantiene el nodo funcionando.
    rclpy.spin(node)

    # Cierra correctamente.
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()