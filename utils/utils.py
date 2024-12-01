import json

from utils.validation import validate_delay_time, validate_chance


def handle_control(control_socket, proxy_config):
    """
    Control interface for dynamic parameter updates.
    """
    print(f"🔧 Control interface active. Use the control port to dynamically update parameters.\n")
    while True:
        try:
            data, addr = control_socket.recvfrom(1024)
            command = data.decode().strip()
            print(f"📝 Received control command: {command}")

            if command.startswith("SET"):
                # Parse multiple parameter=value pairs
                updates = command[4:].strip()  # Remove "SET " prefix
                changes = updates.split()  # Split by spaces to get individual param=value pairs
                responses = []

                for change in changes:
                    if "=" not in change:
                        responses.append(f"❌ Invalid format: {change}")
                        continue

                    param, value = change.split("=", 1)
                    if param in ["client-delay-time", "server-delay-time"]:
                        try:
                            proxy_config[param] = validate_delay_time(value)  # Validate and parse delay time
                            responses.append(f"✅ Updated {param} to {value}")
                        except ValueError as e:
                            responses.append(f"❌ {e}")
                    elif param in proxy_config:
                        try:
                            proxy_config[param] = validate_chance(value)  # Validate chance values
                            responses.append(f"✅ Updated {param} to {value}")
                        except ValueError as e:
                            responses.append(f"❌ {e}")
                    else:
                        responses.append(f"❌ Invalid parameter: {param}")

                # Send responses back to client
                response = "\n".join(responses)
                print(f"🔨 {response}")
                control_socket.sendto(response.encode(), addr)

            elif command.startswith("GET"):
                # Return the current configuration
                response = json.dumps(proxy_config, indent=2)
                print(f"📤 Sent current configuration: {response}")
                control_socket.sendto(response.encode(), addr)

            else:
                response = "❌ Unknown command"
                print(f"⚠️ {response}")
                control_socket.sendto(response.encode(), addr)

        except Exception as e:
            print(f"❌ Error in control interface: {e}")
