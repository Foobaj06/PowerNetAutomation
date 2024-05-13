import netmiko
from xml.etree.ElementTree import Element, SubElement, ElementTree, parse
import time
import getpass
import datetime
import os


def create_xml_root():
    return Element('DeviceStatus')


def add_interface_status_to_xml(root, interface, status):
    timestamp = SubElement(root, 'Timestamp')
    timestamp.text = datetime.datetime.now().isoformat()
    interface_element = SubElement(root, 'Interface')
    name_element = SubElement(interface_element, 'Name')
    name_element.text = interface
    status_element = SubElement(interface_element, 'Status')
    status_element.text = status


def remove_old_entries(root, days=7):
    current_time = datetime.datetime.now()
    entries = root.findall('./Interface')
    for entry in entries:
        timestamp_text = entry.find('Timestamp').text
        entry_time = datetime.datetime.fromisoformat(timestamp_text)
        if (current_time - entry_time).days > days:
            root.remove(entry)


def write_xml_to_file(root, filename):
    tree = ElementTree(root)
    tree.write(filename, encoding='utf-8', xml_declaration=True)


def notify_admin(message):
    print(message)


def load_or_create_xml(filename):
    if os.path.exists(filename):
        tree = parse(filename)
        root = tree.getroot()
        remove_old_entries(root)
    else:
        root = create_xml_root()
    return root


def main():
    device = {
        'device_type': 'generic',
        'host': '10.1.100.10',
        'username': 'admin',
        'password': getpass.getpass("Enter your device password: "),
    }

    filename = 'interface_status.xml'
    interval = 300

    with netmiko.ConnectHandler(**device) as conn:
        while True:
            try:
                output = conn.send_command(
                    'show interface port 1/11-19 status', read_timeout=30)
                root = load_or_create_xml(filename)
                lines = output.splitlines()
                for line in lines[2:]:
                    parts = line.split()
                    interface = parts[0]
                    status = parts[-1]
                    add_interface_status_to_xml(root, interface, status)
                    if status.lower() == 'down':
                        notify_admin(f"Alert: {interface} is down")

                write_xml_to_file(root, filename)
                print(
                    f"Status recorded at {time.strftime('%X')} and saved to 'interface_status.xml'.")
            except netmiko.exceptions.ReadTimeout as e:
                print(f"Read timeout occurred: {str(e)}")
            except Exception as e:
                print(f"An error occurred: {str(e)}")
            time.sleep(interval)


if __name__ == "__main__":
    main()
