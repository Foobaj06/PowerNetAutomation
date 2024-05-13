
import time
import logging
from datetime import datetime
from getpass import getpass
from netmiko import ConnectHandler
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(filename='backup_logs.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

password = getpass("Enter the password for all devices: ")

devices = [
    {'device_type': 'generic', 'host': '10.1.100.10', 'username': 'admin', 'password': password},
    {'device_type': 'generic', 'host': '10.1.100.20', 'username': 'admin', 'password': password},
    {'device_type': 'generic', 'host': '10.1.100.30', 'username': 'admin', 'password': password},
    {'device_type': 'generic', 'host': '10.1.100.40', 'username': 'admin', 'password': password},
]

def backup_config(device):
    try:
            with ConnectHandler(**device) as net_connect:
            net_connect.enable()
            net_connect.send_command("terminal length 0")  
            config = net_connect.send_command('show running-config', expect_string=r'#')
            net_connect.send_command("terminal length 24")  
            
        filename = f"{device['host']}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(filename, 'w') as file:
            file.write(config)
        
        logging.info(f"Backup for {device['host']} saved as {filename}")
        return f"Backup for {device['host']} saved as {filename}"
    except Exception as e:
        logging.error(f"Failed to backup {device['host']}: {e}")
        return f"Failed to backup {device['host']}: {e}"

def backup_all_configs():
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=len(devices)) as executor:
        results = list(executor.map(backup_config, devices))
    total_time = time.time() - start_time
    logging.info(f"Total time taken for backups: {total_time:.2f} seconds")
    return results, total_time

if __name__ == '__main__':
    results, total_time = backup_all_configs()
    print(results)
    print(f"Total time taken for backups: {total_time:.2f} seconds")
