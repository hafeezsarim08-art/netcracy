#!/usr/bin/env python3
# ============================================================================
#               NETCRACY: MULTI-ENGINE SYSTEMS CONFIGURATION CORE
# ============================================================================
import sys
import os
import time
import subprocess

def display_menu_help():
    print("====================================================")
    print("         NETCRACY: SYSTEMS MANAGEMENT INTERFACE     ")
    print("====================================================")
    print("Usage Rules:")
    print("  sudo netcracy start rogue ap <interface> [template] [ssid]")
    print("  sudo netcracy start wlan0mon <interface>")
    print("  sudo netcracy start traffic engine <interface>")
    print("  sudo netcracy start injection loop <interface> <bssid>")
    print("  sudo netcracy run network scan <target_ip/subnet>")
    print("  sudo netcracy start port listener <port>")
    print("  sudo netcracy run cpu crack <handshake.pcap>")
    print("  sudo netcracy run gpu crack <hash_file.hc22000>")
    print("  sudo netcracy run scan wireless <interface>")
    print("  sudo netcracy start spectrum monitor <interface>")
    print("  sudo netcracy start targeted scan <interface> <bssid> <channel>")
    print("====================================================")

def enforce_monitor_mode(interface):
    print(f"[*] Flipping {interface} into monitor mode configurations...")
    subprocess.run(["sudo", "systemctl", "stop", "NetworkManager"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["sudo", "pkill", "wpa_supplicant"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "link", "set", interface, "down"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["sudo", "iw", "dev", interface, "set", "type", "monitor"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "link", "set", interface, "up"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# ============================================================================
#               COMMAND ENGINE EXECUTION FUNCTIONS
# ============================================================================

def handle_rogue_ap(args):
    target_device = args[0] if len(args) >= 1 else "wlan0"
    chosen_template = args[1] if len(args) >= 2 else "starbucks"
    chosen_ssid = args[2] if len(args) >= 3 else "Starbucks_WiFi"
    
    print(f"\n[+] Netcracy -> Initializing Rogue AP Subsystems...")
    print(f"[*] Mapped Wireless Interface: {target_device}")
    print(f"[*] Target Configuration Context: {chosen_template} | {chosen_ssid}")
    time.sleep(1)
    
    # UPDATED: Simplified string layout using only the verified interface flag
    cmd = f"sudo wifipumpkin3 -i {target_device}"
    os.system(cmd)
    

def handle_wlan0mon(args):
    target_device = args[0] if len(args) >= 1 else "wlan0"
    print(f"\n[+] Netcracy -> Spawning Spectrum Interceptor on {target_device}...")
    enforce_monitor_mode(target_device)
    os.system(f"sudo airodump-ng {target_device}")

def handle_traffic_engine(args):
    target_device = args[0] if len(args) >= 1 else "wlan0"
    print(f"\n[+] Netcracy -> Spawning Live Traffic Dashboard on {target_device}...")
    enforce_monitor_mode(target_device)
    os.system(f"sudo bettercap -iface {target_device}")

def handle_injection_loop(args):
    target_device = args[0] if len(args) >= 1 else "wlan0"
    target_bssid = args[1] if len(args) >= 2 else ""
    print(f"\n[+] Netcracy -> Initializing target authentication verification on {target_device}...")
    if target_bssid:
        enforce_monitor_mode(target_device)
        os.system(f"sudo aireplay-ng --test -a {target_bssid} {target_device}")
    else:
        print("[-] Verification Error: Target BSSID parameter required for validation checks.")

def handle_network_scan(args):
    target_ip = args[0] if len(args) >= 1 else "192.168.1.0/24"
    print(f"\n[+] Netcracy -> Initiating subnet verification map across {target_ip}...")
    os.system(f"sudo nmap -v -sV -O {target_ip}")

def handle_port_listener(args):
    target_port = args[0] if len(args) >= 1 else "4444"
    print(f"\n[+] Netcracy -> Spawning persistent socket listener on Port {target_port}...")
    os.system(f"nc -lvnp {target_port}")

def handle_cpu_crack(args):
    target_file = args[0] if len(args) >= 1 else ""
    wordlist = "/usr/share/wordlists/rockyou.txt"
    if target_file:
        print(f"\n[+] Netcracy -> Initiating CPU-accelerated validation check on {target_file}...")
        os.system(f"sudo aircrack-ng '{target_file}' -w {wordlist}")
    else:
        print("[-] Error: Absolute target path to file required.")

def handle_gpu_crack(args):
    target_file = args[0] if len(args) >= 1 else ""
    wordlist = "/usr/share/wordlists/rockyou.txt"
    if target_file:
        print(f"\n[+] Netcracy -> Spawning high-throughput processing calculation loops on {target_file}...")
        os.system(f"hashcat -m 22000 -a 0 '{target_file}' {wordlist}")
    else:
        print("[-] Error: Absolute target hash file path required.")

def handle_wireless_survey(args):
    target_device = args[0] if len(args) >= 1 else "wlan0"
    print(f"\n[+] Netcracy -> Deploying interactive environment survey on {target_device}...")
    enforce_monitor_mode(target_device)
    os.system(f"sudo wifite --kill --i {target_device}")

def handle_spectrum_monitor(args):
    target_device = args[0] if len(args) >= 1 else "wlan0"
    print(f"\n[+] Netcracy -> Launching continuous targeted spectrum sweep on {target_device}...")
    enforce_monitor_mode(target_device)
    os.system(f"sudo airodump-ng {target_device}")

def handle_targeted_scan(args):
    target_device = args[0] if len(args) >= 1 else "wlan0"
    target_bssid = args[1] if len(args) >= 2 else ""
    target_channel = args[2] if len(args) >= 3 else ""
    
    print(f"\n[+] Netcracy -> Deploying Optimized Spectrum Interceptor on {target_device}...")
    enforce_monitor_mode(target_device)
    
    if target_bssid and target_channel:
        print(f"[*] Locking frequency capture onto BSSID [{target_bssid}] on Channel [{target_channel}]")
        os.system(f"sudo airodump-ng --bssid {target_bssid} --channel {target_channel} {target_device}")
    elif target_channel:
        print(f"[*] Locking frequency capture onto Channel [{target_channel}]")
        os.system(f"sudo airodump-ng --channel {target_channel} {target_device}")
    else:
        os.system(f"sudo airodump-ng {target_device}")

# ============================================================================
#               THE CENTRAL DISPATCH DICTIONARY
# ============================================================================

COMMAND_MAP = {
    ("start", "rogue", "ap"): handle_rogue_ap,
    ("start", "wlan0mon", ""): handle_wlan0mon,  # Fallback helper for short syntax
    ("start", "wlan0mon"): handle_wlan0mon,
    ("start", "traffic", "engine"): handle_traffic_engine,
    ("start", "injection", "loop"): handle_injection_loop,
    ("run", "network", "scan"): handle_network_scan,
    ("start", "port", "listener"): handle_port_listener,
    ("run", "cpu", "crack"): handle_cpu_crack,
    ("run", "gpu", "crack"): handle_gpu_crack,
    ("run", "scan", "wireless"): handle_wireless_survey,
    ("start", "spectrum", "monitor"): handle_spectrum_monitor,
    ("start", "targeted", "scan"): handle_targeted_scan,
}

def main():
    if len(sys.argv) < 2:
        display_menu_help()
        sys.exit(1)

    # Sanitize command arguments into a consistent lowercase list
    tokens = [str(arg).lower() for arg in sys.argv[1:]]

    # Dynamically match token chains against our structural lookup dictionary keys
    matched = False
    for command_tuple, function_handler in COMMAND_MAP.items():
        cmd_len = len(command_tuple)
        if len(tokens) >= cmd_len and tuple(tokens[:cmd_len]) == command_tuple:
            # Isolate the remaining arguments to pass directly to the target utility
            remaining_args = tokens[cmd_len:]
            try:
                function_handler(remaining_args)
            except KeyboardInterrupt:
                print("\n\n[*] Intercepted break code execution. Restoring network environment daemons...")
                subprocess.run(["sudo", "systemctl", "start", "NetworkManager"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            matched = True
            break

    if not matched:
        print("[-] Error: Unrecognized string parameter sequence combination.")
        display_menu_help()

if __name__ == "__main__":
    if os.getuid() != 0:
        print("[-] Critical Privilege Error: This interface wrapper requires administrative privileges (sudo).")
        sys.exit(1)
    main()
