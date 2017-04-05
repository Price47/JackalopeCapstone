import numpy as np
import sys
import time
from threading import Timer
from pylibfreenect2 import Freenect2, SyncMultiFrameListener
from pylibfreenect2 import FrameType, Registration, Frame, FrameMap
from pylibfreenect2 import createConsoleLogger
from pylibfreenect2 import LoggerLevel

from settings import (X_CHANGE_THRESHOLD, DROWN_TIME, KINECT_SPECS, DANGER_THRESHOLD,
                      WARNING_THRESHOLD, DISTANCE_THRESHOLD, BODY_DEPTH_THRESHOLD)


class Kinect:

    def __init__(self):
        self.averageSpineX = 0

        self.fn = Freenect2()
        if self.fn.enumerateDevices() == 0:
            sys.exit(47)


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

    def valuePlusMinusDifferential(self, checkValue, testValue, Differential):
        if((checkValue < testValue + Differential) & (checkValue > testValue - Differential)):
            return True
        else:
            return False


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



    # calculate mean depth of depth array, used to find skeleton points.
    def getMeanDepth(self, depth, rows, cols):
        total = 0
        sumDepth = 0
        for row in range(rows):
            for col in range(cols):
                try:
                    offset = row + col * (rows)
                except IndexError as e:
                    print e
                #if depth[offset]['depth'] < DANGER_THRESHOLD:
                total += 1
                sumDepth += depth[offset]['depth']

        return (sumDepth / total)


    # calculate the skeleton points of the depth array
    def getSkeleton(self, depthArray, average, rows, cols):
        topY = 0
        leftX = rows
        bottomY = cols
        rightX = 0

        for d in depthArray:
            #print depthArray[offset]
            if (d['x'] > rightX):
                rightX = d['x']
            if (d['x'] < leftX):
                leftX = d['x']
            if (d['y'] < bottomY):
                bottomY = d['y']
            if (d['y'] > topY):
                topY = d['y']

        averageX = (leftX + rightX) / 2
        returnValues = {'averageX': averageX,
                        'topY': topY,
                        'bottomY': bottomY,
                        'rightX': rightX,
                        'leftX': leftX}

        return returnValues


    def changeInX(self, spine):
        print "changeInX"
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
        print "checkDrowning"
        drowningRisk = True
        drowning = False
        falsePositive = 0
        # 20 seconds from start of def #
        timeLimit = time.time() + DROWN_TIME
        self.device.start()
        while drowningRisk:
            print 'checking...'
            if time.time() > timeLimit:
                drowningRisk = False
                drowning = True

            data = self.fullDataLoop()
            if (self.valueUnbounded((self.averageSpineX - data['spine']['averageX']), X_CHANGE_THRESHOLD)):
                falsePositive += 1
                if falsePositive > 100:
                    drowningRisk = False
            else:
                continue
        if drowning:
            self.device.stop()
            print "This guy is for sure drowning"
            sys.exit(47)

        self.device.stop()

    def depthMatrixToPointCloudPos2(self, depthArray):

        R, C = depthArray.shape

        R -= KINECT_SPECS['cx']
        R *= depthArray
        R /= KINECT_SPECS['fx']

        C -= KINECT_SPECS['cy']
        C *= depthArray
        C /= KINECT_SPECS['fy']

        return np.column_stack((depthArray.ravel(), R.ravel(), C.ravel()))

    def getBody(self, depthArray, average, rows, cols):
        body = []

        for d in depthArray:
            if self.valuePlusMinusDifferential(d['depth'], average, BODY_DEPTH_THRESHOLD):
                body.append(d)

        return body

    def pointRavel(self, unraveledArray, rows, cols):
        raveledArray = []
        d = unraveledArray.ravel()
        for row in range(rows):
            for col in range(cols):
                try:
                    offset = row + col * (rows)
                    raveledArray.append({'x': row, 'y': col, 'depth': d[offset]})
                except IndexError as e:
                    print e

        return raveledArray

    def fullDataLoop(self):


        registration = Registration(self.device.getIrCameraParams(),
                                    self.device.getColorCameraParams())

        deptharraytest = [{'x': 152, 'y': 100, 'depth': 400}, {'x': 300, 'y': 200, 'depth': 400},
                          {'x': 350, 'y': 150, 'depth': 400}, {'x': 400, 'y': 300, 'depth': 400},
                          {'x': 22, 'y': 10, 'depth': 400}, {'x': 144, 'y': 12, 'depth': 400}]

        depthArray = self.update(registration)
        rows, cols = depthArray.shape
        d = self.pointRavel(depthArray, rows, cols)
        m = self.getMeanDepth(d, rows, cols)
        b = self.getBody(d, m, rows, cols)
        s = self.getSkeleton(deptharraytest, m, cols, rows)


        return {'spine' : s, 'meanDepth' : m}

    def run(self, duration):
        end = time.time() + duration
        self.device.start()

        registration = Registration(self.device.getIrCameraParams(),
                                    self.device.getColorCameraParams())


        deptharraytest = [{'x':152, 'y':100, 'depth':400}, {'x':300, 'y':200, 'depth':400},
                          {'x': 350, 'y': 150, 'depth': 400},{'x':400, 'y':300, 'depth':400},
                          {'x': 22, 'y': 10, 'depth': 400},{'x':144, 'y':12, 'depth':400}]
        while time.time() < end:
            depthArray = self.update(registration)
            rows, cols = depthArray.shape
            d = self.pointRavel(depthArray, rows, cols)
            m =self.getMeanDepth(d, rows, cols)
            b = self.getBody(d, m, rows, cols)
            s = self.getSkeleton(deptharraytest, m, cols, rows)
            self.changeInX(s)


        self.device.stop()

    def execute(self):
        self.device.start()

        registration = Registration(self.device.getIrCameraParams(),
                                    self.device.getColorCameraParams())

        d = self.update(registration)
        shape = d.shape
        m = self.getMeanDepth(d, 9)
        b = self.getBody(d,m)
        s = self.getSkeleton(d, m)
        self.changeInX(s)


        print 'depthArray' + str(len(d.ravel()))
        print 'body' + str(len(b))
        for body in b:
            print "(" + str(body['x']) + "," + str(body['y']) + "): " + str(body['z'])


        print m


        self.device.stop()




    def exit(self):
        self.device.stop()
        self.device.close()

2