import time

from src.mypalletizer import Robot, RobotMode

def main():
    # 1) Nur Simulation
    # robot = Robot.sim(ip="127.0.0.1", udp_port=5005)

    # 2) Nur real
    # robot = Robot.connect(port="COM7")

    # 3) Beides
    with Robot(mode=RobotMode.VIRTUAL, port="COM7") as robot:
        robot.send_coords([200, -200, 200, 0], 40)

        '''
        robot.send_angle(1, 90, speed=40)
        time.sleep(3)

        robot.set_color(0, 255, 0)
        robot.send_angles(0, 0, 0, 0, speed=40)
        time.sleep(3)

        robot.set_color(0, 0, 255)
        robot.send_angles(74, 85, 0, 0, speed=40)
        time.sleep(5)
        print(robot.get_angles())

        
        robot.set_color(255, 0, 255)
        robot.move_joints(-74, 85, 0, 0, speed=40)
        robot.sleep(3)

        robot.set_color(255, 0, 0)
        robot.move_joints(0, 0, 0, 0, speed=40)
        robot.sleep(3)

        robot.move_joints(160, 0, -60, 180, speed=100)
        robot.sleep(5)
        

        robot.sync_send_angles(-160, 0, 0, 180, speed=100)
        print(robot.get_angles())

        robot.sync_send_angles(0, 0, 0, 0, speed=120)
        print(robot.get_angles())
        '''

if __name__ == "__main__":
    main()