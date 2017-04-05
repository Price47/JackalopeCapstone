from kinect import Kinect
import time
from settings import RUN_TIME

k = Kinect()

#k.run(6)
#
# for m in means:
#     print m

# k.execute()
k.run(RUN_TIME)

