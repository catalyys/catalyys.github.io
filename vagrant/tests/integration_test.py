import pytest
import paramiko
import subprocess
import re

# ---------------------
# SSH Helpers
# ---------------------

def get_ssh_config(vm_name):
    ssh_config_raw = subprocess.check_output(["vagrant", "ssh-config", vm_name]).decode()
    config = {}
    for line in ssh_config_raw.splitlines():
        match = re.match(r'\s*(\S+)\s+(.*)', line)
        if match:
            config[match[1]] = match[2]
    return {
        "hostname": config["HostName"],
        "port": int(config["Port"]),
        "username": config["User"],
        "key_filename": config["IdentityFile"].strip('"')
    }

def ssh_command(vm_name, command):
    config = get_ssh_config(vm_name)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
        hostname=config["hostname"],
        port=config["port"],
        username=config["username"],
        key_filename=config["key_filename"]
    )
    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode()
    ssh.close()
    return output.strip()

def extract_ip(ip_output):
    match = re.search(r'inet\s(10\.100\.\d+\.\d+)/', ip_output)
    return match.group(1) if match else None

def extract_ipv6(ip_output):
    match = re.search(r'inet6\s(fd11:2:3:4(:+[a-z0-9]+)+)/', ip_output)
    return match.group(1) if match else None

def packet_loss_from_ping(output):
    match = re.search(r'(\d+)% packet loss', output)
    return int(match.group(1)) if match else 100

# ---------------------
# Fixtures
# ---------------------

@pytest.fixture(scope="module")
def client_prod_ip():
    output = ssh_command("client_prod", "ip a")
    return extract_ip(output)

@pytest.fixture(scope="module")
def client_test_ip():
    output = ssh_command("client_test", "ip a")
    return extract_ip(output)

@pytest.fixture(scope="module")
def client_entw_ip():
    output = ssh_command("client_entw", "ip a")
    return extract_ipv6(output)

# ---------------------
# Tests
# ---------------------

# ---------------- IPs ----------------

def test_client_prod_has_ip(client_prod_ip):
    assert client_prod_ip.startswith("10.100.")

def test_client_test_has_ip(client_test_ip):
    assert client_test_ip.startswith("10.100.")

def test_client_entw_has_ip(client_entw_ip):
    assert client_entw_ip.startswith("fd11:2:3:4")

# ---------------- Gateways ----------------

def test_ping_to_gateway_prod():
    output = ssh_command("client_prod", f"ping -c 3 10.100.1.254")
    loss = packet_loss_from_ping(output)
    assert loss < 100, f"Ping failed: {loss}% packet loss\n{output}"

def test_ping_to_gateway_test():
    output = ssh_command("client_test", f"ping -c 3 10.100.2.254")
    loss = packet_loss_from_ping(output)
    assert loss < 100, f"Ping failed: {loss}% packet loss\n{output}"

def test_ping_to_gateway_entw():
    output = ssh_command("client_entw", f"ping6 -c 3 fd11:2:3:4::10")
    loss = packet_loss_from_ping(output)
    assert loss < 100, f"Ping failed: {loss}% packet loss\n{output}"

# ---------------- Firewall ----------------

def test_ping_between_debians(client_prod_ip):
    output = ssh_command("client_test", f"ping -c 3 {client_prod_ip}")
    loss = packet_loss_from_ping(output)
    assert loss < 100, f"Ping failed: {loss}% packet loss\n{output}"

# ---------------- Nginx ----------------

def test_nginx_from_client_test(client_prod_ip):
    output = ssh_command("client_test", f"curl http://{client_prod_ip}:8080")
    assert "azubi" in output.lower()

# ---------------- NAT ----------------

def test_nat_external_ping_client_prod():
    output = ssh_command("client_prod", "ping -c 3 1.1.1.1")
    loss = packet_loss_from_ping(output)
    assert loss < 100, f"Ping failed: {loss}% packet loss\n{output}"

def test_nat_external_ping_client_test():
    output = ssh_command("client_test", "ping -c 3 1.1.1.1")
    loss = packet_loss_from_ping(output)
    assert loss < 100, f"Ping failed: {loss}% packet loss\n{output}"

def test_nat_external_ping_client_entw():
    output = ssh_command("client_entw", "ping -6 -c 3 64:ff9b::8.8.8.8")
    loss = packet_loss_from_ping(output)
    assert loss < 100, f"Ping failed: {loss}% packet loss\n{output}"

# ---------------- NAT64 ----------------

def test_nat64_ping_client_entw(client_prod_ip):
    output = ssh_command("client_entw", f"ping -6 -c 3 64:ff9b::{client_prod_ip}")
    loss = packet_loss_from_ping(output)
    assert loss < 100, f"Ping failed: {loss}% packet loss\n{output}"

# ---------------- DNS ----------------

def test_dns_resolution_client_prod():
    output = ssh_command("client_prod", "dig +short server1.azubi.dataport.de @localhost")
    assert "10.100.1.10" in output

def test_dns_resolution_client_test():
    output = ssh_command("client_test", "dig +short server2.test.azubi.dataport.de @localhost")
    assert "10.100.2.10" in output

def test_dns_resolution_client_test_prod(client_prod_ip):
    output = ssh_command("client_test", f"dig +short server1.azubi.dataport.de @{client_prod_ip}")
    assert "10.100.1.10" in output

def test_dns_forwarding_test_prod():
    output = ssh_command("client_test", "dig +short server1.azubi.dataport.de @localhost")
    assert "10.100.1.10" in output

def test_dns_forwarding_prod_test():
    output = ssh_command("client_prod", "dig +short debian.test.azubi.dataport.de @localhost")
    assert "10.100.2.9" in output

# ---------------- DNS64 ----------------

def test_dns64_entw_test():
    output = ssh_command("client_entw", "dig +short debian.test.azubi.dataport.de aaaa")
    assert "64:ff9b::a64:209" in output

# ---------------- NFS ----------------

def test_nfs_prod():
    output = ssh_command("client_test", "sudo ls /opt/nfs/backup/bind")
    assert "prod_named.conf" in output

def test_nfs_test():
    output = ssh_command("client_test", "sudo ls /opt/nfs/backup/bind")
    assert "test_named.conf" in output

