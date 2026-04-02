import sys
import os

# Add src to path for local execution without installation
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from mypalletizer import Robot, RobotMode, World, Box, Cylinder
from mypalletizer.robot import EndEffector


def main():
    with Robot(mode=RobotMode.VIRTUAL, ip="127.0.0.1", udp_port=5005) as robot:
        with World(ip="127.0.0.1", udp_port=5006) as world:

            robot.set_end_effector(EndEffector.PUMP)

            world.clear()
            world.load_preset("three_blocks")

            """
            world.spawn(
                Box(
                    name="box1",
                    position=(0.20, 0.05, 0.10),
                    scale=(0.05, 0.05, 0.05),
                    color=(255, 0, 0),
                )
            )

            world.spawn(
                Cylinder(
                    name="cyl1",
                    position=(0.25, -0.05, 0.10),
                    scale=(0.04, 0.08, 0.04),
                    color=(0, 0, 255),
                )
            )"""

            robot.set_color(0, 255, 0)
            #robot.send_angles(0, 0, 0, 0, 40)
            robot.sync_move_joints(-90, 30, 0, 0, 50)
            robot.sync_move_joints(-90, 35, 0, 0, 20)
            robot.sleep(4)
            robot.pump_on()
            robot.set_gripper_state(1,50)
            robot.sleep(1)
            robot.sync_move_joints(0, 35, 0, 0, 40)
            robot.sleep(2)
            robot.pump_off()
            robot.set_gripper_state(0, 50)
            robot.sleep(1)

            robot.sync_move_joints(90, 30, 0, 0, 50)
            robot.sync_move_joints(90, 35, 0, 0, 20)
            robot.sleep(4)
            robot.pump_on()
            robot.set_gripper_state(1, 50)
            robot.sleep(1)
            robot.sync_move_joints(0, 25, 0, 0, 40)
            robot.sleep(2)
            robot.pump_off()
            robot.set_gripper_state(0, 50)
            robot.sleep(1)

            robot.sync_move_joints(0, 0, 0, 0, 50)
            robot.sync_move_joints(90, 62, -90, 0, 50)
            robot.sync_move_joints(90, 69, -90, 0, 20)
            robot.sleep(4)
            robot.pump_on()
            robot.set_gripper_state(1, 50)
            robot.sleep(2)
            robot.sync_move_joints(0, 25, 0, 0, 40)
            robot.sleep(5)
            robot.pump_off()
            robot.set_gripper_state(0, 50)
            robot.sleep(2)

            robot.sync_move_joints(90, 50, 0, 0, 50)
            robot.sync_move_joints(-90, 50, 0, 0, 50)





if __name__ == "__main__":
    main()