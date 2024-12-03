import json
import threading

from utils.logger import control_logger, log_control_event
from utils.validation import validate_delay_time, validate_chance

# Initialize a threading lock
control_lock = threading.Lock()


def handle_control(control_socket, proxy_config):
    """
    Control interface for dynamic parameter updates.
    Logs all updates using the control_logger.
    """
    print(f"🔧 Control interface active. Use the control port to dynamically update parameters.\n")
    while True:
        try:
            data, addr = control_socket.recvfrom(1024)
            command = data.decode().strip()
            control_logger.info(f"Received control command from {addr}: {command}")
            print(f"📝 Received control command: {command}")

            if command.startswith("SET"):
                updates = command[4:].strip()  # Remove "SET " prefix
                changes = updates.split()  # Split by spaces to get individual param=value pairs
                responses = []

                print(f"🔒 Acquiring lock for configuration update...")
                with control_lock:  # Lock during updates
                    print(f"🔑 Lock acquired.")
                    for change in changes:
                        if "=" not in change:
                            msg = f"❌ Invalid format: {change}"
                            responses.append(msg)
                            control_logger.error(msg)
                            continue

                        param, value = change.split("=", 1)
                        if param in ["client-delay-time", "server-delay-time"]:
                            try:
                                old_value = proxy_config[param]
                                new_value = validate_delay_time(value)  # Validate and parse delay time
                                proxy_config[param] = new_value
                                responses.append(f"✅ Updated {param} from {old_value} to {new_value}")
                                log_control_event(control_logger, param, old_value, new_value)
                            except ValueError as e:
                                msg = f"❌ {e}"
                                responses.append(msg)
                                control_logger.error(msg)
                        elif param in proxy_config:
                            try:
                                old_value = proxy_config[param]
                                new_value = validate_chance(value)  # Validate chance values
                                proxy_config[param] = new_value
                                responses.append(f"✅ Updated {param} from {old_value} to {new_value}")
                                log_control_event(control_logger, param, old_value, new_value)
                            except ValueError as e:
                                msg = f"❌ {e}"
                                responses.append(msg)
                                control_logger.error(msg)
                        else:
                            msg = f"❌ Invalid parameter: {param}"
                            responses.append(msg)
                            control_logger.error(msg)

                    print(f"🔓 Lock released after configuration update.")

                response = "\n".join(responses)
                print(f"🔨 {response}")
                control_logger.info(f"Changes applied: {response}")
                control_socket.sendto(response.encode(), addr)

            elif command.startswith("GET"):
                response = json.dumps(proxy_config, indent=2)
                print(f"📤 Sent current configuration: {response}")
                control_logger.info(f"Sent current configuration to {addr}")
                control_socket.sendto(response.encode(), addr)

            else:
                response = "❌ Unknown command"
                print(f"⚠️ {response}")
                control_logger.error(f"Unknown command from {addr}: {command}")
                control_socket.sendto(response.encode(), addr)

        except Exception as e:
            error_msg = f"❌ Error in control interface: {e}"
            print(error_msg)
            control_logger.error(error_msg)
