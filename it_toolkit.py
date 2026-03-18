#!/usr/bin/env python3
"""
IT Support Toolkit v1.0
========================
A lightweight CLI tool for IT Support Engineers to automate
common diagnostic and troubleshooting tasks.

Author: [Your Name]
License: MIT
"""

import subprocess
import socket
import platform
import json
import os
import sys
import re
import csv
import argparse
from datetime import datetime
from pathlib import Path


# ─────────────────────────────────────────────
#  COLORS & FORMATTING
# ─────────────────────────────────────────────
class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"


def banner():
    print(f"""{Colors.CYAN}{Colors.BOLD}
    ╔══════════════════════════════════════════╗
    ║       🔧  IT SUPPORT TOOLKIT v1.0       ║
    ║    Automate. Diagnose. Resolve. Fast.    ║
    ╚══════════════════════════════════════════╝{Colors.RESET}
    """)


def log(status, message):
    icons = {"ok": f"{Colors.GREEN}✔{Colors.RESET}", 
             "fail": f"{Colors.RED}✘{Colors.RESET}",
             "warn": f"{Colors.YELLOW}⚠{Colors.RESET}", 
             "info": f"{Colors.CYAN}ℹ{Colors.RESET}"}
    print(f"  {icons.get(status, '•')} {message}")


