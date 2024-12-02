from argparse import Namespace
from unittest.mock import patch

import pytest

from client import parse_arguments as parse_client_arguments
from proxy import parse_arguments as parse_proxy_arguments
from server import parse_arguments as parse_server_arguments


# Common helper function for argument validation
def _test_arguments(parser_function, args, expected_output):
    mock_args = Namespace(**args)
    with patch("argparse.ArgumentParser.parse_args", return_value=mock_args):
        if expected_output:
            try:
                parser_function()
            except SystemExit as e:
                pytest.fail(f"Valid args caused a system exit: {e}")
        else:
            with pytest.raises(SystemExit):
                parser_function()


# Proxy Tests
@pytest.mark.parametrize("args, expected_output", [
    # Valid case
    (
            {
                "listen_ip": "127.0.0.1",
                "listen_port": "8080",
                "target_ip": "192.168.1.1",
                "target_port": "9090",
                "client_drop": "0.2",
                "server_drop": "0.1",
                "client_delay": "0.3",
                "server_delay": "0.4",
                "client_delay_time": "100-500",
                "server_delay_time": "200-600",
                "control_port": "7070",
            },
            True
    ),
    # Invalid IP
    (
            {
                "listen_ip": "256.0.0.1",  # Invalid IP
                "listen_port": "8080",
                "target_ip": "192.168.1.1",
                "target_port": "9090",
                "client_drop": "0.2",
                "server_drop": "0.1",
                "client_delay": "0.3",
                "server_delay": "0.4",
                "client_delay_time": "100-500",
                "server_delay_time": "200-600",
                "control_port": "7070",
            },
            False
    ),
])
def test_proxy_arguments(args, expected_output):
    _test_arguments(parse_proxy_arguments, args, expected_output)


# Client Tests
@pytest.mark.parametrize("args, expected_output", [
    # Valid case
    (
            {
                "target_ip": "127.0.0.1",
                "target_port": "8080",
                "timeout": "2000",
            },
            True
    ),
    # Non-numeric IP
    (
            {
                "target_ip": "not-an-ip",  # Non-numeric IP
                "target_port": "8080",
                "timeout": "2000",
            },
            False
    ),
])
def test_client_arguments(args, expected_output):
    _test_arguments(parse_client_arguments, args, expected_output)


# Server Tests
@pytest.mark.parametrize("args, expected_output", [
    # Valid case
    (
            {
                "listen_ip": "127.0.0.1",
                "listen_port": "8080",
            },
            True
    ),
    # Invalid port
    (
            {
                "listen_ip": "127.0.0.1",
                "listen_port": "70000",  # Port > 65535
            },
            False
    ),
])
def test_server_arguments(args, expected_output):
    _test_arguments(parse_server_arguments, args, expected_output)
