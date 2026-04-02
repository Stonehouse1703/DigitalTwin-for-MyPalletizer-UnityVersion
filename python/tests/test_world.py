import pytest
from unittest.mock import patch
from mypalletizer.world import World
from mypalletizer.objects import Box


@pytest.fixture
def mock_socket():
    with patch("socket.socket") as mock_sock:
        yield mock_sock


def test_world_spawn(mock_socket):
    with World() as world:
        box = Box(name="test_box", position=(0.1, 0.2, 0.3))
        world.spawn(box)
        world.sock.sendto.assert_called()


def test_world_clear(mock_socket):
    with World() as world:
        world.clear()
        world.sock.sendto.assert_called()


def test_world_load_preset(mock_socket):
    with World() as world:
        # Load a preset should call spawn (which calls sendto)
        world.load_preset("three_blocks")
        assert world.sock.sendto.call_count >= 1
