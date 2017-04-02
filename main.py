from kinect import Kinect
import time

k = Kinect()

end_time = time.time() + 3


d = k.update()
for data in d:
    print data

