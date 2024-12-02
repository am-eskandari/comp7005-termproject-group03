from argparse import Namespace
from unittest.mock import patch

import pytest

from client import parse_arguments as parse_client_arguments
from proxy import parse_arguments as parse_proxy_arguments
from server import parse_arguments as parse_server_arguments


# Common helper function for argument validation
def _test_arguments(parser_function, args, expected_output):
    print(f"\nRunning test with arguments: {args}")
    try:
        mock_args = Namespace(**args)
        with patch("argparse.ArgumentParser.parse_args", return_value=mock_args):
            if expected_output:
                try:
                    parser_function()
                    print("✅ Test passed: Expected success, and the parser handled the arguments correctly.")
                except SystemExit as e:
                    pytest.fail(f"❌ Valid args caused a system exit: {e}")
            else:
                with pytest.raises(SystemExit):
                    parser_function()
                    print("✅ Test passed: Expected failure, and the parser raised SystemExit as expected.")
    except AttributeError as e:
        if not expected_output:
            print("✅ Test passed: Expected failure, and the parser raised AttributeError as expected.")
            return
        raise AssertionError(f"❌ Unexpected AttributeError: {e}")


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
    # Edge case for IP (wildcard address)
    (
            {
                "listen_ip": "0.0.0.0",  # Valid wildcard IP
                "listen_port": "8080",
            },
            True
    ),
    # Edge case for IP (broadcast address)
    (
            {
                "listen_ip": "255.255.255.255",  # Valid broadcast IP
                "listen_port": "8080",
            },
            True
    ),
    # Edge case for port (minimum valid port)
    (
            {
                "listen_ip": "127.0.0.1",
                "listen_port": "1024",  # Minimum valid port
            },
            True
    ),
    # Edge case for port (maximum valid port)
    (
            {
                "listen_ip": "127.0.0.1",
                "listen_port": "65535",  # Maximum valid port
            },
            True
    ),
    # Invalid port (below valid range)
    (
            {
                "listen_ip": "127.0.0.1",
                "listen_port": "80",  # Below valid range
            },
            False
    ),
    # Invalid port (above valid range)
    (
            {
                "listen_ip": "127.0.0.1",
                "listen_port": "70000",  # Above valid range
            },
            False
    ),
    # Invalid port (non-numeric)
    (
            {
                "listen_ip": "127.0.0.1",
                "listen_port": "abcd",  # Non-numeric value
            },
            False
    ),
    # Invalid IP format (too few octets)
    (
            {
                "listen_ip": "127.0.0",  # Invalid IP
                "listen_port": "8080",
            },
            False
    ),
    # Invalid IP format (too many octets)
    (
            {
                "listen_ip": "127.0.0.1.1",  # Invalid IP
                "listen_port": "8080",
            },
            False
    ),
    # Alphabetical value for IP
    (
            {
                "listen_ip": "wildcard",  # Invalid IP
                "listen_port": "8080",
            },
            False
    ),
    # Missing required argument (listen_ip)
    (
            {
                # Missing "listen_ip"
                "listen_port": "8080",
            },
            False
    ),
    # Missing required argument (listen_port)
    (
            {
                "listen_ip": "127.0.0.1",
                # Missing "listen_port"
            },
            False
    ),
    # Both arguments missing
    (
            {
                # Missing "listen_ip" and "listen_port"
            },
            False
    ),
])
def test_server_arguments(args, expected_output):
    _test_arguments(parse_server_arguments, args, expected_output)


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
                "listen_ip": "256.0.0.1",
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
    # Invalid delay range
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
                "client_delay_time": "500-100",  # Max < Min
                "server_delay_time": "200-600",
                "control_port": "7070",
            },
            False
    ),
    # Missing required argument
    (
            {
                "listen_ip": "127.0.0.1",
                "listen_port": "8080",
                # Missing "target_ip"
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
    # Alphabetical value for IP
    (
            {
                "listen_ip": "abc.def.ghi.jkl",
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
    # Invalid port below 1024
    (
            {
                "listen_ip": "127.0.0.1",
                "listen_port": "80",  # Below valid range
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
    # Invalid port above 65535
    (
            {
                "listen_ip": "127.0.0.1",
                "listen_port": "70000",  # Above valid range
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
    # Non-numeric port
    (
            {
                "listen_ip": "127.0.0.1",
                "listen_port": "abcd",  # Non-numeric
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
    # Invalid client_drop above 1.0
    (
            {
                "listen_ip": "127.0.0.1",
                "listen_port": "8080",
                "target_ip": "192.168.1.1",
                "target_port": "9090",
                "client_drop": "1.5",  # Invalid value
                "server_drop": "0.1",
                "client_delay": "0.3",
                "server_delay": "0.4",
                "client_delay_time": "100-500",
                "server_delay_time": "200-600",
                "control_port": "7070",
            },
            False
    ),
    # Negative client_drop
    (
            {
                "listen_ip": "127.0.0.1",
                "listen_port": "8080",
                "target_ip": "192.168.1.1",
                "target_port": "9090",
                "client_drop": "-0.1",  # Invalid value
                "server_drop": "0.1",
                "client_delay": "0.3",
                "server_delay": "0.4",
                "client_delay_time": "100-500",
                "server_delay_time": "200-600",
                "control_port": "7070",
            },
            False
    ),
    # Invalid client_delay_time with non-numeric values
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
                "client_delay_time": "abc-def",  # Invalid format
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
    # Edge case for port (valid lower boundary)
    (
            {
                "target_ip": "127.0.0.1",
                "target_port": "1024",  # Valid but edge of reserved range
                "timeout": "2000",
            },
            True
    ),
    # Edge case for port (valid upper boundary)
    (
            {
                "target_ip": "127.0.0.1",
                "target_port": "65535",  # Maximum valid port
                "timeout": "2000",
            },
            True
    ),
    # Invalid timeout (negative value)
    (
            {
                "target_ip": "127.0.0.1",
                "target_port": "8080",
                "timeout": "-1000",  # Negative value
            },
            False
    ),
    # Invalid timeout (non-numeric value)
    (
            {
                "target_ip": "127.0.0.1",
                "target_port": "8080",
                "timeout": "abc",  # Non-numeric
            },
            False
    ),
    # Missing required argument
    (
            {
                "target_ip": "127.0.0.1",
                # Missing "target_port"
                "timeout": "2000",
            },
            False
    ),
    # Missing `timeout`
    (
            {
                "target_ip": "127.0.0.1",
                "target_port": "8080",
            },
            False
    ),
    # Alphabetical value for `target_ip`
    (
            {
                "target_ip": "xyz.xyz.xyz.xyz",
                "target_port": "8080",
                "timeout": "2000",
            },
            False
    ),
    # Invalid `target_port` below valid range
    (
            {
                "target_ip": "127.0.0.1",
                "target_port": "80",  # Below valid range
                "timeout": "2000",
            },
            False
    ),
    # Invalid `target_port` above valid range
    (
            {
                "target_ip": "127.0.0.1",
                "target_port": "70000",  # Above valid range
                "timeout": "2000",
            },
            False
    ),
    # Non-numeric `target_port`
    (
            {
                "target_ip": "127.0.0.1",
                "target_port": "abcd",  # Non-numeric
                "timeout": "2000",
            },
            False
    ),
    # Non-standard but valid IP (wildcard)
    (
            {
                "target_ip": "0.0.0.0",  # Wildcard address
                "target_port": "8080",
                "timeout": "2000",
            },
            True
    ),
    # Large valid timeout
    (
            {
                "target_ip": "127.0.0.1",
                "target_port": "8080",
                "timeout": "1000000",  # Large but valid timeout
            },
            True
    ),
])
def test_client_arguments(args, expected_output):
    _test_arguments(parse_client_arguments, args, expected_output)
