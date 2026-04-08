#!/usr/bin/env python
import rospy
import numpy as np
from pycrazyswarm import *
from std_msgs.msg import Float64MultiArray
from std_msgs.msg import Bool

class FullStateCmd:
    def __init__(self):
        swarm = Crazyswarm()
        self.timeHelper = swarm.timeHelper
        self.cf = swarm.allcfs.crazyflies[0]

        self.hz = 100
        self.Z = 0.5
        self.take_off_duration = 2
        self.goto_duration = 4
        self.duration = 60
        # self.duration = 60
        init_pos = np.array([1.0,0.0,0.7])

        control_sub = rospy.Subscriber('/control', Float64MultiArray, self.update_control)
        self.control = None
        take_off_pub = rospy.Publisher('/take_off', Bool, queue_size=10)

        # LED color
        self.cf.setParam("ring/effect", 7)
        rgb = (1.0, 1.0, 1.0)
        self.cf.setLEDColor(*rgb)

        # control loop
        # take off
        self.cf.takeoff(targetHeight=self.Z, duration=self.take_off_duration)
        self.timeHelper.sleep(self.Z + self.take_off_duration)
        self.cf.goTo(init_pos, 0, self.goto_duration)
        self.timeHelper.sleep(0.5 + self.goto_duration)

        task_off_msg = Bool()
        task_off_msg.data = True
        take_off_pub.publish(task_off_msg)

        # fullStateCmd
        self.fullStateCmd()

        self.cf.notifySetpointsStop()
        # self.cf.goTo(np.array([0,0,self.Z]), 0, self.goto_duration)
        # self.timeHelper.sleep(0.5 + self.goto_duration)

        self.cf.land(targetHeight=0.03, duration=self.take_off_duration)
        self.timeHelper.sleep(self.Z + self.take_off_duration)

    def update_control(self, msg):
        self.control = np.array(msg.data)

    def fullStateCmd(self):
        start_time = self.timeHelper.time()
        while not self.timeHelper.isShutdown():
            t = self.timeHelper.time() - start_time
            if t > self.duration:
                break

            if self.control is not None:
                pos = self.control[:3]
                vel = self.control[3:6]
                acc = self.control[6:9]

                self.cf.cmdFullState(
                    pos,
                    vel,
                    acc,
                    0.0,
                    np.zeros((3,))
                )

            self.timeHelper.sleepForRate(self.hz)

if __name__ == "__main__":
    # swarm = Crazyswarm()
    # timeHelper = swarm.timeHelper
    # cf = swarm.allcfs.crazyflies[0]
    #
    # hz = 100
    # Z = 1
    #
    # # sub
    # control_sub = rospy.Subscriber('/control', Float64MultiArray, self.update_control)
    #
    # cf.takeoff(targetHeight=Z, duration=Z+1.0)
    # timeHelper.sleep(Z+2.0)
    #
    # fullStateCmd(timeHelper, cf)
    fullStateCmd = FullStateCmd()




