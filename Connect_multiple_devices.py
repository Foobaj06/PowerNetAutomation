import getpass
from netmiko import ConnectHandler

def connect_to_device(device_details):
    device_details['password'] = getpass.getpass(f"Enter your SSH password for {device_details['host']}: ")
    return ConnectHandler(**device_details)

def main():
    devices = [
        {'device_type': 'generic', 'host': '10.1.100.10', 'username': 'admin', 'port': 22},
        {'device_type': 'generic', 'host': '10.1.100.20', 'username': 'admin', 'port': 22},
        {'device_type': 'generic', 'host': '10.1.100.30', 'username': 'admin', 'port': 22},
        {'device_type': 'generic', 'host': '10.1.100.40', 'username': 'admin', 'port': 22},
    ]

    commands = ['show ip interface brief', 'show vlan brief']
    for device in devices:
        net_connect = connect_to_device(device)
        print(f"Connected to {device['host']}...")
        for command in commands:
            output = net_connect.send_command(command)
            print(f"Output of '{command}' on {device['host']}:\n{output}\n")
        net_connect.disconnect()
        print(f"Disconnected from {device['host']}.\n")

if __name__ == "__main__":
    main()
