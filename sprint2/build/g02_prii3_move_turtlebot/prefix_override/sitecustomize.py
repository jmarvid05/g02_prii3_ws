import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/javiermv/UNI/PROYECTOS3/g02_prii3_ws/sprint2/install/g02_prii3_move_turtlebot'
