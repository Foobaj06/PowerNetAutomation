import getpass
from netmiko import ConnectHandler

def connect_to_device(device_details):
    device_details['password'] = getpass.getpass(f"Enter your SSH password for {device_details['host']}: ")
    return ConnectHandler(**device_details)

def main():
    device = {
        'device_type': 'cisco_ios',
        'host': '192.168.1.1',
        'username': 'admin',
        'port': 22,
    }

    net_connect = connect_to_device(device)
    commands = ['show ip interface brief', 'show vlan brief', 'show interface status']
    for command in commands:
        output = net_connect.send_command(command)
        print(f"Output of '{command}':\n{output}\n")
    net_connect.disconnect()

if __name__ == "__main__":
    main()
