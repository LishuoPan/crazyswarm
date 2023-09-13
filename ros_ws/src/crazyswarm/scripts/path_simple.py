import numpy as np

import json
import random
# V1
from pycrazyswarm import *
import yaml
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

with open('../launch/allCrazyflies_demo.yaml', 'r') as f:
    allcfs = yaml.load(f)
    my_cfs = allcfs['crazyflies']
    indices_dict = {cf['id']: i for i, cf in enumerate(my_cfs)}

TIME = time_info*5
with open('../launch/crazyflies.yaml') as f:
    mycfs = yaml.load(f)
    robot_ids = [cf['id'] for cf in mycfs['crazyflies']]
    print(robot_ids)
# robot_ids = [13, 21, 23, 24, 25, 27, 28, 30, 31, 33, 34, 35, 36, 38, 40, 41, 43, 44, 47, 50]
robot_indices = [int(indices_dict[r]) for r in robot_ids]
robot_position_info = np.array(robot_position_info)
ALL_WAYPOINTS = robot_position_info[:, robot_indices, :]

# print("time info: ", time_info)
# print("num timesteps: ", num_timesteps)
# print("robot_position_info.shape: ", robot_position_info.shape)

# print(ALL_WAYPOINTS[:,0,:])
# print()
# print(ALL_WAYPOINTS[:,1,:])


def main():
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs
    


    # Get the number of timesteps
    num_timesteps = len(TIME)
    num_drones = np.minimum(len(allcfs.crazyflies), ALL_WAYPOINTS.shape[1])

    for cf in allcfs.crazyflies:
        cf.setParam("ring/effect", 7)
    
    rgb_bits = [tuple((x >> k) & 0x1 for k in range(3)) for x in range(8)]
    rgb_bits.pop(0) 
    # rgb_bits = [(x / 49, (x // 7) / 7, (x % 7) / 7) for x in range(50)]

    for cf, rgb in zip(allcfs.crazyflies, rgb_bits):
        cf.setLEDColor(*rgb)
        # print(*rgb)

    # Start the mission
    allcfs.takeoff(Z, TAKEOFF_DURATION)
    timeHelper.sleep(TAKEOFF_DURATION + 1)

    # Assign positions to each drone at each timestep
    for t in range(1, num_timesteps):
        for i in range(num_drones): 
            # Gets the correct crazyflie 
            WAYPOINTS = ALL_WAYPOINTS[:,i,:] 
            # Get the positions for the current timestep
            positions = WAYPOINTS[t, :] # Gets a vector of all the row values in a specifc column t
            cf = allcfs.crazyflies[i]
            cf.goTo([positions[0], positions[1], positions[2]], 0.0, (TIME[t] - TIME[t-1]))
        timeHelper.sleep((TIME[t] - TIME[t-1]))

    # Land the drones
    allcfs.land(TARGET_HEIGHT, LAND_DURATION)
    timeHelper.sleep(LAND_DURATION + 1)

if __name__ == "__main__":
    main()


# def get_color(id, allcfs, timeHelper):
#  # rgb_bits = [tuple((x >> k) & 0x1 for k in range(3)) for x in range(num_robots)]
#     rgb_bits = [(x / 49, (x // 7) / 7, (x % 7) / 7) for x in range(50)]
#     print(rgb_bits)

#     for cf in allcfs.crazyflies:
#         for rgb in rgb_bits:
#             cf.setLEDColor(*rgb)
#         timeHelper.sleep(1.0)





