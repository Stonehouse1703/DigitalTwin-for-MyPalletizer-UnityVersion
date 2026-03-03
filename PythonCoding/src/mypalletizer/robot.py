from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from parso.python.tree import String

from .controller import MyPalletizerController
from .errors import InvalidConfigError


class RobotMode(str, Enum):
    VIRTUAL = "virtual"
    REAL = "real"
    BOTH = "both"


@dataclass(frozen=True)
class RobotConfig:
    mode: RobotMode
    port: Optional[str] = None
    ip: str = "127.0.0.1"
    udp_port: int = 5005
    baudrate: int = 115200


class Robot:
    """
    Student-facing API.
    """

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

    # ---------------- API ----------------

    def send_angle(self, id: int, degree: float, speed: int = 40):
        self._impl.send_angle(id, degree, speed=speed)

    def send_angles(self, j1: float, j2: float, j3: float, j4: float, speed: int = 40):
        self._impl.send_angles(j1, j2, j3, j4, speed=speed)

    def sync_send_angles(self, j1: float, j2: float, j3: float, j4: float, speed: int = 40):
        self._impl.sync_send_angles(j1, j2, j3, j4, speed=speed)

    def set_color(self, r: int, g: int, b: int):
        self._impl.set_color(r, g, b)

    def get_angles(self) -> String:
        return self._impl.get_angles()

    def close(self):
        self._impl.close()

    # Context manager support
    def __enter__(self) -> "Robot":
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        self.close()
        return False

    # ---------------- Validation ----------------

    @staticmethod
    def _validate(cfg: RobotConfig):
        if cfg.mode in (RobotMode.REAL, RobotMode.BOTH) and not cfg.port:
            raise InvalidConfigError(
                "Mode REAL or BOTH requires a serial port (e.g. port='COM7')."
            )

        if not (1 <= cfg.udp_port <= 65535):
            raise InvalidConfigError("udp_port must be in range 1..65535.")