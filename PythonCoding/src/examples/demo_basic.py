from mypalletizer import Robot, RobotMode, World, Box, Cylinder


def main():
    with Robot(mode=RobotMode.VIRTUAL, ip="127.0.0.1", udp_port=5005) as robot:
        with World(ip="127.0.0.1", udp_port=5006) as world:
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
            robot.send_angles(0, 0, 0, 0, 40)
            robot.sleep(3)

            robot.set_color(0, 0, 255)
            robot.send_angles(74, 85, 0, 0, 40)
            robot.sleep(5)

            print(robot.get_angles())

            robot.sync_move_joints(-160, 0, 0, 180, 100)
            print(robot.get_angles())

            robot.sync_move_joints(0, 0, 0, 0, 100)
            print(robot.get_angles())


if __name__ == "__main__":
    main()