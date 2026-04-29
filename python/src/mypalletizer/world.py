import json
import socket
from typing import Optional

from .objects import WorldObject
from .protocol import build_spawn_msg, build_delete_msg, build_clear_msg
from .errors import InvalidConfigError, WorldConnectionError
from .presets import PRESETS

class World:
    def __init__(self, ip: str = "127.0.0.1", udp_port: int = 5006):
        self.ip = ip
        self.udp_port = udp_port
        self.sock: Optional[socket.socket] = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self._validate()

    def spawn(self, obj: WorldObject):
        self._validate_object(obj)

        payload = build_spawn_msg(
            object_type=obj.object_type,
            name=obj.name,
            position=obj.position,
            rotation=obj.rotation,
            scale=obj.scale,
            color=obj.color,
            is_static=obj.is_static,
        )
        self._send_udp(payload)

    def delete(self, name: str):
        if not name or not name.strip():
            raise InvalidConfigError("Object name must not be empty.")
        self._send_udp(build_delete_msg(name.strip()))

    def clear(self):
        self._send_udp(build_clear_msg())

    def close(self):
        if self.sock:
            try:
                self.sock.close()
            finally:
                self.sock = None

    def __enter__(self) -> "World":
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        self.close()
        return False

    def _send_udp(self, payload: dict):
        if not self.sock:
            raise WorldConnectionError("World socket is closed.")

        data = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        self.sock.sendto(data, (self.ip, self.udp_port))

    def _validate(self):
        if not (1 <= self.udp_port <= 65535):
            raise InvalidConfigError("World udp_port must be in range 1..65535.")

    def list_presets(self) -> list[str]:
        return list(PRESETS.keys())

    def load_preset(self, name: str, clear_first: bool = True):
        if name not in PRESETS:
            raise InvalidConfigError(f"Unknown preset: {name}")

        if clear_first:
            self.clear()

        for obj in PRESETS[name]:
            self.spawn(obj)

    @staticmethod
    def _validate_object(obj: WorldObject):
        if not obj.name or not obj.name.strip():
            raise InvalidConfigError("Object name must not be empty.")

        if len(obj.position) != 3:
            raise InvalidConfigError("Position must contain exactly 3 values.")
        if len(obj.rotation) != 3:
            raise InvalidConfigError("Rotation must contain exactly 3 values.")
        if len(obj.scale) != 3:
            raise InvalidConfigError("Scale must contain exactly 3 values.")
        if len(obj.color) != 3:
            raise InvalidConfigError("Color must contain exactly 3 values.")

        sx, sy, sz = obj.scale
        if sx <= 0 or sy <= 0 or sz <= 0:
            raise InvalidConfigError("Scale values must be > 0.")