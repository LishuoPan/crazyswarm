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

# read in the json
f = open('../data/simulation.json')
data = json.load(f)

num_timesteps = len(data)
num_robots = len(data[0]["robot_data"])

time_info = np.zeros(num_timesteps) # holds time values
robot_position_info = np.zeros((num_timesteps, num_robots, 3)) # holds robot position values
# the robot's id should be the same as the index
# there is an assert statement to verify this, in case anything changes in the simulation code

for timestep_index, timestep_log in enumerate(data): 
    # contents of timestep_log
    # timestep_log["planner_data"]
    # timestep_log["robot_data"] per robot info
    # timestep_log["timestamp"]

    time_info[timestep_index] = timestep_log["timestamp"]

    for robot_index, robot_log in enumerate(timestep_log["robot_data"]): 
        #  print(timestep_log["robot_data"].keys())
        assert(robot_index == robot_log["robot_id"])
        robot_position_info[timestep_index][robot_index] = np.asarray(robot_log["cur_pos"])


TIME = time_info*5
ALL_WAYPOINTS = robot_position_info



print("time info: ", time_info)
print("num timesteps: ", num_timesteps)
print("robot_position_info.shape: ", robot_position_info.shape)

print(ALL_WAYPOINTS[:,0,:])
print()
print(ALL_WAYPOINTS[:,1,:])


def main():
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    # Start the mission
    allcfs.takeoff(Z, TAKEOFF_DURATION)
    timeHelper.sleep(TAKEOFF_DURATION + 1)

    # Get the number of timesteps
    num_timesteps = len(TIME)
    num_drones = len(allcfs.crazyflies)

    # Assign positions to each drone at each timestep
    for t in range(1, num_timesteps):
        for i in range(num_drones): 
            # Gets the correct crazyflie 
            WAYPOINTS = ALL_WAYPOINTS[:,i,:] 
            # Get the positions for the current timestep
            positions = WAYPOINTS[t, :] # Gets a vector of all the row values in a specifc column t

            cf = allcfs.crazyflies[i]
            cf.goTo([positions[0], positions[1], positions[2]], 0.0, (TIME[t] - TIME[t-1]))
        timeHelper.sleep((TIME[t] - TIME[t-1])-0.8)

    # Land the drones
    allcfs.land(TARGET_HEIGHT, LAND_DURATION)
    timeHelper.sleep(LAND_DURATION + 1)

if __name__ == "__main__":
    main()
