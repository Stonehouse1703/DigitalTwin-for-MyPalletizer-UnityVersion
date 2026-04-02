def build_move_msg(j1: float, j2: float, j3: float, j4: float, speed: int) -> dict:
    return {
        "v": 1,
        "type": "move_joints",
        "j1": float(j1),
        "j2": float(j2),
        "j3": float(j3),
        "j4": float(j4),
        "speed": int(speed),
    }


def sync_build_move_msg(j1: float, j2: float, j3: float, j4: float, speed: int) -> dict:
    return {
        "v": 1,
        "type": "sync_move_joints",
        "j1": float(j1),
        "j2": float(j2),
        "j3": float(j3),
        "j4": float(j4),
        "speed": int(speed),
    }


def build_led_msg(r: int, g: int, b: int) -> dict:
    return {
        "v": 1,
        "type": "led",
        "r": int(r),
        "g": int(g),
        "b": int(b),
    }

def build_set_end_effector_msg(tool: str) -> dict:
    return {
        "v": 1,
        "type": "set_end_effector",
        "tool": str(tool),
    }


def build_set_gripper_state_msg(flag: int, speed: int, type_1: int = 1) -> dict:
    return {
        "v": 1,
        "type": "set_gripper_state",
        "flag": int(flag),
        "speed": int(speed),
        "type_1": int(type_1),
    }


def build_pump_msg(enabled: bool) -> dict:
    return {
        "v": 1,
        "type": "pump",
        "enabled": bool(enabled),
    }



# ---------------< Obejct spawn for the world >---------------


def build_spawn_msg(
    object_type: str,
    name: str,
    position: tuple[float, float, float],
    rotation: tuple[float, float, float],
    scale: tuple[float, float, float],
    color: tuple[int, int, int],
) -> dict:
    return {
        "v": 1,
        "type": "spawn",
        "object_type": object_type,
        "name": name,
        "position": {
            "x": float(position[0]),
            "y": float(position[1]),
            "z": float(position[2]),
        },
        "rotation": {
            "x": float(rotation[0]),
            "y": float(rotation[1]),
            "z": float(rotation[2]),
        },
        "scale": {
            "x": float(scale[0]),
            "y": float(scale[1]),
            "z": float(scale[2]),
        },
        "color": {
            "r": int(color[0]),
            "g": int(color[1]),
            "b": int(color[2]),
        },
    }


def build_delete_msg(name: str) -> dict:
    return {
        "v": 1,
        "type": "delete",
        "name": name,
    }


def build_clear_msg() -> dict:
    return {
        "v": 1,
        "type": "clear",
    }

