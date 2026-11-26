
import rclpy

from rclpy.node import Node
from rclpy.time import Time

from geometry_msgs.msg import PoseWithCovarianceStamped
from nav2_msgs.srv import ManageLifecycleNodes
from tf2_ros import Buffer, TransformListener


class Nav2AutoStart(Node):

    def __init__(self):
        super().__init__('nav2_auto_start')

        self.localization = self.create_client(
            ManageLifecycleNodes,
            '/lifecycle_manager_localization/manage_nodes'
        )

        self.navigation = self.create_client(
            ManageLifecycleNodes,
            '/lifecycle_manager_navigation/manage_nodes'
        )

        self.create_subscription(
            PoseWithCovarianceStamped,
            '/initialpose',
            self.pose_callback,
            10
        )

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.estado = 'esperando_localizacion'
        self.future = None
        self.pose_recibida = False

        self.create_timer(0.5, self.comprobar)

        self.get_logger().info('Esperando localizacion...')

    def pose_callback(self, msg):
        if msg.header.frame_id != 'map':
            self.get_logger().warn('La pose inicial debe estar en map')
            return

        self.pose_recibida = True

        if self.estado == 'esperando_pose':
            self.estado = 'esperando_tf'

    def iniciar_servicio(self, cliente):
        request = ManageLifecycleNodes.Request()
        request.command = 0  # STARTUP
        return cliente.call_async(request)

    def comprobar(self):

        if self.estado == 'esperando_localizacion':
            if self.localization.service_is_ready():
                self.future = self.iniciar_servicio(self.localization)
                self.estado = 'activando_localizacion'

        elif self.estado == 'activando_localizacion':
            if self.future.done():
                try:
                    respuesta = self.future.result()
                except Exception as error:
                    self.fallar(str(error))
                    return

                if respuesta is not None and respuesta.success:
                    self.get_logger().info(
                        'Localizacion activa. Usa 2D Pose Estimate.'
                    )
                    self.estado = (
                        'esperando_tf' if self.pose_recibida
                        else 'esperando_pose'
                    )
                else:
                    self.fallar('Error activando localizacion')

        elif self.estado == 'esperando_tf':
            if self.tf_buffer.can_transform(
                'map', 'base_footprint', Time()
            ):
                self.get_logger().info(
                    'TF disponible. Activando navegacion...'
                )
                self.estado = 'esperando_navegacion'

        elif self.estado == 'esperando_navegacion':
            if self.navigation.service_is_ready():
                self.future = self.iniciar_servicio(self.navigation)
                self.estado = 'activando_navegacion'

        elif self.estado == 'activando_navegacion':
            if self.future.done():
                try:
                    respuesta = self.future.result()
                except Exception as error:
                    self.fallar(str(error))
                    return

                if respuesta is not None and respuesta.success:
                    self.get_logger().info(
                        'NAV2 ACTIVADO. Listo para recibir destinos.'
                    )
                    self.estado = 'listo'
                else:
                    self.fallar('Error activando navegacion')

    def fallar(self, mensaje):
        self.get_logger().error(mensaje)
        self.estado = 'error'


def main(args=None):
    rclpy.init(args=args)
    node = Nav2AutoStart()

    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
