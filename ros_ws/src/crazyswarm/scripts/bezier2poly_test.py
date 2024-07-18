#!/usr/bin/env python
import json
import numpy as np
import yaml

from pycrazyswarm import *
import uav_trajectory
import colorsys

if __name__ == "__main__":

    def generateRGBColors(num_colors):
        output = []
        num_colors += 1 # to avoid the first color
        for index in range(1, num_colors):
            incremented_value = 1.0 * index / num_colors
            output.append(colorsys.hsv_to_rgb(incremented_value, 0.75, 0.75))
        return np.asarray(output)

    # Environment constants
    Z = 1.0
    TAKEOFF_DURATION = 2.5
    TARGET_HEIGHT = 0.02
    ALL_TRAJ_PATH = "./cf_trajectories/10piece_result/"
    num_robots = 24  ## TODO change to read
    TIMESCALE = 1.0

    with open('../launch/allCrazyflies_demo_new.yaml', 'r') as f:
        allcfs_yaml = yaml.load(f)
        my_cfs = allcfs_yaml['crazyflies']
        indices_dict = {cf['id']: i for i, cf in enumerate(my_cfs)}
    with open('../launch/crazyflies.yaml') as f:
        cfs_yaml = yaml.load(f)
        robot_ids = [cf['id'] for cf in cfs_yaml['crazyflies']]
        print("robot_ids:", robot_ids)
    
    robot_indices = [int(indices_dict[r]) for r in robot_ids]
    print("robot_indices: ", robot_indices)

    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs
    assert(len(allcfs.crazyflies) == num_robots)

    all_trajs = []
    max_duration = 0
    for traj_index in robot_indices:
        traj = uav_trajectory.Trajectory()
        traj.loadcsv(ALL_TRAJ_PATH + "cf_trajectory_" + str(traj_index) + ".csv")
        max_duration = max(max_duration, traj.duration)
        all_trajs.append(traj)

    for cf_index, cf in enumerate(allcfs.crazyflies):
        cf.uploadTrajectory(0, 0, all_trajs[cf_index])

    allcfs.takeoff(targetHeight=1.0, duration=2.0)
    timeHelper.sleep(2.5)
    for cf in allcfs.crazyflies:
        pos = np.array(cf.initialPosition) + np.array([0, 0, 1.0])
        cf.goTo(pos, 0, 2.0)
    timeHelper.sleep(2.5)
    
    print("start trajectory")
    allcfs.startTrajectory(0, timescale=TIMESCALE)
    timeHelper.sleep(max_duration * TIMESCALE + 2.0)
    
    allcfs.land(targetHeight=0.06, duration=2.0)
    timeHelper.sleep(3.0)
