import signal
import sys

from vision import *
from detectors.fuel_detector import *
from detectors.robot_detector import *
from preprocessors.field_preprocessor import *
from preprocessors.robot_preprocessor import *
from flatteners.field_flattener import *
from flatteners.robot_flattener import *
from senders.socket_sender import *

field_vision = Vision([FuelDetector(), RobotDetector()], FieldPreprocessor(), FieldFlattener(), SocketSender(), "test_videos/match_video.mp4")
robot_vision = Vision([FuelDetector(), RobotDetector()], RobotPreprocessor(), RobotFlattener(), SocketSender(), "test_videos/match_video.mp4")

def kill(signal, frame):
    field_vision.kill()
    robot_vision.kill()
    sys.exit(0)

signal.signal(signal.SIGINT, kill)

print("Starting field vision thread")
field_vision.start()

print("Starting robot vision thread")
robot_vision.run()
