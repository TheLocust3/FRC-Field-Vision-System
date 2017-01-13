from vision import *
from detectors.fuel_detector import *
from detectors.robot_detector import *
from preprocessors.field_preprocessor import *
from flatteners.field_flattener import *
from senders.socket_sender import *

field_vision = Vision([FuelDetector(), RobotDetector()], FieldPreprocessor(), FieldFlattener(), SocketSender(), "test_videos/match_video.mp4")
field_vision.run()
field_vision.shutdown()
