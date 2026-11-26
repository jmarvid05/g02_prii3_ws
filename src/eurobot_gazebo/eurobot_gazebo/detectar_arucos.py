import cv2
import rclpy

from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String


class ArucoDetection(Node):

    def __init__(self):
        super().__init__('aruco_detection')

        self.bridge = CvBridge()

        self.dictionary = cv2.aruco.getPredefinedDictionary(
            cv2.aruco.DICT_4X4_100
        )

        self.parameters = cv2.aruco.DetectorParameters_create()

        self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )

        self.publicadores = {}


    def image_callback(self, msg):

        image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')

        corners, ids, _ = cv2.aruco.detectMarkers(
            image, self.dictionary, parameters=self.parameters
        )

        detectados = []

        if ids is not None:

            for corner, marker_id in zip(corners, ids.flatten()):

                marker_id = int(marker_id)

                # Solo ArUcos de Eurobot
                if marker_id not in range(20, 24) and marker_id not in range(51, 60):
                    continue

                puntos = corner[0]
                x = int(puntos[:, 0].mean())
                y = int(puntos[:, 1].mean())

                # Crear topic si no existe
                if marker_id not in self.publicadores:
                    self.publicadores[marker_id] = self.create_publisher(
                        String,
                        f'/overhead_camera/aruco_{marker_id}',
                        10
                    )

                mensaje = String()
                mensaje.data = f'ID: {marker_id}, X: {x}, Y: {y}'

                self.publicadores[marker_id].publish(mensaje)
                detectados.append(marker_id)

        # Eliminar ArUcos que ya no se ven
        for marker_id in list(self.publicadores):
            if marker_id not in detectados:
                self.destroy_publisher(self.publicadores.pop(marker_id))


def main(args=None):

    rclpy.init(args=args)

    node = ArucoDetection()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()