import logging
from getpass import getpass
from netmiko import ConnectHandler

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

def shutdown_ports(conn):
    conn.enable()
    conn.send_command("configure terminal", expect_string=r'#')
    port_range = input("Enter the port range to shutdown (e.g., fa0/1-24): ")
    commands = [
        f"interface range {port_range}",
        "shutdown"
    ]
    for cmd in commands:
        conn.send_command(cmd, expect_string=r'#')
    print(f"Ports {port_range} have been shut down.")
    conn.send_command("end", expect_string=r'#')

def perform_shutdown(device):
    filtered_device = {key: device[key] for key in ['device_type', 'host', 'username', 'password']}

    with ConnectHandler(**filtered_device) as conn:
        shutdown_ports(conn)

def main():
    list_devices()
    device_choice = int(input("Select the device number: ")) - 1
    device = devices[device_choice]
    device['password'] = getpass(f"Enter password for {device['host']}: ")

    perform_shutdown(device)

if __name__ == '__main__':
    main()
