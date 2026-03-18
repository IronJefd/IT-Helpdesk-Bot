# 🔧 IT Support Toolkit

> A lightweight, zero-dependency CLI tool for IT Support Engineers to automate common diagnostic and troubleshooting tasks.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey)

---

## Why This Exists

Every IT support engineer runs the same 10 commands daily: check disk, check memory, ping hosts, scan ports, verify services. **This toolkit wraps all of that into a single command** with structured output, color-coded results, and exportable reports.

No pip installs. No dependencies. Just Python 3.8+ and you're ready.

---

## ⚡ Quick Start

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/it-support-toolkit.git
cd it-support-toolkit

# Run all diagnostics
python it_toolkit.py --all

# Export a full report
python it_toolkit.py --all --report json
```

---

## 🧩 Modules

| Module | Flag | Description |
|--------|------|-------------|
| **System Health** | `--health` | OS info, disk, memory, CPU load, uptime |
| **Network Diagnostics** | `--network` | Connectivity tests to critical endpoints |
| **Port Scanner** | `--portscan HOST` | Scans 14 common service ports |
| **DNS Lookup** | `--dns DOMAIN` | Forward + reverse DNS resolution |
| **Service Status** | `--services` | Check systemd services (Linux) |
| **Report Export** | `--report json\|csv` | Save results for documentation |

---

## 📸 Sample Output

```
    ╔══════════════════════════════════════════╗
    ║       🔧  IT SUPPORT TOOLKIT v1.0       ║
    ║    Automate. Diagnose. Resolve. Fast.    ║
    ╚══════════════════════════════════════════╝

── System Health Check ──

  ℹ OS: Linux 5.15.0 (x86_64)
  ℹ Hostname: workstation | IP: 192.168.1.42
  ✔ Disk usage: 45% (98G used of 256G)
  ✔ Memory: 62% used (5.8 GB free of 16.0 GB)
  ✔ CPU load: 1.24 / 1.08 / 0.95 (cores: 8)
  ℹ Uptime: 12d 6h

── Network Diagnostics ──

  ✔ Google DNS (8.8.8.8) → 12ms
  ✔ Cloudflare DNS (1.1.1.1) → 8ms
  ✔ Google (google.com) → 23ms
  ✔ GitHub (github.com) → 45ms
  ⚠ AWS (aws.amazon.com) → 187ms
```

---

## 🗂 Use Cases

- **Daily health checks** before your shift starts
- **Incident response** — quick triage of connectivity and services
- **Onboarding documentation** — export system reports for new hires
- **Interview prep** — demonstrate real automation skills
- **Ticket documentation** — attach JSON/CSV reports to tickets

---

## 🔮 Roadmap

- [ ] Email/Slack alert integration
- [ ] SSL certificate expiration checker
- [ ] Active Directory / LDAP connectivity test
- [ ] Scheduled runs via cron with diff reporting
- [ ] Windows native support improvements
- [ ] Docker container health checks

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit PRs.

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/ssl-checker`)
3. Commit your changes (`git commit -m 'Add SSL cert checker'`)
4. Push to the branch (`git push origin feature/ssl-checker`)
5. Open a Pull Request

---

## 📄 License

MIT License — use it, fork it, make it yours.

---

**Built by an IT Support Engineer, for IT Support Engineers.**
