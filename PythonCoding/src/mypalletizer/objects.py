from dataclasses import dataclass
from typing import Tuple

Vec3 = Tuple[float, float, float]
Rgb = Tuple[int, int, int]


@dataclass
class WorldObject:
    name: str
    position: Vec3
    rotation: Vec3 = (0.0, 0.0, 0.0)
    scale: Vec3 = (1.0, 1.0, 1.0)
    color: Rgb = (255, 255, 255)

    @property
    def object_type(self) -> str:
        raise NotImplementedError("Subclasses must define object_type.")


@dataclass
class Box(WorldObject):
    scale: Vec3 = (0.05, 0.05, 0.05)

    @property
    def object_type(self) -> str:
        return "box"


@dataclass
class Sphere(WorldObject):
    scale: Vec3 = (0.05, 0.05, 0.05)

    @property
    def object_type(self) -> str:
        return "sphere"


@dataclass
class Cylinder(WorldObject):
    scale: Vec3 = (0.05, 0.08, 0.05)

    @property
    def object_type(self) -> str:
        return "cylinder"