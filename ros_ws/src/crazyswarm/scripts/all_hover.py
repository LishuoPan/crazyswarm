"""Takeoff-hover-land for one CF. Useful to validate hardware config."""

from pycrazyswarm import Crazyswarm


TAKEOFF_DURATION = 2.5
HOVER_DURATION = 5.0


def main():
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    cfs = swarm.allcfs.crazyflies
    # cf = swarm.allcfs.crazyflies[0]
    for cf in cfs:
        cf.takeoff(targetHeight=1.0, duration=TAKEOFF_DURATION)
    timeHelper.sleep(TAKEOFF_DURATION + HOVER_DURATION)

    for cf in cfs:
        cf.goTo([1.,0.,0.], 0., 2., relative=True)
    timeHelper.sleep(2.5)

    for cf in cfs:
        cf.goTo([-1.,0.,0.], 0., 2., relative=True)
    timeHelper.sleep(2.5)
    
    for cf in cfs:
        cf.land(targetHeight=0.04, duration=2.5)
    timeHelper.sleep(TAKEOFF_DURATION)


if __name__ == "__main__":
    main()
