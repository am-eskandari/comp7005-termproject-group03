import csv
import logging
from logging.handlers import RotatingFileHandler

# Set up logger for packet events
logger = logging.getLogger('packet_logger')
logger.setLevel(logging.INFO)
log_handler = RotatingFileHandler('packet_logs.log', maxBytes=5 * 1024 * 1024,
                                  backupCount=2)  # Rotate every 5MB, keep 2 backups
formatter = logging.Formatter('%(asctime)s, %(levelname)s, %(message)s')
log_handler.setFormatter(formatter)
logger.addHandler(log_handler)


def initialize_log(log_file_path, headers):
    """
    Initialize the CSV log file with headers.

    Args:
        log_file_path (str): Path to the log file.
        headers (list): List of headers for the CSV file.
    """
    with open(log_file_path, "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(headers)


def log_event(event, sequence, acknowledgment, src_ip, src_port, dest_ip, dest_port, message, latency):
    """
    Log an event using the rotating logger.

    Args:
        event (str): The type of event to log.
        sequence (int): The sequence number of the packet.
        acknowledgment (int or None): The acknowledgment number, if applicable.
        src_ip (str): Source IP address.
        src_port (int): Source port number.
        dest_ip (str): Destination IP address.
        dest_port (int): Destination port number.
        message (str or None): Message content, if applicable.
        latency (str or None): Latency in milliseconds, if applicable.
    """
    log_message = f"{event}, {sequence}, {acknowledgment}, {src_ip}, {src_port}, {dest_ip}, {dest_port}, {message}, {latency}"
    logger.info(log_message)
