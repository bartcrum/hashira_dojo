import ldap3
import requests
import os

def get_a_records(domain):
    server = ldap3.Server("ldap://dc.example.com")
    conn = ldap3.Connection(server, auto_bind=True)
    base_dn = "DC=example,DC=com"
    search_filter = "(&(objectCategory=dnsNode)(aRecord=*))"
    attributes = ["dNSHostName", "aRecord"]
    result = conn.extend.standard.paged_search(
        search_base=base_dn,
        search_filter=search_filter,
        search_scope=ldap3.SUBTREE,
        attributes=attributes,
        paged_size=5,
        generator=False
    )
    a_records = []
    for entry in result:
        dns_host_name = entry["attributes"]["dNSHostName"]
        a_record = entry["attributes"]["aRecord"]
        a_records.append({"dns_host_name": dns_host_name, "a_record": a_record})
    return a_records

def import_a_records(api_key, a_records):
    headers = {"Authorization": f"Bearer {api_key}"}
    imported_records_file = "imported_records.txt"
    imported_records = set()
    if os.path.exists(imported_records_file):
        with open(imported_records_file, "r") as f:
            for line in f:
                imported_records.add(line.strip())
    with open(imported_records_file, "a") as f:
        for a_record in a_records:
            host_name = a_record["dns_host_name"]
            ip_address = a_record["a_record"]
            record = f"{host_name}:{ip_address}"
            if record in imported_records:
                continue
            url = f"https://api.fortinet.com/dns/v1/records/{domain}/{host_name}"
            data = {"type": "A", "value": ip_address}
            response = requests.put(url, headers=headers, json=data)
            if response.status_code == 200:
                f.write(record + "\n")
                imported_records.add(record)
            else:
                print(f"Failed to import {record}: {response.text}")

domain = "example.com"
api_key = "your_api_key"
a_records = get_a_records(domain)
import_a_records(api_key, a_records)
