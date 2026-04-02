from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from .controller import MyPalletizerController
from .errors import InvalidConfigError


class RobotMode(str, Enum):
    VIRTUAL = "virtual"
    REAL = "real"
    BOTH = "both"

class EndEffector(str, Enum):
    PUMP = "pump"
    GRIPPER = "gripper"


@dataclass(frozen=True)
class RobotConfig:
    mode: RobotMode
    port: Optional[str] = None
    ip: str = "127.0.0.1"
    udp_port: int = 5005
    baudrate: int = 115200


class Robot:
    def __init__(
        self,
        *,
        mode: RobotMode,
        port: Optional[str] = None,
        ip: str = "127.0.0.1",
        udp_port: int = 5005,
        baudrate: int = 115200,
    ):
        config = RobotConfig(
            mode=mode,
            port=port,
            ip=ip,
            udp_port=udp_port,
            baudrate=baudrate,
        )

        self._validate(config)
        self.config = config

        self._impl = MyPalletizerController(
            mode=config.mode.value,
            port=config.port,
            ip=config.ip,
            udp_port=config.udp_port,
            baudrate=config.baudrate,
        )

    def send_angles(self, j1: float, j2: float, j3: float, j4: float, speed: int = 40):
        self._impl.send_angles(j1, j2, j3, j4, speed=speed)

    def send_angle(self, id: int, degree: float, speed: int = 40):
        self._impl.send_angle(id, degree, speed=speed)

    def sync_move_joints(self, j1: float, j2: float, j3: float, j4: float, speed: int = 40):
        self._impl.sync_move_joints(j1, j2, j3, j4, speed=speed)

    def set_color(self, r: int, g: int, b: int):
        self._impl.set_color(r, g, b)

    def get_angles(self) -> str:
        return self._impl.get_angles()

    def sleep(self, seconds: float):
        self._impl.sleep(seconds)

    def close(self):
        self._impl.close()

    def set_end_effector(self, tool: str):
        self._impl.set_end_effector(tool)

    def set_gripper_state(self, flag: int, speed: int, _type_1: int = 1):
        self._impl.set_gripper_state(flag, speed, _type_1)

    def pump_on(self):
        self._impl.pump_on()

    def pump_off(self):
        self._impl.pump_off()

    def __enter__(self) -> "Robot":
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        self.close()
        return False

    @staticmethod
    def _validate(cfg: RobotConfig):
        if cfg.mode in (RobotMode.REAL, RobotMode.BOTH) and not cfg.port:
            raise InvalidConfigError(
                "Mode REAL or BOTH requires a serial port (e.g. port='COM7' or '/dev/ttyUSB0')."
            )

        if not (1 <= cfg.udp_port <= 65535):
            raise InvalidConfigError("udp_port must be in range 1..65535.")