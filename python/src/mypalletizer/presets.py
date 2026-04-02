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
        Cylinder(
            name="cylinder_L1",
            position=(-2, 0, 0),
            scale=(0.5, 0.1, 0.5),
            color=(120, 120, 120),
        ),
    ],
    "pick_and_place_basic": [
        Box(
            name="pickup_box",
            position=(0.22, 0.08, 0.10),
            scale=(0.04, 0.04, 0.04),
            color=(255, 140, 0),
        ),
        Cylinder(
            name="target_zone",
            position=(0.32, -0.08, 0.10),
            scale=(0.08, 0.01, 0.08),
            color=(120, 120, 120),
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
        ),
    ],
}