import cv2
import rclpy

from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from ament_index_python.packages import get_package_share_directory

import os


class CameraRectification(Node):

    def __init__(self):
        super().__init__('camera_rectification')

        self.bridge = CvBridge()

        # Topic provisional de la cámara.
        # Cuando tengamos el JetBot comprobaremos el topic real.
        self.declare_parameter(
            'image_topic',
            '/camera/image_raw'
        )

        image_topic = self.get_parameter(
            'image_topic'
        ).get_parameter_value().string_value

        # Buscar CameraModel.yml dentro del paquete
        package_share = get_package_share_directory(
            'g02_prii3_move_jetbot'
        )

        calibration_file = os.path.join(
            package_share,
            'config',
            'CameraModel.yml'
        )

        # Cargar parámetros de calibración
        fs = cv2.FileStorage(
            calibration_file,
            cv2.FILE_STORAGE_READ
        )

        self.camera_matrix = fs.getNode(
            'cameraMatrix'
        ).mat()

        self.dist_coeffs = fs.getNode(
            'distCoeffs'
        ).mat()

        fs.release()

        if self.camera_matrix is None or self.dist_coeffs is None:
            self.get_logger().error(
                'No se pudieron cargar los parametros de calibracion'
            )
            return

        self.get_logger().info(
            'Parametros de calibracion cargados correctamente'
        )

        self.get_logger().info(
            f'Esperando imagenes en: {image_topic}'
        )

        self.subscription = self.create_subscription(
            Image,
            image_topic,
            self.image_callback,
            10
        )

    def image_callback(self, msg):

        try:
            img = self.bridge.imgmsg_to_cv2(
                msg,
                desired_encoding='bgr8'
            )

        except Exception as error:
            self.get_logger().error(str(error))
            return

        h, w = img.shape[:2]

        new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(
            self.camera_matrix,
            self.dist_coeffs,
            (w, h),
            1,
            (w, h)
        )

        rectificada = cv2.undistort(
            img,
            self.camera_matrix,
            self.dist_coeffs,
            None,
            new_camera_matrix
        )

        original = img.copy()

        cv2.putText(
            original,
            'ORIGINAL',
            (40, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.5,
            (0, 255, 0),
            3
        )

        cv2.putText(
            rectificada,
            'RECTIFICADA',
            (40, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.5,
            (0, 255, 0),
            3
        )

        comparacion = cv2.hconcat(
            [original, rectificada]
        )

        comparacion = cv2.resize(
            comparacion,
            None,
            fx=0.5,
            fy=0.5
        )

        cv2.imshow(
            'Original vs Rectificada',
            comparacion
        )

        cv2.waitKey(1)


def main(args=None):

    rclpy.init(args=args)

    node = CameraRectification()

    rclpy.spin(node)

    node.destroy_node()

    cv2.destroyAllWindows()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
