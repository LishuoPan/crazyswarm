import numpy as np

import json

# V1

from pycrazyswarm import *
# V2

# from crazyflie_py import Crazyswarm

# Environment constants
Z = 1.0
TAKEOFF_DURATION = 2.5
TARGET_HEIGHT = 0.02
GOTO_DURATION = 3.0
LAND_DURATION = 3.0
TIME = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0])

WAYPOINTS_R1 = np.array([
    [1.0, 1.0, 1.0, 1.0, 1.5, 1.5, 1.5, 1.5, 1.0, 0.5],
    [0.0, 0.5, 1.0, 1.5, 1.5, 1.0, 0.5, 0.0, 0.0, 0.0],
    [Z, Z, Z, Z, Z, Z, Z, Z, Z, Z]
    ])
WAYPOINTS_R2 = np.array([
    [-1.0, -1.0, -1.0, -1.0, -1.0,-1.0, -1.0, -1.0, -1.0, -1.0],
    [0.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 1.0, 1.0],
    [Z, Z, Z, Z, Z, Z, Z, Z, Z, Z]
    ])
WAYPOINTS_R3 = np.array([
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0],
    [Z, Z, Z, Z, Z, Z, Z, Z, Z, Z]
    ])
ALL_WAYPOINTS = [WAYPOINTS_R1, WAYPOINTS_R2, WAYPOINTS_R3]

def main():
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    # Start the mission
    allcfs.takeoff(Z, TAKEOFF_DURATION)
    timeHelper.sleep(TAKEOFF_DURATION + 1)

    # Get the number of timesteps
    num_timesteps = len(TIME)
    num_drones = len(ALL_WAYPOINTS)

    # Assign positions to each drone at each timestep

    for t in range(1, num_timesteps):
        for i in range(num_drones): 
            
            # Get the positions for the current timestep
            
            WAYPOINTS = ALL_WAYPOINTS[i]
            positions = WAYPOINTS[:, t] # Gets a vector of all the row values in a specifc column t

            cf = allcfs.crazyflies[i]
            
            cf.goTo([positions[0], positions[1], positions[2]], 0.0, (TIME[t] - TIME[t-1]))

        timeHelper.sleep((TIME[t] - TIME[t-1] + 0.5))

    # Land the drones
    allcfs.land(TARGET_HEIGHT, LAND_DURATION)
    timeHelper.sleep(LAND_DURATION + 1)

if __name__ == "__main__":
    main()