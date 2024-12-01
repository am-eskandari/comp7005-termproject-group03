import logging
from logging.handlers import RotatingFileHandler


def create_logger(logger_name, log_file_name):
    """
    Create a logger for a specific component (client, server, proxy).

    Args:
        logger_name (str): Name of the logger.
        log_file_name (str): Path to the log file.

    Returns:
        logging.Logger: Configured logger.
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    # Create handler for rotating logs
    log_handler = RotatingFileHandler(log_file_name, maxBytes=5 * 1024 * 1024, backupCount=2)
    formatter = logging.Formatter('%(asctime)s, %(levelname)s, %(message)s')
    log_handler.setFormatter(formatter)

    # Avoid adding multiple handlers if the logger is used more than once
    if not logger.hasHandlers():
        logger.addHandler(log_handler)

    return logger


def log_event(logger, event, sequence, acknowledgment, src_ip, src_port, dest_ip, dest_port, message, latency):
    """
    Log an event using the rotating logger.

    Args:
        logger (logging.Logger): Logger instance (client, server, proxy).
        event (str): The type of event to log.
        sequence (int or None): The sequence number of the packet, or None if not applicable.
        acknowledgment (int or None): The acknowledgment number, if applicable.
        src_ip (str): Source IP address.
        src_port (int): Source port number.
        dest_ip (str): Destination IP address.
        dest_port (int): Destination port number.
        message (str or None): Message content, if applicable.
        latency (float or None): Latency in milliseconds, if applicable.
    """
    sequence_str = str(sequence) if sequence is not None else "N/A"
    acknowledgment_str = str(acknowledgment) if acknowledgment is not None else "N/A"
    log_message = f"{event}, {sequence_str}, {acknowledgment_str}, {src_ip}, {src_port}, {dest_ip}, {dest_port}, {message}, {latency}"
    logger.info(log_message)


# Loggers for each module
client_logger = create_logger('client_logger', 'client_packet_logs.log')
server_logger = create_logger('server_logger', 'server_packet_logs.log')
proxy_logger = create_logger('proxy_logger', 'proxy_packet_logs.log')
