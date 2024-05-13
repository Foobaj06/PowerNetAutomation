import netmiko
import getpass
import time
import datetime
import logging
import logging.handlers
import os

def setup_logger():
    logger = logging.getLogger('NetworkStatusLogger')
    logger.setLevel(logging.INFO)

    log_file = 'interface_status.log'
    handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3)  
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

def notify_admin(logger, message):
    print(message)
    logger.warning(message)  

def monitor_interfaces(conn, interface_ranges, logger):
    for interface_range in interface_ranges:
        output = conn.send_command(f'show interface port {interface_range} status', read_timeout=30)
        lines = output.splitlines()
        for line in lines[2:]:  
            parts = line.split()
            interface = parts[0]
            status = parts[-1]
            logger.info(f"Interface {interface} status: {status}")  
            if status.lower() == 'down':
                notify_admin(logger, f"Alert: {interface} is down")

def main():
    logger = setup_logger()
    device = {
        'device_type': 'generic',
        'host': '10.1.100.10',
        'username': 'admin',
        'password': getpass.getpass("Enter your device password: "),
    }

    interval = 60  
    interface_ranges = ["1/1-9", "1/10", "1/11-19", "1/20-24"]

    with netmiko.ConnectHandler(**device) as conn:
        while True:
            try:
                monitor_interfaces(conn, interface_ranges, logger)
                print(f"Status check completed at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            except netmiko.exceptions.ReadTimeout as e:
                logger.error(f"Read timeout occurred: {str(e)}")
            except Exception as e:
                logger.error(f"An error occurred: {str(e)}")
            time.sleep(interval)

if __name__ == "__main__":
    main()
