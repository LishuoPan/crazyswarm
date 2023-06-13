"""Takeoff-hover-land for one CF. Useful to validate hardware config."""

from pycrazyswarm import Crazyswarm
import numpy as np

TAKEOFF_DURATION = 2.5
ACTION_GAP = 0.5
HOVER_DURATION = 5.0
NUM_COMMAND_REPEAT = 2


def main():
    # Environment constant 
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    cfs = swarm.allcfs
    num_robots = 50
    num_robots_each_row = 7

    num_action_loop = 30


    # execution
    # take off command
    cfs.takeoff(targetHeight=1.0, duration=TAKEOFF_DURATION)
    timeHelper.sleep(TAKEOFF_DURATION + ACTION_GAP)

    for i in range(num_action_loop):
        # individual goTo command
        for cf_id in np.arange(1, num_robots+1, 1): # this loops the robot id
            # access the cf byID
            try:
                cf = cfs.crazyfliesById[cf_id]
            except:
                continue

            # identify the row index based on the robot id
            row_index = cf_id // num_robots_each_row
            # print(row_index%2)
            if (row_index % 2 == 0): # go left
                # print("go left", row_index)
                for i in range(NUM_COMMAND_REPEAT):
                    cf.goTo([1.,0.,0.], 0., 2., relative=True)
            else: # go right
                # print("go right", row_index)
                for i in range(NUM_COMMAND_REPEAT):
                    cf.goTo([-1.,0.,0.], 0., 2., relative=True)
        timeHelper.sleep(2.5)

        # individual goTo command
        for cf_id in np.arange(1, num_robots+1, 1): # this loops the robot id
            # access the cf byID
            try:
                cf = cfs.crazyfliesById[cf_id]
            except:
                continue

            # identify the row index based on the robot id
            row_index = cf_id // num_robots_each_row
            # print(row_index%2)
            if (row_index % 2 == 0): # go left
                for i in range(NUM_COMMAND_REPEAT):
                    cf.goTo([-1.,0.,0.], 0., 2., relative=True)
            else: # go right
                for i in range(NUM_COMMAND_REPEAT):
                    cf.goTo([1.,0.,0.], 0., 2., relative=True)
        timeHelper.sleep(2.5)


    # land command
    cfs.land(targetHeight=0.04, duration=TAKEOFF_DURATION)
    timeHelper.sleep(TAKEOFF_DURATION + ACTION_GAP)

    # cf = cfs.crazyfliesById[0]
    # cf.takeoff(targetHeight=1.0, duration=TAKEOFF_DURATION)
    # timeHelper.sleep(2.5)
    # cf.goTo([1.,0.,0.], 0., 2., relative=True)
    # timeHelper.sleep(2.5)


    # for cf in cfs:
    #     cf.takeoff(targetHeight=1.0, duration=TAKEOFF_DURATION)
    # timeHelper.sleep(TAKEOFF_DURATION + HOVER_DURATION)

    # for cf in cfs:
    #     cf.goTo([1.,0.,0.], 0., 2., relative=True)
    # timeHelper.sleep(2.5)

    # for cf in cfs:
    #     cf.goTo([-1.,0.,0.], 0., 2., relative=True)
    # timeHelper.sleep(2.5)
    
    # for cf in cfs:
    #     cf.land(targetHeight=0.04, duration=2.5)
    # timeHelper.sleep(TAKEOFF_DURATION)


if __name__ == "__main__":
    main()
