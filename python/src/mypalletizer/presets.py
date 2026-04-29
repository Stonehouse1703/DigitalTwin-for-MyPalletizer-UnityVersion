from .objects import Box, Cylinder, Sphere


PRESETS = {
    "empty": [],
    "three_blocks": [
        Box(
            name="box_red",
            position=(-2, 0.5, 0),
            scale=(0.5, 0.5, 0.5),
            color=(255, 0, 0),
        ),
        Box(
            name="box_green",
            position=(2, 0.5, 0),
            scale=(0.5, 0.5, 0.5),
            color=(0, 255, 0),
        ),
        Box(
            name="box_blue",
            position=(3, 0.5, 0),
            scale=(0.5, 0.5, 0.5),
            color=(0, 0, 255),
        ),
    ],
    "Base1": [
        Cylinder(
            name="A11",
            position=(-1.948, 0.1, -0.629),
            scale=(0.7, 0.06, 0.7),
            color=(163, 64, 255),
            is_static=True,
        ),
        Cylinder(
            name="A12",
            position=(-1.988, 0.1, 0.512),
            scale=(0.7, 0.06, 0.7),
            color=(163, 64, 255),
            is_static=True,
        ),
        Cylinder(
            name="A13",
            position=(-1.783, 0.1, 1.482),
            scale=(0.7, 0.06, 0.7),
            color=(163, 64, 255),
            is_static=True,
        ),
        Cylinder(
            name="A21",
            position=(1.897, 0.1, -0.629),
            scale=(0.6, 0.06, 0.6),
            color=(255, 255, 0),
            is_static=True,
        ),
        Cylinder(
            name="A22",
            position=(1.906, 0.1, 0.562),
            scale=(0.6, 0.06, 0.6),
            color=(255, 255, 0),
            is_static=True,
        ),
        Cylinder(
            name="A23",
            position=(1.695, 0.1, 1.482),
            scale=(0.6, 0.06, 0.6),
            color=(255, 255, 0),
            is_static=True,
        ),
        Cylinder(
            name="A31",
            position=(2.66, 0.1, -0.629),
            scale=(0.6, 0.06, 0.6),
            color=(0, 0, 255),
            is_static=True,
        ),
        Cylinder(
            name="A32",
            position=(2.67, 0.1, 0.562),
            scale=(0.6, 0.06, 0.6),
            color=(0, 0, 255),
            is_static=True,
        ),
        Cylinder(
            name="A33",
            position=(2.47, 0.1, 1.482),
            scale=(0.6, 0.06, 0.6),
            color=(0, 0, 255),
            is_static=True,
        ),
    ],
    "sorting_task": [
        Box(
            name="part_1",
            position=(0.18, 0.10, 0.10),
            scale=(0.04, 0.04, 0.04),
            color=(255, 0, 0),
        ),
        Box(
            name="part_2",
            position=(0.24, 0.10, 0.10),
            scale=(0.04, 0.04, 0.04),
            color=(0, 255, 0),
        ),
        Box(
            name="part_3",
            position=(0.30, 0.10, 0.10),
            scale=(0.04, 0.04, 0.04),
            color=(0, 0, 255),
        ),
        Sphere(
            name="zone_red",
            position=(0.25, -0.12, 0.10),
            scale=(0.05, 0.01, 0.05),
            color=(255, 100, 100),
            is_static=True,
        ),
    ],
}