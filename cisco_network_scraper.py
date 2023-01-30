import paramiko
import csv

def gather_device_info(host, username, password, commands):
    results = {}
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=username, password=password)
    for command in commands:
        stdin, stdout, stderr = ssh.exec_command(command)
        result = stdout.read().decode()
        results[command] = result
    ssh.close()
    return results

def write_to_csv(data, filename):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data.items())

if __name__ == "__main__":
    host = "cisco_device_ip_or_hostname"
    username = "cisco_device_username"
    password = "cisco_device_password"
    commands = [
        "show interfaces brief",
        "show ip route",
        "show ip bgp neighbors",
        "show ip ospf neighbors",
    ]
    results = gather_device_info(host, username, password, commands)
    filename = "device_info.csv"
    write_to_csv(results, filename)
    print(f"Results written to {filename}")
