# Inside installer.py
import os

def run_setup():
    print("\n[+] Netcracy -> Updating system package lists...")
    os.system("sudo apt-get update -y")
    packages = "hashcat nmap bettercap aircrack-ng wifipumpkin3 netcat-traditional wifite macchanger hcxtools mdk4"
    os.system(f"sudo apt-get install -y {packages}")
    print("\n[*] Setup complete!")
  
