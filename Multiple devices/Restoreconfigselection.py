import time
import logging
from datetime import datetime
from getpass import getpass
from netmiko import ConnectHandler
import os

# Setup basic logging
logging.basicConfig(filename='network_operations.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

devices = [
    {'device_type': 'generic', 'host': '10.1.100.10', 'username': 'admin', 'password': '', 'description': 'Switch 1'},
    {'device_type': 'generic', 'host': '10.1.100.20', 'username': 'admin', 'password': '', 'description': 'Switch 2'},
    {'device_type': 'generic', 'host': '10.1.100.30', 'username': 'admin', 'password': '', 'description': 'Switch 3'},
    {'device_type': 'generic', 'host': '10.1.100.40', 'username': 'admin', 'password': '', 'description': 'Switch 4'},
]

def list_devices():
    for idx, device in enumerate(devices):
        print(f"{idx+1}. {device['description']} - {device['host']}")

def get_device_passwords():
    for device in devices:
        device['password'] = getpass(f"Enter password for {device['host']}: ")

def restore_configuration(conn, filename):
    if not os.path.isfile(filename):
        print(f"Error: File '{filename}' not found.")
        return

    conn.enable()
    conn.send_command("configure terminal", expect_string=r'#')

    with open(filename, 'r') as file:
        config_lines = file.read().strip().splitlines()

    errors_occurred = False
    for line in config_lines:
        if line.strip() == "" or line.strip().startswith("!"):
            continue 

        try:
            conn.send_command(line.strip(), expect_string=r'#', delay_factor=2)
        except Exception as e:
            print(f"Error sending command '{line.strip()}': {str(e)}")
            errors_occurred = True

    try:
        conn.exit_config_mode()
    except ValueError:
        print("Manual attempt to exit configuration mode")
        conn.send_command('end', expect_string=r'#')

    if not errors_occurred:
        print(f"Configuration restored from {filename}")
    else:
        print(f"Configuration restored with errors from {filename}")

def perform_restore(device, filename):
    filtered_device = {key: device[key] for key in ['device_type', 'host', 'username', 'password']}

    with ConnectHandler(**filtered_device) as conn:
        restore_configuration(conn, filename)

def main():
    list_devices()
    device_choice = int(input("Select the device number: ")) - 1
    device = devices[device_choice]
    device['password'] = getpass(f"Enter password for {device['host']}: ")

    filename = input("Enter filename to restore: ")
    perform_restore(device, filename)

if __name__ == '__main__':
    main()
