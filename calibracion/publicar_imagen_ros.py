import cv2
import rclpy

from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge


class ImagePublisher(Node):

    def __init__(self):
        super().__init__('image_publisher')

        self.publisher_ = self.create_publisher(
            Image,
            '/camera/image_raw',
            10
        )

        self.bridge = CvBridge()

        self.image = cv2.imread(
            'calibracion/imagen_prueba.jpg'
        )

        if self.image is None:
            self.get_logger().error('No se pudo cargar la imagen')
            return

        self.timer = self.create_timer(
            0.5,
            self.publish_image
        )

        self.get_logger().info(
            'Publicando imagen en /camera/image_raw'
        )

    def publish_image(self):

        msg = self.bridge.cv2_to_imgmsg(
            self.image,
            encoding='bgr8'
        )

        self.publisher_.publish(msg)


def main(args=None):

    rclpy.init(args=args)

    node = ImagePublisher()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
