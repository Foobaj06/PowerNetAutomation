import netmiko
import getpass
import datetime
import logging
import os
import time

# Enable logging for debugging purposes
logging.basicConfig(filename="netmiko_debug.log", level=logging.DEBUG)
logger = logging.getLogger("netmiko")

def ssh_backup_and_restore(device, action):
    start_time = time.time()
    filename = f"{device['host']}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    with netmiko.ConnectHandler(**device) as conn:
        if action == 'backup':
            backup_configuration(conn, filename)
        elif action == 'restore':
            restore_configuration(conn, filename)
        else:
            print("Invalid action. Please enter 'backup' or 'restore'.")

    elapsed_time = time.time() - start_time
    print(f"{action.capitalize()} completed for {device['host']}. Time taken: {elapsed_time:.2f} seconds")

def backup_configuration(conn, filename):
    conn.enable()
    conn.send_command("terminal length 0")
    config = conn.send_command("show running-config", expect_string=r"#")
    conn.send_command("terminal length 24")
    with open(filename, 'w') as file:
        file.write(config)
    print(f"Configuration backed up to {filename}")

def restore_configuration(conn, filename):
    if not os.path.isfile(filename):
        print(f"Error: File '{filename}' not found.")
        return

    with open(filename, 'r') as file:
        config_lines = file.read().strip().splitlines()

    for line in config_lines:
        if line.strip() == "" or line.strip().startswith("!"):
            continue
        conn.send_command(line, expect_string=r"#", delay_factor=2)

    try:
        conn.exit_config_mode()
    except ValueError:
        print("Manual attempt to exit configuration mode")
        conn.send_command('end', expect_string=r"#")
    print(f"Configuration restored from {filename}")

def main():
    devices = [
        {'device_type': 'generic', 'host': '10.1.100.10', 'username': 'admin', 'password': getpass.getpass("Enter password for 10.1.100.10: ")},
        {'device_type': 'generic', 'host': '10.1.100.20', 'username': 'admin', 'password': getpass.getpass("Enter password for 10.1.100.20: ")},
        {'device_type': 'generic', 'host': '10.1.100.30', 'username': 'admin', 'password': getpass.getpass("Enter password for 10.1.100.30: ")},
        {'device_type': 'generic', 'host': '10.1.100.40', 'username': 'admin', 'password': getpass.getpass("Enter password for 10.1.100.40: ")}
    ]
    
    action = input("Enter 'backup' or 'restore': ").strip().lower()
    for device in devices:
        ssh_backup_and_restore(device, action)

if __name__ == "__main__":
    main()
