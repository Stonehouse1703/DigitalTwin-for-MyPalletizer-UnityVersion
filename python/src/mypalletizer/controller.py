import json
import socket
import time
from typing import Optional
from enum import Enum
from pymycobot import MyPalletizer260

from .protocol import (
    build_led_msg,
    build_move_msg,
    sync_build_move_msg,
    build_set_end_effector_msg,
    build_set_gripper_state_msg,
    build_pump_msg,
)

from .errors import RobotConnectionError


class MyPalletizerController:
    _JOINT_LIMITS = {
        "j1": (-160.0, 160.0),
        "j2": (0.0, 90.0),
        "j3": (-60.0, 0.0),
        "j4": (-360.0, 360.0),
    }

    def __init__(self, mode: str, port: Optional[str], ip: str, udp_port: int, baudrate: int = 115200):
        self.mode = mode
        self.mc: Optional[MyPalletizer260] = None
        self.sock: Optional[socket.socket] = None
        self.udp_ip = ip
        self.udp_port = udp_port
        self._sim_angles: list[float] = [0.0, 0.0, 0.0, 0.0]

        if mode in ("real", "both"):
            try:
                self.mc = MyPalletizer260(port, baudrate)
                time.sleep(2)
                self.mc.power_on()
                time.sleep(0.5)
                print(f"Connected to robot on port {port}")
            except Exception as e:
                raise RobotConnectionError(f"Could not connect to robot on port {port}.") from e

        if mode in ("virtual", "both"):
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        print(f"Starting in mode: {mode}")

    def send_angles(self, j1, j2, j3, j4, speed=40):
        j1 = self._clamp("j1", j1)
        j2 = self._clamp("j2", j2)
        j3 = self._clamp("j3", j3)
        j4 = self._clamp("j4", j4)
        speed = self._clamp_speed(speed)

        self._sim_angles = [j1, j2, j3, j4]

        if self.sock:
            self._send_udp(build_move_msg(j1, j2, j3, j4, speed))

        if self.mc:
            self.mc.send_angles([j1, j2, j3, j4], speed)

    def send_angle(self, id, degree, speed=40):
        joint_name = f"j{id}"
        if joint_name not in self._JOINT_LIMITS:
            raise ValueError(f"Invalid joint id: {id}. Expected 1..4.")

        degree = self._clamp(joint_name, degree)
        speed = self._clamp_speed(speed)

        if self.sock and not self.mc:
            raise NotImplementedError("send_angle is not implemented for virtual-only mode.")

        if self.mc:
            self.mc.send_angle(id, degree, speed)

            if 1 <= id <= 4:
                self._sim_angles[id - 1] = degree

    def sync_move_joints(self, j1, j2, j3, j4, speed=40):
        j1 = self._clamp("j1", j1)
        j2 = self._clamp("j2", j2)
        j3 = self._clamp("j3", j3)
        j4 = self._clamp("j4", j4)
        speed = self._clamp_speed(speed)

        self._sim_angles = [j1, j2, j3, j4]

        if self.sock:
            self._send_udp(sync_build_move_msg(j1, j2, j3, j4, speed))

        if self.mc:
            self.mc.sync_send_angles([j1, j2, j3, j4], speed)

    def set_color(self, r, g, b):
        r, g, b = self._clamp_rgb(r, g, b)

        if self.sock:
            self._send_udp(build_led_msg(r, g, b))

        if self.mc:
            self.mc.set_color(r, g, b)

    def get_angles(self) -> str:
        if self.mode == "virtual":
            return (
                f"j1: {self._sim_angles[0]:.1f}, "
                f"j2: {self._sim_angles[1]:.1f}, "
                f"j3: {self._sim_angles[2]:.1f}, "
                f"j4: {self._sim_angles[3]:.1f}"
            )

        if self.mode == "real":
            if self.mc:
                angles = self.mc.get_angles()
                return (
                    f"j1: {angles[0]:.1f}, "
                    f"j2: {angles[1]:.1f}, "
                    f"j3: {angles[2]:.1f}, "
                    f"j4: {angles[3]:.1f}"
                )
            raise RobotConnectionError("Not connected to robot.")

        if self.mode == "both":
            if self.mc:
                angles = self.mc.get_angles()
                return (
                    f"Real - j1: {angles[0]:.1f}, j2: {angles[1]:.1f}, "
                    f"j3: {angles[2]:.1f}, j4: {angles[3]:.1f}\n"
                    f"Sim  - j1: {self._sim_angles[0]:.1f}, j2: {self._sim_angles[1]:.1f}, "
                    f"j3: {self._sim_angles[2]:.1f}, j4: {self._sim_angles[3]:.1f}"
                )
            raise RobotConnectionError("Not connected to robot.")

        raise RobotConnectionError(f"Unknown mode: {self.mode}")

    def sleep(self, seconds: float):
        time.sleep(max(0.0, float(seconds)))

    def close(self):
        if self.sock:
            try:
                self.sock.close()
            finally:
                self.sock = None

        if self.mc:
            try:
                close_fn = getattr(self.mc, "close", None)
                if callable(close_fn):
                    close_fn()
            finally:
                self.mc = None

    def _send_udp(self, payload: dict):
        if not self.sock:
            raise RobotConnectionError("UDP socket is not available.")
        data = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        self.sock.sendto(data, (self.udp_ip, self.udp_port))

    def _clamp(self, joint: str, angle: float) -> float:
        lo, hi = self._JOINT_LIMITS[joint]
        a = float(angle)
        if a < lo:
            return lo
        if a > hi:
            return hi
        return a

    def set_end_effector(self, tool):
        if isinstance(tool, Enum):
            tool = tool.value

        tool = str(tool).strip().lower()

        if tool not in ("gripper", "pump"):
            raise ValueError("tool must be 'gripper' or 'pump'.")

        if self.sock:
            self._send_udp(build_set_end_effector_msg(tool))

    def set_gripper_state(self, flag: int, speed: int, _type_1: int = 1):
        flag = int(flag)
        speed = self._clamp_speed(speed)
        _type_1 = int(_type_1)

        if flag not in (0, 1, 254):
            raise ValueError("flag must be 0 (open), 1 (close), or 254 (release).")

        if self.sock:
            self._send_udp(build_set_gripper_state_msg(flag, speed, _type_1))

        if self.mc:
            self.mc.set_gripper_state(flag, speed, _type_1)

    def pump_on(self):
        if self.sock:
            self._send_udp(build_pump_msg(True))

        if self.mc:
            self.mc.set_basic_output(2, 0)
            self.mc.set_basic_output(5, 0)

    def pump_off(self):
        if self.sock:
            self._send_udp(build_pump_msg(False))

        if self.mc:
            self.mc.set_basic_output(2, 1)
            self.mc.set_basic_output(5, 1)

    @staticmethod
    def _clamp_speed(speed: int) -> int:
        s = int(speed)
        if s < 1:
            return 1
        if s > 100:
            return 100
        return s

    @staticmethod
    def _clamp_rgb(r: int, g: int, b: int):
        def c(x):
            x = int(x)
            return 0 if x < 0 else 255 if x > 255 else x

        return c(r), c(g), c(b)