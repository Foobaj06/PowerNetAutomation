import netmiko
import getpass

def configure_vlan(conn, vlan_id, vlan_name):
    # Create a VLAN and assign a name
    commands = [f"vlan {vlan_id}", f"name {vlan_name}"]
    conn.send_config_set(commands)

def assign_ports_to_vlan(conn, vlan_id, ports):
    # Assign multiple ports to the specified VLAN
    commands = []
    for port in ports:
        commands.append(f"interface {port}")
        commands.append(f"switchport access vlan {vlan_id}")
    conn.send_config_set(commands)

def configure_trunk(conn, trunk_port, allowed_vlans):
    # Configure a trunk port and specify which VLANs are allowed
    commands = [
        f"interface {trunk_port}",
        "switchport mode trunk",
        f"switchport trunk allowed vlan {allowed_vlans}"
    ]
    conn.send_config_set(commands)

def main():
    # Specify device connection details
    device = {
        'device_type': 'generic',  # Adjust based on your network device type
        'host': '10.1.100.40',  # Replace with the IP address of your device
        'username': 'admin',  # Replace with your device username
        'password': getpass.getpass("Enter your device password: "),
    }

    # Prompt for VLAN ID and name
    vlan_id = input("Enter VLAN ID: ")
    vlan_name = input("Enter VLAN name: ")

    # Prompt for access ports (ports to assign to the VLAN)
    access_ports = input("Enter access ports (comma-separated): ").split(",")

    # Prompt for trunk port and allowed VLANs
    trunk_port = input("Enter trunk port: ")
    allowed_vlans = input("Enter allowed VLANs on trunk (comma-separated): ")

    # Connect to the network device and configure VLANs
    with netmiko.ConnectHandler(**device) as conn:
        configure_vlan(conn, vlan_id, vlan_name)
        assign_ports_to_vlan(conn, vlan_id, access_ports)
        configure_trunk(conn, trunk_port, allowed_vlans)
        print("VLAN configuration completed successfully.")

if __name__ == "__main__":
    main()
