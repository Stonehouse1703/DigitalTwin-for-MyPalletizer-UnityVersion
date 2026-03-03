import json
import socket
import time
from typing import Optional
from pymycobot import MyPalletizer260
from .errors import RobotConnectionError

from .protocol import (
    build_led_msg,
    build_move_msg,
    sync_build_move_msg,
    build_move_angle_msg,
    build_move_coord_msg,
    build_move_coords_msg,
)

class MyPalletizerController:

    _JOINT_LIMITS = {
        "j1": (-160.0, 160.0),
        "j2": (0, 90.0),
        "j3": (-60, 0),
        "j4": (-360.0, 360.0),
    }

    _COORD_LIMITS = {
        "x": (-260.0, 260.0),
        "y": (-260.0, 260.0),
        "z": (-15.0, 357.58),
        "rx": (-180.0, 180.0),
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
                print("✅ Connected to robot on port", port)
            except Exception as e:
                raise RobotConnectionError(f"Could not connect to robot on port {port}.") from e

        if mode in ("virtual", "both"):
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        print("🛫 Starting in mode:", mode)

    #Todo: die Methode de no uselösche:
    def test(self):
        self.mc.send_coords([60,150,50,0],40)

    def send_angle(self, id: int, degree: float, speed=40):
        if self.sock:
            self._send_udp(build_move_angle_msg(id, degree, speed))

        if self.mc:
            self.mc.send_angle(id, degree, speed)

    def send_angles(self, j1, j2, j3, j4, speed=40):
        self._sim_angles = [j1, j2, j3, j4]
        j1 = self._clamp("j1", j1)
        j2 = self._clamp("j2", j2)
        j3 = self._clamp("j3", j3)
        j4 = self._clamp("j4", j4)
        speed = self._clamp_speed(speed)

        if self.sock:
            self._send_udp(build_move_msg(j1, j2, j3, j4, speed))

        if self.mc:
            self.mc.send_angles([j1, j2, j3, j4], speed)


    def sync_send_angles(self, j1, j2, j3, j4, speed=40):
        self._sim_angles = [j1, j2, j3, j4]
        j1 = self._clamp("j1", j1)
        j2 = self._clamp("j2", j2)
        j3 = self._clamp("j3", j3)
        j4 = self._clamp("j4", j4)
        speed = self._clamp_speed(speed)

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
            return f"j1: {self._sim_angles[0]:.1f}, j2: {self._sim_angles[1]:.1f}, j3: {self._sim_angles[2]:.1f}, j4: {self._sim_angles[3]:.1f}"

        if self.mode == "real":
            if self.mc:
                angles = self.mc.get_angles()
                return f"j1: {angles[0]:.1f}, j2: {angles[1]:.1f}, j3: {angles[2]:.1f}, j4: {angles[3]:.1f}"
            else:
                raise RobotConnectionError("Not connected to robot.")

        if self.mode == "both":
            if self.mc:
                angles = self.mc.get_angles()
                return f"Real - j1: {angles[0]:.1f}, j2: {angles[1]:.1f}, j3: {angles[2]:.1f}, j4: {angles[3]:.1f} \nSim - j1: {self._sim_angles[0]:.1f}, j2: {self._sim_angles[1]:.1f}, j3: {self._sim_angles[2]:.1f}, j4: {self._sim_angles[3]:.1f}"
            else:
                raise RobotConnectionError("Not connected to robot.")

    def send_coord(self, coord_id: int, coord: float, speed=40):
        """
        id: 1..4 => [x, y, z, rx]
        """
        speed = self._clamp_speed(speed)

        coord_id = int(coord_id)
        if coord_id not in (1, 2, 3, 4):
            raise ValueError("coord_id must be 1..4 (1=x,2=y,3=z,4=rx)")

        name_by_id = {1: "x", 2: "y", 3: "z", 4: "rx"}
        name = name_by_id[coord_id]
        coord = self._clamp_coord(name, coord)

        if self.sock:
            self._send_udp(build_move_coord_msg(coord_id, coord, speed))

        if self.mc:
            # pymycobot API: send_coord(id, coord, speed)
            self.mc.send_coord(coord_id, coord, speed)

    def send_coords(self, coords, speed=40):
        """
        coords: [x,y,z,rx]
        """
        speed = self._clamp_speed(speed)
        if coords is None or len(coords) != 4:
            raise ValueError("coords must be a list [x,y,z,rx] of length 4")

        x = self._clamp_coord("x", coords[0])
        y = self._clamp_coord("y", coords[1])
        z = self._clamp_coord("z", coords[2])
        rx = self._clamp_coord("rx", coords[3])

        if self.sock:
            self._send_udp(build_move_coords_msg(x, y, z, rx, speed))

        if self.mc:
            # pymycobot API: send_coords([x,y,z,rx], speed)
            self.mc.send_coords([x, y, z, rx], speed)

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
        data = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        self.sock.sendto(data, (self.udp_ip, self.udp_port))

    def _clamp(self, joint: str, angle: float) -> float:
        lo, hi = self._JOINT_LIMITS[joint]
        a = float(angle)
        if a < lo: return lo
        if a > hi: return hi
        return a

    def _clamp_coord(self, name: str, value: float) -> float:
        lo, hi = self._COORD_LIMITS[name]
        v = float(value)
        if v < lo: return lo
        if v > hi: return hi
        return v

    @staticmethod
    def _clamp_speed(speed: int) -> int:
        s = int(speed)
        if s < 1: return 1
        if s > 100: return 100
        return s

    @staticmethod
    def _clamp_rgb(r: int, g: int, b: int):
        def c(x):
            x = int(x)
            return 0 if x < 0 else 255 if x > 255 else x
        return c(r), c(g), c(b)