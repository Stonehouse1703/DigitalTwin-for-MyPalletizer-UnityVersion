# 🤖 MyPalletizer 650 M5 – Simulation Environment

## Overview

This project provides a **simple simulation environment in Unity** for the **MyPalletizer 650 M5** robot.

The same control logic can be used to:

* ▶ run the robot in simulation
* 🤖 run the real robot
* 🔁 or run both simultaneously

The robot is controlled using **Python**, just like on the real hardware.
This project provides a **lightweight library** that can be used directly for both simulation and real-world execution.

---

## Purpose

The goal is to:

* develop and test robot programs in simulation
* reuse the same Python code on the real robot
* simplify debugging and development

---

## Features

* Unity-based simulation
* Python control (same interface as real robot)
* UDP communication between Python and Unity
* Support for:

  * Gripper
  * Suction pump
* Simple pick & place interactions
* Dynamic object spawning

---

## Usage

Start the Unity simulation and control the robot via Python.

Example:

```python
robot.set_end_effector("gripper")
robot.set_gripper_state(1, 50)  # close
robot.set_gripper_state(0, 50)  # open
```

---

## Notes

* Uses a simplified interaction model (no full physics grasping)
* Designed for development, testing, and rapid iteration

---

## Documentation

Detailed setup and architecture will be added in the **Wiki**.


