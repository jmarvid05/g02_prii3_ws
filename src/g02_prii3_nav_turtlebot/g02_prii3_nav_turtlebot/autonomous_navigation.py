import rclpy

from rclpy.node import Node
from rclpy.action import ActionClient

from action_msgs.msg import GoalStatus
from geometry_msgs.msg import PoseWithCovarianceStamped
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

        # Recibe los ArUcos detectados.
        self.create_subscription(
            String,
            '/aruco_info',
            self.aruco_callback,
            10
        )

        # Recibe la pose inicial marcada con 2D Pose Estimate.
        self.create_subscription(
            PoseWithCovarianceStamped,
            '/initialpose',
            self.initial_pose_callback,
            10
        )

        # Pose intermedia delante del ArUco 5.
        self.entrada_x = 3.24
        self.entrada_y = 1.71
        self.entrada_z = 0.717
        self.entrada_w = 0.697

        # Destino final: mesa del profesor.
        self.mesa_x = 2.75
        self.mesa_y = 14.42

        # Al principio se ignoran los ArUcos.
        self.puede_leer_aruco = False

        # Evita mandar varias veces el destino final.
        self.aruco_detectado = False

        # Evita iniciar la navegación varias veces.
        self.navegacion_iniciada = False

        # Timer para esperar a que Nav2 termine de activarse.
        self.timer_inicio = None

        self.get_logger().info(
            'Esperando 2D Pose Estimate en RViz...'
        )


    def initial_pose_callback(self, msg):

        # Solo inicia la navegación una vez.
        if self.navegacion_iniciada:
            return

        self.navegacion_iniciada = True

        self.get_logger().info(
            'Pose inicial recibida desde RViz.'
        )

        self.get_logger().info(
            'Esperando a que Nav2 esté preparado...'
        )

        # Espera 5 segundos antes de empezar.
        self.timer_inicio = self.create_timer(
            5.0,
            self.iniciar_navegacion
        )


    def iniciar_navegacion(self):

        # El timer solo se ejecuta una vez.
        self.timer_inicio.cancel()

        # Empieza la navegación hacia el ArUco.
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

        # Orientación para quedar mirando al ArUco.
        goal.pose.pose.orientation.z = self.entrada_z
        goal.pose.pose.orientation.w = self.entrada_w

        self.get_logger().info(
            'Yendo hacia el ArUco...'
        )

        # Envía el objetivo a Navigation2.
        future = self.client.send_goal_async(goal)

        # Comprueba si Nav2 acepta el destino.
        future.add_done_callback(
            self.entrada_aceptada
        )


    def entrada_aceptada(self, future):

        # Obtiene la respuesta de Navigation2.
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

        # Obtiene el resultado final de Navigation2.
        resultado = future.result()

        # Solo continúa si el robot ha llegado correctamente.
        if resultado.status != GoalStatus.STATUS_SUCCEEDED:

            self.get_logger().info(
                'No se ha podido llegar al ArUco.'
            )

            return

        self.get_logger().info(
            'Robot delante del ArUco.'
        )

        # Ahora sí empieza a aceptar ArUcos.
        self.puede_leer_aruco = True

        self.get_logger().info(
            'Esperando ID del ArUco...'
        )


    def aruco_callback(self, msg):

        # Mientras el robot va hacia la entrada,
        # se ignoran los ArUcos detectados.
        if not self.puede_leer_aruco:
            return

        # Si ya se ha usado un ArUco,
        # no vuelve a mandar el destino.
        if self.aruco_detectado:
            return

        # Comprueba exactamente si aparece el ID 5.
        aruco_5 = any(
            aruco.strip().startswith('ID: 5,')
            for aruco in msg.data.split('|')
        )

        if aruco_5:

            self.get_logger().info(
                'ArUco 5 detectado.'
            )

            self.get_logger().info(
                'Yendo a la mesa del profesor...'
            )

            # Evita repetir el destino.
            self.aruco_detectado = True

            self.enviar_mesa()


    def enviar_mesa(self):

        # Crea el destino final.
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

    # Cierra correctamente.
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()