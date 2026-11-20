import cv2
import rclpy

from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String


class ArucoDetection(Node):

    def __init__(self):
        super().__init__('aruco_detection')

        # Convierte imágenes ROS a OpenCV.
        self.bridge = CvBridge()

        # Diccionario usado en Eurobot.
        self.dictionary = cv2.aruco.getPredefinedDictionary(
            cv2.aruco.DICT_4X4_100
        )

        self.parameters = cv2.aruco.DetectorParameters_create()

        # Recibe imágenes de la cámara.
        self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )

        # Publica ID y coordenadas.
        self.publisher = self.create_publisher(
            String,
            '/aruco_info',
            10
        )


    def image_callback(self, msg):

        # Imagen ROS -> OpenCV.
        image = self.bridge.imgmsg_to_cv2(
            msg,
            desired_encoding='bgr8'
        )

        # Detecta los ArUcos.
        corners, ids, _ = cv2.aruco.detectMarkers(
            image,
            self.dictionary,
            parameters=self.parameters
        )

        arucos = []

        if ids is not None:

            for corner, marker_id in zip(
                corners,
                ids.flatten()
            ):

                # Calcula el centro del ArUco.
                puntos = corner[0]

                x = int(puntos[:, 0].mean())
                y = int(puntos[:, 1].mean())

                arucos.append(
                    f'ID: {marker_id}, X: {x}, Y: {y}'
                )

        # Publica todos los ArUcos detectados.
        mensaje = String()

        if arucos:
            mensaje.data = ' | '.join(arucos)
        else:
            mensaje.data = '[]'

        self.publisher.publish(mensaje)


def main(args=None):

    rclpy.init(args=args)

    node = ArucoDetection()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()