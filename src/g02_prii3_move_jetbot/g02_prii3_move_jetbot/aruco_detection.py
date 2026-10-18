import cv2
import rclpy
import os

from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from ament_index_python.packages import get_package_share_directory


class ArucoDetection(Node):

    def __init__(self):
        super().__init__('aruco_detection')

        self.bridge = CvBridge()

        # Topic provisional de la camara
        self.declare_parameter(
            'image_topic',
            '/camera/image_raw'
        )

        # Tamano provisional del ArUco en metros
        self.declare_parameter(
            'marker_size',
            0.05
        )

        self.image_topic = self.get_parameter(
            'image_topic'
        ).get_parameter_value().string_value

        self.marker_size = self.get_parameter(
            'marker_size'
        ).get_parameter_value().double_value

        # Cargar calibracion
        package_share = get_package_share_directory(
            'g02_prii3_move_jetbot'
        )

        calibration_file = os.path.join(
            package_share,
            'config',
            'CameraModel.yml'
        )

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

        # Diccionario usado por los marcadores
        self.dictionary = cv2.aruco.Dictionary_get(
            cv2.aruco.DICT_4X4_50
        )

        self.parameters = cv2.aruco.DetectorParameters_create()

        self.subscription = self.create_subscription(
            Image,
            self.image_topic,
            self.image_callback,
            10
        )

        self.get_logger().info(
            'Detector ArUco iniciado'
        )

        self.get_logger().info(
            f'Esperando imagenes en: {self.image_topic}'
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

        gray = cv2.cvtColor(
            img,
            cv2.COLOR_BGR2GRAY
        )

        corners, ids, rejected = cv2.aruco.detectMarkers(
            gray,
            self.dictionary,
            parameters=self.parameters
        )

        if ids is not None:

            cv2.aruco.drawDetectedMarkers(
                img,
                corners,
                ids
            )

            rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(
                corners,
                self.marker_size,
                self.camera_matrix,
                self.dist_coeffs
            )

            for i in range(len(ids)):

                marker_id = int(ids[i][0])

                cv2.drawFrameAxes(
                    img,
                    self.camera_matrix,
                    self.dist_coeffs,
                    rvecs[i],
                    tvecs[i],
                    self.marker_size * 0.5
                )

                esquina = corners[i][0][0]

                x = int(esquina[0])
                y = int(esquina[1])

                cv2.putText(
                    img,
                    f'ID: {marker_id}',
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2
                )

        cv2.imshow(
            'Deteccion ArUco',
            img
        )

        cv2.waitKey(1)


def main(args=None):

    rclpy.init(args=args)

    node = ArucoDetection()

    rclpy.spin(node)

    node.destroy_node()

    cv2.destroyAllWindows()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
