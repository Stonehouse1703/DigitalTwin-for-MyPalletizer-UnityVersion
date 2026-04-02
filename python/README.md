# MyPalletizer Python API

This is the official Python library for controlling the MyPalletizer 260 M5 robot, both in simulation (Unity) and real hardware.

## Installation

To use this library, it is recommended to install it in a virtual environment:

```bash
pip install .
```

For development purposes, you can install it in editable mode:

```bash
pip install -e .
```




## Dependencies

- `pymycobot` (for real robot control)

## Usage

### Connecting to the Robot

```python
from mypalletizer import Robot, RobotMode

# Simulation mode
with Robot(mode=RobotMode.VIRTUAL) as robot:
    robot.sync_move_joints(0, 45, -45, 0, 50)

# Real robot mode (requires COM port)
with Robot(mode=RobotMode.REAL, port="COM3") as robot:
    robot.set_color(255, 0, 0)
```

### Controlling the World (Simulation Only)

```python
from mypalletizer import World, Box

with World() as world:
    world.spawn(Box(name="my_box", position=(0.2, 0.0, 0.1)))
```

## Examples

Check the `examples/` directory for more usage examples.
