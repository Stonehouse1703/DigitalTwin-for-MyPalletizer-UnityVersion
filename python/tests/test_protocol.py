from mypalletizer.protocol import (
    build_move_msg,
    sync_build_move_msg,
    build_led_msg,
    build_set_end_effector_msg,
    build_set_gripper_state_msg,
    build_pump_msg,
    build_spawn_msg,
    build_delete_msg,
    build_clear_msg,
)


def test_build_move_msg():
    msg = build_move_msg(10.0, 20.0, -30.0, 40.0, 50)
    assert msg == {
        "v": 1,
        "type": "move_joints",
        "j1": 10.0,
        "j2": 20.0,
        "j3": -30.0,
        "j4": 40.0,
        "speed": 50,
    }


def test_sync_build_move_msg():
    msg = sync_build_move_msg(0, 0, 0, 0, 100)
    assert msg["type"] == "sync_move_joints"
    assert msg["speed"] == 100


def test_build_led_msg():
    msg = build_led_msg(255, 128, 0)
    assert msg == {"v": 1, "type": "led", "r": 255, "g": 128, "b": 0}


def test_build_set_end_effector_msg():
    msg = build_set_end_effector_msg("gripper")
    assert msg == {"v": 1, "type": "set_end_effector", "tool": "gripper"}


def test_build_set_gripper_state_msg():
    msg = build_set_gripper_state_msg(1, 50, 1)
    assert msg == {"v": 1, "type": "set_gripper_state", "flag": 1, "speed": 50, "type_1": 1}


def test_build_pump_msg():
    assert build_pump_msg(True)["enabled"] is True
    assert build_pump_msg(False)["enabled"] is False


def test_build_spawn_msg():
    msg = build_spawn_msg(
        "box", "test_box", (1, 2, 3), (0, 0, 0), (0.1, 0.1, 0.1), (255, 0, 0)
    )
    assert msg["type"] == "spawn"
    assert msg["name"] == "test_box"
    assert msg["position"] == {"x": 1.0, "y": 2.0, "z": 3.0}
    assert msg["color"] == {"r": 255, "g": 0, "b": 0}


def test_build_delete_msg():
    msg = build_delete_msg("item1")
    assert msg == {"v": 1, "type": "delete", "name": "item1"}


def test_build_clear_msg():
    assert build_clear_msg() == {"v": 1, "type": "clear"}
