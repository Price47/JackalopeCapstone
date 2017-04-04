import numpy as np
import sys
import time
from threading import Timer
from pylibfreenect2 import Freenect2, SyncMultiFrameListener
from pylibfreenect2 import FrameType, Registration, Frame, FrameMap
from pylibfreenect2 import createConsoleLogger
from pylibfreenect2 import LoggerLevel

from settings import (X_CHANGE_THRESHOLD, DROWN_TIME, KINECT_SPECS, DANGER_THRESHOLD,
                        WARNING_THRESHOLD,DISTANCE_THRESHOLD)


class Kinect:
    def __init__(self):
        self.averageSpineX = 0

        self.fn = Freenect2()
        assert self.fn.enumerateDevices() > 0

        self.serial = self.fn.getDeviceSerialNumber(0)

        types = 0
        types |= FrameType.Color
        types |= (FrameType.Ir | FrameType.Depth)
        self.listener = SyncMultiFrameListener(types)

        self.logger = createConsoleLogger(LoggerLevel.Debug)

        self.device = self.fn.openDevice(self.serial)

        self.device.setColorFrameListener(self.listener)
        self.device.setIrAndDepthFrameListener(self.listener)

        self.undistorted = Frame(512, 424, 4)
        self.registered = Frame(512, 424, 4)

    def valueBounded(self, checkValue, absoluteValue):
        if ((-absoluteValue <= checkValue >= absoluteValue)):
            return True
        else:
            return False

    def valueUnbounded(self, checkValue, absoluteValue):
        if ((checkValue > absoluteValue) | (checkValue < -absoluteValue)):
            return True
        else:
            return False


    def depthMatrixToPointCloudPos2(self, depthArray):

        R, C = depthArray.shape

        R -= KINECT_SPECS['cx']
        R *= depthArray
        R /= KINECT_SPECS['fx']

        C -= KINECT_SPECS['cy']
        C *= depthArray
        C /= KINECT_SPECS['fy']

        return np.column_stack((depthArray.ravel(), R.ravel(), -C.ravel()))

    def update(self, registration):
        self.device.setColorFrameListener(self.listener)
        self.device.setIrAndDepthFrameListener(self.listener)

        frames = self.listener.waitForNewFrame()
        depth = frames["depth"]
        color = frames["color"]

        d = self.undistorted.asarray(dtype=np.float32)

        registration.apply(color, depth, self.undistorted, self.registered)

        self.listener.release(frames)

        return d

    # calculate the average and skeleton points of a depth array, those
    # values plus the depth array
    def getDepthArray(self):
        depthArray = Frame(512, 424, 4).asarray(dtype=np.float32)
        average = self.getMeanDepth(depthArray)
        skeletonPoints = self.getSkeleton(depthArray, average)

        return {'depthArray': depthArray,
                'average': average,
                'skeletonPoints': skeletonPoints}

    # calculate mean depth of depth array, used to find skeleton points
    def getMeanDepth(self, depth):
        total = 0
        sumDepth = 0

        rows, columns = depth.shape
        depthArray = depth.ravel()

        for row in range(rows):
            for col in range(columns):
                try:
                    offset = row + col * (rows)
                except IndexError as e:
                    print e
                data = depthArray[offset]
                total += 1
                sumDepth += data

        return (sumDepth / total)

    # calculate the skeleton points of the depth array
    def getSkeleton(self, depthArray, rows, columns, average):
        topY = 0
        leftX = 0
        bottomY = self.depthHeight
        rightX = self.depthWidth

        rows, columns = depthArray.shape
        depthArray = depthArray.ravel()

        for row in range(rows):
            for col in range(columns):
                try:
                    offset = row + col * (rows)
                except IndexError as e:
                    print e
                if (self.valueBounded(depthArray[offset],200)):
                    if (row > leftX):
                        leftX = row
                    if (col < bottomY):
                        bottomY = col
                    if (row < rightX):
                        rightX = row
                    if (col > topY):
                        topY = col

        averageX = (leftX + rightX) / 2
        returnValues = {'averageX': averageX,
                        'topY': topY,
                        'bottomY': bottomY,
                        'leftX': leftX,
                        'rightX': rightX}

        return returnValues

    def changeInX(self, spine):
        if self.averageSpineX == 0:
            self.averageSpineX = spine['averageX']
        elif (self.valueBounded((self.averageSpineX - spine['averageX']), X_CHANGE_THRESHOLD)):
            self.averageSpineX = ((self.averageSpineX + spine['averageX']) / 2)
        else:
            self.checkDrowning()

    # Check to see if the difference between the averageSpineX and the last
    # analyzed averageX is less below a threshold. If it is, the loop
    # continues. If it runs for 20 seconds, it will set the drowning flag to
    # true. If falsePositive gets to be too high, DORi will no longer
    # assume the victim is a drowning risk
    def checkDrowning(self):
        drowningRisk = True
        drowning = False
        falsePositive = 0
        # 20 seconds from start of def #
        timeLimit = time.time() + DROWN_TIME
        while drowningRisk:
            if time.time() > timeLimit:
                drowning = True
            depth = self.getDepthArray()
            if (self.valueUnbounded((self.averageSpineX - depth['skeletonPoints']['averageX']), X_CHANGE_THRESHOLD)):
                falsePositive += 1
                if falsePositive > 100:
                    drowningRisk = False
            else:
                continue

    def dataLoop(self):
        dangerThreshold = DANGER_THRESHOLD
        warningThreshold = WARNING_THRESHOLD
        distanceThreshold = DISTANCE_THRESHOLD
        depth = self.getDepthArray()
        shoulderHeight = (depth['skeletonPoints']['topY']) * (7 / 8)
        body = []
        for x in range(0, self.depthWidth):
            for y in range(0, self.depthHeight):
                offset = x + y * self.depthWidth
                d = depth['depthArray'][offset]
                if (d > depth['average'] - 200 & d < depth['average'] + 200):
                    print "build skeleton"
                    body.append(d)
                elif (d > 300 & d < dangerThreshold):
                    print "MOVE THE FUCK BACK"
                elif (d > dangerThreshold & d < warningThreshold):
                    print "move back"
                elif (d > warningThreshold & d < distanceThreshold):
                    print "good distance"
                else:
                    print "too far"

        spine = {'topY': depth['skeletonPoints']['topY'],
                 'bottomY': depth['skeletonPoints']['bottomY'],
                 'averageX': depth['skeletonPoints']['averageX']}

        self.changeInX(spine)

    def run(self, duration):
        end = time.time() + duration
        self.device.start()

        registration = Registration(self.device.getIrCameraParams(),
                                    self.device.getColorCameraParams())

        while time.time() < end:
            d = self.update(registration)
            m =  self.getMeanDepth(d)
            print m

        self.device.stop()


    def exit(self):
        self.device.stop()
        self.device.close()

2