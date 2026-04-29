import sys
import os

import time

# Add src to path for local execution without installation
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from mypalletizer import Robot, RobotMode, World, Box, Cylinder
from mypalletizer.robot import EndEffector


def main():
    with Robot(mode=RobotMode.VIRTUAL, ip="127.0.0.1", udp_port=5005) as robot:
        with World(ip="127.0.0.1", udp_port=5006) as world:

            #Set Gripper State -> (Gripper or Pump)
            robot.set_end_effector(EndEffector.PUMP)

            #Set up a World
            world.clear()
            world.load_preset("Base1")
            time.sleep(3)

            # You can also generate Pieces (Box, Cylinder, Sphere)
            '''
            world.spawn(
                Cylinder(
                    name="A31",
                    position=(0, 0.1, -1.5),
                    scale=(0.6, 0.06, 0.6),
                    color=(0, 255, 255), #RGB
                )
            )
            '''

            # Move to initial Point
            robot.send_angles(0,0,0,0,80)
            time.sleep(5)

            # Move to every point

            # Move to Point 11
            robot.send_angles(-72,40,20,0,80)
            # i recoment to make after every move a timeout!
            time.sleep(1)
            robot.send_angles(-72, 50, 25, 0,80)
            time.sleep(3)
            robot.send_angles(-72, 40, 20, 0, 80)
            time.sleep(1)

            # Move to Point 12
            robot.send_angles(-107, 40, 15, 0, 80)
            # i recoment to make after every move a timeout!
            time.sleep(1)
            robot.send_angles(-107, 50, 25, 0, 80)
            time.sleep(3)
            robot.send_angles(-107, 40, 15, 0, 80)
            time.sleep(1)

            # Move to Point 13
            robot.send_angles(-135, 50, -5, 0, 80)
            # i recoment to make after every move a timeout!
            time.sleep(1)
            robot.send_angles(-135, 55, 5, 0, 80)
            time.sleep(3)
            robot.send_angles(-135, 50, -5, 0, 80)
            time.sleep(1)

            # Move to Point 21
            robot.send_angles(72, 40, 20, 0, 80)
            # i recoment to make after every move a timeout!
            time.sleep(2)
            robot.send_angles(72, 50, 25, 0, 80)
            time.sleep(3)
            robot.send_angles(72, 40, 20, 0, 80)
            time.sleep(1)

            # Move to Point 22
            robot.send_angles(107, 50, 15, 0, 80)
            # i recoment to make after every move a timeout!
            time.sleep(1)
            robot.send_angles(107, 50, 25, 0, 80)
            time.sleep(3)
            robot.send_angles(107, 50, 15, 0, 80)
            time.sleep(1)

            # Move to Point 23
            robot.send_angles(135, 50, -5, 0, 80)
            # i recoment to make after every move a timeout!
            time.sleep(1)
            robot.send_angles(135, 55, 5, 0, 80)
            time.sleep(3)
            robot.send_angles(135, 50, -5, 0, 80)
            time.sleep(2)

            # Move to Point 31
            robot.send_angles(77, 0, 0, 0, 80)
            # i recoment to make after every move a timeout!
            time.sleep(2)
            robot.send_angles(77, 70, -40, 0, 80)
            time.sleep(3)
            robot.send_angles(77, 0, 0, 0, 80)
            time.sleep(2)

            # Move to Point 32
            robot.send_angles(103, 0, 0, 0, 80)
            # i recoment to make after every move a timeout!
            time.sleep(2)
            robot.send_angles(103, 70, -30, 0, 80)
            time.sleep(3)
            robot.send_angles(103, 0, 0, 0, 80)
            time.sleep(2)

            # Move to Point 33
            robot.send_angles(120, 0, 0, 0, 80)
            # i recoment to make after every move a timeout!
            time.sleep(2)
            robot.send_angles(120, 80, -55, 0, 80)
            time.sleep(3)
            robot.send_angles(120, 0, 0, 0, 80)
            time.sleep(2)

if __name__ == "__main__":
    main()