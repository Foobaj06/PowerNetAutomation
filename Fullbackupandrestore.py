
import time
import logging
from datetime import datetime
from getpass import getpass
from netmiko import ConnectHandler
from concurrent.futures import ThreadPoolExecutor
import os

# Setup basic logging
logging.basicConfig(filename='network_operations.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def backup_configuration(conn):
    conn.enable()
    conn.send_command("terminal length 0")  # Disable pagination
    config = conn.send_command('show running-config', expect_string=r'#')
    conn.send_command("terminal length 24")  # Re-enable pagination (optional)
    return config

def restore_configuration(conn, filename):
    if not os.path.isfile(filename):
        print(f"Error: File '{filename}' not found.")
        return

    with open(filename, 'r') as file:
        config_lines = file.read().strip().splitlines()

    conn.enable()
    conn.send_command("configure terminal", expect_string=r'#')
    for line in config_lines:
        if line.strip() and not line.strip().startswith('!'):
            conn.send_command_timing(line.strip(), expect_string=r'#')
    conn.send_command("end", expect_string=r'#')
    print(f"Configuration restored from {filename}.")

def perform_backup_or_restore(action, device, filename=None):
    with ConnectHandler(**device) as conn:
        if action == 'backup':
            config = backup_configuration(conn)
            with open(filename, 'w') as file:
                file.write(config)
            print(f"Configuration backed up to {filename}")
        elif action == 'restore':
            restore_configuration(conn, filename)

def main():
    device = {
        'device_type': 'cisco_ios',
        'host': '10.1.100.30',  # Example IP
        'username': 'admin',
        'password': getpass("Enter the password for all devices: "),
    }

    action = input("Enter 'backup' or 'restore': ").lower()
    filename = ''
    if action == 'backup':
        filename = f"config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        perform_backup_or_restore(action, device, filename)
    elif action == 'restore':
        filename = input("Enter filename to restore: ")
        perform_backup_or_restore(action, device, filename)
    else:
        print("Invalid action. Please enter 'backup' or 'restore'.")

if __name__ == '__main__':
    main()