# ─────────────────────────────────────────────
#  MODULE 1: SYSTEM HEALTH CHECK
# ─────────────────────────────────────────────
def system_health_check():
    """Run a full system diagnostic and return structured results."""
    print(f"\n{Colors.BOLD}── System Health Check ──{Colors.RESET}\n")
    
    results = {"timestamp": datetime.now().isoformat(), "checks": []}
    
    # OS Info
    os_info = f"{platform.system()} {platform.release()} ({platform.machine()})"
    log("info", f"OS: {os_info}")
    results["os"] = os_info
    
    # Hostname & IP
    hostname = socket.gethostname()
    try:
        local_ip = socket.gethostbyname(hostname)
    except socket.gaierror:
        local_ip = "Unable to resolve"
    log("info", f"Hostname: {hostname} | IP: {local_ip}")
    
    # Disk Usage
    if platform.system() != "Windows":
        try:
            disk = subprocess.run(["df", "-h", "/"], capture_output=True, text=True)
            lines = disk.stdout.strip().split("\n")
            if len(lines) > 1:
                parts = lines[1].split()
                usage_pct = int(parts[4].replace("%", ""))
                status = "ok" if usage_pct < 80 else ("warn" if usage_pct < 90 else "fail")
                log(status, f"Disk usage: {parts[4]} ({parts[2]} used of {parts[1]})")
                results["checks"].append({"name": "disk", "status": status, "value": usage_pct})
        except Exception:
            log("warn", "Could not check disk usage")
    
    # Memory
    if platform.system() == "Linux":
        try:
            with open("/proc/meminfo") as f:
                mem = {}
                for line in f:
                    parts = line.split()
                    mem[parts[0].rstrip(":")] = int(parts[1])
                total = mem["MemTotal"] / 1024 / 1024
                available = mem["MemAvailable"] / 1024 / 1024
                used_pct = round((1 - available / total) * 100)
                status = "ok" if used_pct < 80 else ("warn" if used_pct < 90 else "fail")
                log(status, f"Memory: {used_pct}% used ({available:.1f} GB free of {total:.1f} GB)")
                results["checks"].append({"name": "memory", "status": status, "value": used_pct})
        except Exception:
            log("warn", "Could not check memory")
    
    # CPU Load (Unix)
    if platform.system() != "Windows":
        try:
            load = os.getloadavg()
            cpu_count = os.cpu_count() or 1
            load_ratio = load[0] / cpu_count
            status = "ok" if load_ratio < 0.7 else ("warn" if load_ratio < 0.9 else "fail")
            log(status, f"CPU load: {load[0]:.2f} / {load[1]:.2f} / {load[2]:.2f} (cores: {cpu_count})")
            results["checks"].append({"name": "cpu_load", "status": status, "value": round(load_ratio, 2)})
        except Exception:
            log("warn", "Could not check CPU load")
    
    # Uptime
    if platform.system() == "Linux":
        try:
            with open("/proc/uptime") as f:
                uptime_seconds = float(f.read().split()[0])
                days = int(uptime_seconds // 86400)
                hours = int((uptime_seconds % 86400) // 3600)
                log("info", f"Uptime: {days}d {hours}h")
        except Exception:
            pass
    
    return results


# ─────────────────────────────────────────────
#  MODULE 2: NETWORK DIAGNOSTICS
# ─────────────────────────────────────────────
def network_diagnostics(targets=None):
    """Test connectivity to critical endpoints."""
    print(f"\n{Colors.BOLD}── Network Diagnostics ──{Colors.RESET}\n")
    
    if targets is None:
        targets = [
            ("Google DNS", "8.8.8.8"),
            ("Cloudflare DNS", "1.1.1.1"),
            ("Google", "google.com"),
            ("GitHub", "github.com"),
            ("AWS", "aws.amazon.com"),
        ]
    
    results = []
    
    for name, host in targets:
        try:
            start = datetime.now()
            socket.setdefaulttimeout(3)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ip = socket.gethostbyname(host)
            result = sock.connect_ex((ip, 443))
            latency = (datetime.now() - start).total_seconds() * 1000
            sock.close()
            
            if result == 0:
                status = "ok" if latency < 200 else "warn"
                log(status, f"{name} ({host}) → {latency:.0f}ms")
                results.append({"target": name, "host": host, "status": "reachable", "latency_ms": round(latency)})
            else:
                log("fail", f"{name} ({host}) → Connection refused")
                results.append({"target": name, "host": host, "status": "refused"})
        except socket.timeout:
            log("fail", f"{name} ({host}) → Timeout")
            results.append({"target": name, "host": host, "status": "timeout"})
        except socket.gaierror:
            log("fail", f"{name} ({host}) → DNS resolution failed")
            results.append({"target": name, "host": host, "status": "dns_fail"})
        except Exception as e:
            log("fail", f"{name} ({host}) → {str(e)}")
            results.append({"target": name, "host": host, "status": "error", "error": str(e)})
    
    return results


# ─────────────────────────────────────────────
#  MODULE 3: PORT SCANNER (Light)
# ─────────────────────────────────────────────
def port_scan(host, ports=None):
    """Scan common service ports on a target host."""
    print(f"\n{Colors.BOLD}── Port Scan: {host} ──{Colors.RESET}\n")
    
    if ports is None:
        ports = {
            22: "SSH", 80: "HTTP", 443: "HTTPS", 3306: "MySQL",
            5432: "PostgreSQL", 3389: "RDP", 8080: "HTTP-Alt",
            21: "FTP", 25: "SMTP", 53: "DNS", 5900: "VNC",
            6379: "Redis", 27017: "MongoDB", 8443: "HTTPS-Alt"
        }
    
    open_ports = []
    
    for port, service in sorted(ports.items()):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((host, port))
            sock.close()
            if result == 0:
                log("ok", f"Port {port:>5} ({service}) → OPEN")
                open_ports.append({"port": port, "service": service, "status": "open"})
            else:
                log("fail", f"Port {port:>5} ({service}) → closed")
        except Exception:
            log("warn", f"Port {port:>5} ({service}) → error")
    
    return open_ports


# ─────────────────────────────────────────────
#  MODULE 4: DNS LOOKUP
# ─────────────────────────────────────────────
def dns_lookup(domain):
    """Perform DNS resolution for a domain."""
    print(f"\n{Colors.BOLD}── DNS Lookup: {domain} ──{Colors.RESET}\n")
    
    results = {}
    
    try:
        ips = socket.getaddrinfo(domain, None)
        unique_ips = list(set(addr[4][0] for addr in ips))
        
        for ip in unique_ips:
            ip_type = "IPv6" if ":" in ip else "IPv4"
            log("ok", f"{ip_type}: {ip}")
        
        results["domain"] = domain
        results["addresses"] = unique_ips
        
        # Reverse DNS
        try:
            reverse = socket.gethostbyaddr(unique_ips[0])
            log("info", f"Reverse DNS: {reverse[0]}")
            results["reverse_dns"] = reverse[0]
        except Exception:
            log("warn", "Reverse DNS: not available")
            
    except socket.gaierror as e:
        log("fail", f"DNS resolution failed: {e}")
        results["error"] = str(e)
    
    return results


# ─────────────────────────────────────────────
#  MODULE 5: SERVICE STATUS CHECKER
# ─────────────────────────────────────────────
def check_services():
    """Check status of common IT services (Linux)."""
    print(f"\n{Colors.BOLD}── Service Status ──{Colors.RESET}\n")
    
    if platform.system() != "Linux":
        log("warn", "Service check is only available on Linux")
        return []
    
    services = ["sshd", "nginx", "apache2", "docker", "mysql", 
                 "postgresql", "redis-server", "cron", "ufw"]
    results = []
    
    for service in services:
        try:
            cmd = subprocess.run(
                ["systemctl", "is-active", service],
                capture_output=True, text=True, timeout=5
            )
            status = cmd.stdout.strip()
            if status == "active":
                log("ok", f"{service:.<25} running")
                results.append({"service": service, "status": "active"})
            elif status == "inactive":
                log("warn", f"{service:.<25} stopped")
                results.append({"service": service, "status": "inactive"})
            else:
                log("fail", f"{service:.<25} {status}")
                results.append({"service": service, "status": status})
        except FileNotFoundError:
            log("info", "systemctl not available")
            break
        except Exception:
            pass
    
    return results


# ─────────────────────────────────────────────
#  MODULE 6: GENERATE REPORT
# ─────────────────────────────────────────────
def generate_report(all_results, output_format="json"):
    """Export diagnostic results as JSON or CSV."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if output_format == "json":
        filename = f"it_report_{timestamp}.json"
        with open(filename, "w") as f:
            json.dump(all_results, f, indent=2, default=str)
    elif output_format == "csv":
        filename = f"it_report_{timestamp}.csv"
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Category", "Check", "Status", "Value"])
            for category, checks in all_results.items():
                if isinstance(checks, list):
                    for check in checks:
                        writer.writerow([category, check.get("name", ""), 
                                        check.get("status", ""), check.get("value", "")])
    
    log("ok", f"Report saved: {filename}")
    return filename


# ─────────────────────────────────────────────
#  CLI INTERFACE
# ─────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="🔧 IT Support Toolkit — Automate common diagnostics",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python it_toolkit.py --all                    Run all diagnostics
  python it_toolkit.py --health --network       System + network check
  python it_toolkit.py --portscan 192.168.1.1   Scan ports on a host
  python it_toolkit.py --dns google.com         DNS lookup
  python it_toolkit.py --all --report json      Full report as JSON
        """
    )
    
    parser.add_argument("--all", action="store_true", help="Run all diagnostic modules")
    parser.add_argument("--health", action="store_true", help="System health check")
    parser.add_argument("--network", action="store_true", help="Network connectivity test")
    parser.add_argument("--portscan", type=str, metavar="HOST", help="Port scan a target host")
    parser.add_argument("--dns", type=str, metavar="DOMAIN", help="DNS lookup for a domain")
    parser.add_argument("--services", action="store_true", help="Check service statuses")
    parser.add_argument("--report", choices=["json", "csv"], help="Export results to file")
    
    args = parser.parse_args()
    
    if len(sys.argv) == 1:
        banner()
        parser.print_help()
        return
    
    banner()
    all_results = {}
    
    if args.all or args.health:
        all_results["health"] = system_health_check()
    
    if args.all or args.network:
        all_results["network"] = network_diagnostics()
    
    if args.portscan:
        all_results["portscan"] = port_scan(args.portscan)
    
    if args.dns:
        all_results["dns"] = dns_lookup(args.dns)
    
    if args.all or args.services:
        all_results["services"] = check_services()
    
    if args.report:
        generate_report(all_results, args.report)
    
    print(f"\n{Colors.DIM}  Done. {len(all_results)} module(s) executed.{Colors.RESET}\n")


if __name__ == "__main__":
    main()
