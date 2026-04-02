import pytest
from unittest.mock import MagicMock, patch
from mypalletizer.robot import Robot, RobotMode, EndEffector


@pytest.fixture
def mock_socket():
    with patch("socket.socket") as mock_sock:
        yield mock_sock


@pytest.fixture
def mock_mc():
    with patch("mypalletizer.controller.MyPalletizer260") as mock_mc_class:
        mock_instance = MagicMock()
        mock_mc_class.return_value = mock_instance
        yield mock_instance


def test_robot_init_virtual(mock_socket):
    with Robot(mode=RobotMode.VIRTUAL) as robot:
        assert robot.config.mode == RobotMode.VIRTUAL
        assert robot._impl.sock is not None
        assert robot._impl.mc is None


def test_robot_init_real(mock_mc):
    with Robot(mode=RobotMode.REAL, port="/dev/ttyUSB0") as robot:
        assert robot.config.mode == RobotMode.REAL
        assert robot._impl.sock is None
        assert robot._impl.mc is not None
        mock_mc.power_on.assert_called_once()


def test_robot_send_angles_virtual(mock_socket):
    with Robot(mode=RobotMode.VIRTUAL) as robot:
        robot.send_angles(10, 20, -30, 40, 50)
        # Verify UDP send was called
        robot._impl.sock.sendto.assert_called()


def test_robot_set_end_effector(mock_socket):
    with Robot(mode=RobotMode.VIRTUAL) as robot:
        robot.set_end_effector(EndEffector.PUMP)
        # Should build and send pump message
        robot._impl.sock.sendto.assert_called()


def test_robot_close(mock_socket):
    robot = Robot(mode=RobotMode.VIRTUAL)
    robot.close()
    assert robot._impl.sock is None
