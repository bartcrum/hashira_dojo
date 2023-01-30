import paramiko
import csv

# Define a function to establish SSH connection and retrieve ACL's
def get_acls(ip, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username=username, password=password)
    stdin, stdout, stderr = ssh.exec_command("show access-lists")
    acls = stdout.read().decode()
    ssh.close()
    return acls

# Open a CSV file to write the ACL's
with open('acls.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Router IP', 'ACLs'])

# Read the router list from a CSV file
with open('router_list.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader) # skip the header row
    routers = [row[0] for row in reader]

# Loop through the list of routers
for router in routers:
    acls = get_acls(router, 'admin', 'password')
    with open('acls.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([router, acls])

print("ACL's exported to acls.csv")
