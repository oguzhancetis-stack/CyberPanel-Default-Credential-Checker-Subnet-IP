import argparse
import subprocess
import os
from colorama import Fore, Style
import ctypes
os.system("cls")
subnetsloc = input(Fore.YELLOW + "[+] Subnet txt location : " + Style.RESET_ALL)
def scan_subnet(subnet):
    # Your subnet scanning logic here
    print(f"Scanning subnet: {subnet}")



with open(subnetsloc, "r") as file:
    for line in file:
        subnet = line.strip()
        subprocess.Popen(["py", "Soz.py", "--subnet", subnet])
