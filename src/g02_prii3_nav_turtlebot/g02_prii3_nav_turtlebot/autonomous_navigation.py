import rclpy

from rclpy.node import Node
from rclpy.action import ActionClient

from action_msgs.msg import GoalStatus
from nav2_msgs.action import NavigateToPose
from std_msgs.msg import String


class AutonomousNavigation(Node):

    def __init__(self):
        super().__init__('autonomous_navigation')

        # Cliente para enviar objetivos a Navigation2.
        self.client = ActionClient(
            self,
            NavigateToPose,
            'navigate_to_pose'
        )

        # Suscripción al topic donde se publican los ArUcos detectados.
        self.create_subscription(
            String,
            '/aruco_info',
            self.aruco_callback,
            10
        )

        # Pose intermedia delante del ArUco 5.
        # Incluye posición y orientación.
        self.entrada_x = 3.24
        self.entrada_y = 1.71
        self.entrada_z = 0.717
        self.entrada_w = 0.697

        # Destino final: mesa del profesor.
        self.mesa_x = 2.75
        self.mesa_y = 14.42

        # Al principio se ignoran los ArUcos.
        # Solo se activará cuando el robot llegue a la entrada.
        self.puede_leer_aruco = False

        # Evita mandar varias veces el mismo destino final.
        self.aruco_detectado = False

        # El primer paso es ir delante del ArUco.
        self.enviar_entrada()


    def enviar_entrada(self):

        # Espera hasta que Navigation2 esté disponible.
        self.client.wait_for_server()

        # Crea el objetivo de navegación.
        goal = NavigateToPose.Goal()

        # Las coordenadas están referidas al mapa.
        goal.pose.header.frame_id = 'map'

        # Posición delante del ArUco.
        goal.pose.pose.position.x = self.entrada_x
        goal.pose.pose.position.y = self.entrada_y

        # Orientación para que el robot quede mirando al ArUco.
        goal.pose.pose.orientation.z = self.entrada_z
        goal.pose.pose.orientation.w = self.entrada_w

        self.get_logger().info(
            'Yendo hacia el ArUco...'
        )

        # Envía el objetivo a Navigation2.
        future = self.client.send_goal_async(goal)

        # Cuando Nav2 responde si acepta o no el objetivo,
        # se ejecuta entrada_aceptada().
        future.add_done_callback(
            self.entrada_aceptada
        )


    def entrada_aceptada(self, future):

        # Obtiene la respuesta de Navigation2.
        goal_handle = future.result()

        # Si Nav2 rechaza el objetivo, se detiene aquí.
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

        # Cuando termina, comprueba si realmente ha llegado.
        result_future.add_done_callback(
            self.entrada_completada
        )


    def entrada_completada(self, future):

        # Resultado final de la navegación.
        resultado = future.result()

        # Solo continuamos si Navigation2 confirma
        # que el objetivo se ha completado correctamente.
        if resultado.status != GoalStatus.STATUS_SUCCEEDED:

            self.get_logger().info(
                'No se ha podido llegar al ArUco.'
            )

            return

        # El robot ya está delante del ArUco.
        self.get_logger().info(
            'Robot delante del ArUco.'
        )

        # A partir de ahora sí se aceptan
        # los mensajes recibidos por /aruco_info.
        self.puede_leer_aruco = True

        self.get_logger().info(
            'Esperando ID del ArUco...'
        )


    def aruco_callback(self, msg):

        # Mientras el robot va hacia la entrada,
        # se ignoran todos los ArUcos detectados.
        if not self.puede_leer_aruco:
            return

        # Si ya se ha usado un ArUco,
        # no volvemos a mandar el destino.
        if self.aruco_detectado:
            return

        # Si se detecta el ArUco 5,
        # se manda al robot hacia la mesa.
        if 'ID: 5' in msg.data:

            self.get_logger().info(
                'ArUco 5 detectado.'
            )

            self.get_logger().info(
                'Yendo a la mesa del profesor...'
            )

            # Evita ejecutar esta parte varias veces.
            self.aruco_detectado = True

            self.enviar_mesa()


    def enviar_mesa(self):

        # Crea un nuevo objetivo.
        goal = NavigateToPose.Goal()

        goal.pose.header.frame_id = 'map'

        # Posición final.
        goal.pose.pose.position.x = self.mesa_x
        goal.pose.pose.position.y = self.mesa_y

        # Orientación final sencilla.
        goal.pose.pose.orientation.w = 1.0

        # Envía el destino final.
        self.client.send_goal_async(goal)


def main(args=None):

    # Inicializa ROS 2.
    rclpy.init(args=args)

    # Crea el nodo.
    node = AutonomousNavigation()

    # Mantiene el nodo funcionando.
    rclpy.spin(node)

    # Cierra el nodo correctamente.
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()