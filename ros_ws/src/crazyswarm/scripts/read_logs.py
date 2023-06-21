import json
import numpy as np
  
f = open('../../../data/simulation.json')
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

print("time info: ", time_info)
print("num timesteps: ", num_timesteps)
print("robot_position_info.shape: ", robot_position_info.shape)

