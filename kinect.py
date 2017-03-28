import numpy as np
import sys
from pylibfreenect2 import Freenect2, SyncMultiFrameListener
from pylibfreenect2 import FrameType, Registration, Frame
from pylibfreenect2 import createConsoleLogger, setGlobalLogger
from pylibfreenect2 import LoggerLevel


print "price is a bller"

fn = Freenect2()
assert fn.enumerateDevices() > 0

logger = createConsoleLogger(
    LoggerLevel.Debug)

device = fn.openDefaultDevice()

frame = Frame(512, 424, 4)
try:
    depth_array = frame.asarray(dtype=np.float32)
    print depth_array
except Exception as e:
    print e

