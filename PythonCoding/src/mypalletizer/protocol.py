def build_move_angle_msg(id: int, degree: float, speed: int) -> dict:
    return {
        "v": 1,
        "type": "move_joint",
        "id": float(id),
        "degree": float(degree),
        "speed": float(speed),
    }

def build_move_msg(j1: float, j2: float, j3: float, j4: float, speed: int) -> dict:
    return {
        "v": 1,
        "type": "move_joints",
        "j1": float(j1),
        "j2": float(j2),
        "j3": float(j3),
        "j4": float(j4),
        "speed": float(speed),
    }

def sync_build_move_msg(j1: float, j2: float, j3: float, j4: float, speed: int) -> dict:
    return {
        "v": 1,
        "type": "sync_move_joints",
        "j1": float(j1),
        "j2": float(j2),
        "j3": float(j3),
        "j4": float(j4),
        "speed": float(speed),
    }

def build_led_msg(r: int, g: int, b: int) -> dict:
    return {
        "v": 1,
        "type": "led",
        "r": int(r),
        "g": int(g),
        "b": int(b),
    }

def build_move_coord_msg(coord_id: int, coord: float, speed: int) -> dict:
    # coord_id: 1..4 => x,y,z,rx
    return {
        "v": 1,
        "type": "move_coord",
        "coord_id": int(coord_id),
        "coord": float(coord),
        "speed": float(speed),
    }


def build_move_coords_msg(x: float, y: float, z: float, rx: float, speed: int) -> dict:
    return {
        "v": 1,
        "type": "move_coords",
        "x": float(x),
        "y": float(y),
        "z": float(z),
        "rx": float(rx),
        "speed": float(speed),
    }