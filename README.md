# 🔍 PortScanner - Learn How Networks Work!

A **friendly, educational** port scanner that teaches you about networking while being fun to use!

Think of it like a "network detective" that knocks on doors (ports) and sees which ones answer back.

## ✨ Features

- **Fast Parallel Scanning** - Scan multiple hosts and ports simultaneously
- **Service Detection** - Identify services running on open ports
- **Multiple Export Formats** - JSON, TXT, and HTML reports
- **Professional Logging** - Colored console output and file logging
- **Educational Focus** - Learn about networking, sockets, and threading
- **No External Dependencies** - Uses only Python standard library

## 📦 Installation & Quick Start

### Requirement: Python 3.7+
Check your Python version:
```bash
python3 --version
```

### Option 1: Quick Run (No Installation)
```bash
# Clone the repository
git clone https://github.com/yourusername/portscanner.git
cd portscanner

# Run in interactive mode
python3 main.py --interactive
```

### Option 2: Install Package
```bash
git clone https://github.com/yourusername/portscanner.git
cd portscanner
pip install -e .
```

**No pip install of dependencies needed!** We use only Python's standard library. 

👉 **[See GETTING_STARTED.md for detailed instructions](GETTING_STARTED.md)**

## 🎓 Educational Value

This project teaches:
- **Sockets & TCP/IP** - How network connections work
- **Threading** - Parallel processing for speed
- **Port States** - OPEN, CLOSED, FILTERED concepts
- **Service Detection** - Port-to-service mapping (IANA standard)
- **CLI Development** - Command-line argument parsing
- **Professional Code** - Type hints, documentation, error handling

## ⚠️ Important Disclaimer

**This tool is for educational purposes only.**

- ✅ Scan networks you own
- ✅ Scan with explicit written permission
- ✅ Learn networking concepts
- ❌ DO NOT scan other people's networks without permission
- ❌ DO NOT use for malicious purposes
- ❌ Unauthorized network scanning may be illegal

---

---

## 🚀 Quick Start (5 Minutes!)

### 1️⃣ Don't know where to start?

**Try the interactive mode!** It will ask you friendly questions:

```bash
python main.py --interactive
```

This is perfect if you're new - just answer the questions and we'll do the rest!

### 2️⃣ Know what you want?

```bash
# Scan YOUR computer (the easy one to test)
python main.py --target 127.0.0.1 --ports 1-1000

# Scan your home network (ask for permission first!)
python main.py --target 192.168.1.1 --ports 1-1000

# Scan MULTIPLE computers at once
python main.py --target 192.168.1.1,192.168.1.2 --ports 1-1000
```

That's it! It will show you what ports are "open" (services responding) and tell you what services are probably running.

---

## 📚 Beginner's Guide

### What is a "Port"?

Imagine your computer is an apartment building:
- The computer is the building
- Ports are like doors (numbered 1-65535)
- Some doors have services behind them (SSH, HTTP, etc.)
- Some doors are locked (closed ports)
- Some are blocked by security guards (firewall/filtered)

**Examples of common ports:**
- Port 22: SSH (secure remote login)
- Port 80: HTTP (websites)
- Port 443: HTTPS (secure websites)
- Port 3306: MySQL (database)

### What Happens When You Run a Scan?

```
1. You tell us which computer to scan (IP address)
2. We send small "hello" messages to each port
3. If a port says "hello back!" → It's OPEN ✓
4. If it says "go away!" → It's CLOSED ✗
5. If it doesn't answer → It's FILTERED (firewall blocking)
6. We create a nice report showing what we found
```

### Running Your First Scan

**Step 1: Find an IP to scan**

The safest IP to scan is your own computer:
```bash
# Windows: open Command Prompt
ipconfig

# Mac/Linux: open Terminal
ifconfig
```

Look for an IP like `192.168.x.x` or `10.0.0.x`

**Step 2: Run the scan**

```bash
python main.py --target YOUR_IP_HERE --ports 1-1000
```

Replace `YOUR_IP_HERE` with the IP you found.

**Step 3: Wait for results**

You'll see a progress bar. When it's done, it shows you the open ports!

**Step 4: Check the reports**

Look in the `reports/` folder for:
- `scan_*.html` - Pretty report (open in web browser!)
- `scan_*.txt` - Simple text version
- `scan_*.json` - Data for analysis

---

## 🤔 Common Questions (FAQ)

### "Can I break something with this?"

No! This tool only:
- Sends connection attempts (like knocking on a door)
- Doesn't exploit anything
- Doesn't send malicious data
- Doesn't modify anything

It's completely safe and read-only.

### "What if I don't know the IP address?"

**Option 1:** Find your own IP:
```bash
# Windows
ipconfig

# Mac/Linux  
ifconfig
```

**Option 2:** Scan your local network:
```bash
python main.py --target 192.168.1.1 --ports 1-1000
```

### "Why do some scans take longer?"

Port scanning takes time because we're:
- Connecting to many ports in parallel (threading)
- Waiting for responses (timeout = 2 seconds by default)
- Checking more ports = more time

**To make it faster:**
```bash
python main.py --target 192.168.1.1 --ports 1-1000 --threads 100 --timeout 1.0
```

### "What should I scan?"

**Good targets (YOU OWN THEM):**
- ✅ Your own computer (127.0.0.1)
- ✅ Your home network (with permission)
- ✅ Lab equipment (in school/training)
- ✅ Test servers you set up

**Bad targets (GET PERMISSION FIRST):**
- ❌ Your friend's computer
- ❌ Your school's network
- ❌ Your company's network
- ❌ Random IP addresses online

### "What do the colors mean?"

```
🟢 Green = Good/Success
🔴 Red = Problem/Error
🟡 Yellow = Warning
🔵 Blue = Information
```

### "Why does it say OPEN, CLOSED, FILTERED?"

- **OPEN** 🟢: Service is listening, we connected successfully!
- **CLOSED** 🔴: Port exists but nothing is listening
- **FILTERED** 🟡: Firewall is blocking our attempts (no response)

### "Can I scan a website?"

**Technically yes, but:**
- You need the website's IP address
- The website owner might have a firewall
- You might trigger security alerts
- **Always get permission first!**

```bash
# Find IP of a website
nslookup google.com  # Windows
dig google.com       # Mac/Linux

# But don't scan it without permission!
```

### "I got an error. What do I do?"

Common errors and fixes:

**"Invalid IP address"**
```
❌ python main.py --target "hello.world"
✅ python main.py --target 192.168.1.1
```

**"Port range invalid"**
```
❌ python main.py --ports 500-200  (start > end)
✅ python main.py --ports 200-500
```

**"Need admin/root for ports 1-1023"**
```
# Windows: Run as Administrator
# Mac/Linux:
sudo python3 main.py --target 192.168.1.1 --ports 1-1023
```

### "How do I scan from a file?"

Create a file called `targets.txt`:
```
192.168.1.1
192.168.1.2
192.168.1.3
# You can add comments with #
192.168.1.4
```

Then:
```bash
python main.py --file targets.txt --ports 1-1000
```

### "What if I want to scan many ports?"

```bash
# Scan all 65535 ports (takes about 30 seconds per computer)
python main.py --target 192.168.1.1 --ports all

# Or specify a big range
python main.py --target 192.168.1.1 --ports 1-65535
```

---

## 📖 Learning Path

### Level 1: Beginner
- [ ] Run the interactive mode: `python main.py --interactive`
- [ ] Scan your own computer: `python main.py --target 127.0.0.1`
- [ ] Check the HTML report in the `reports/` folder
- [ ] Read through the code and comments

### Level 2: Intermediate
- [ ] Scan your home network
- [ ] Understand what services are on different ports
- [ ] Look at the JSON report to see the data format
- [ ] Modify code to add custom messages

### Level 3: Advanced
- [ ] Study the threading architecture in `host_scanner.py`
- [ ] Understand how sockets work in `port_scanner.py`
- [ ] Add new features (banner grabbing, UDP scanning, etc.)
- [ ] Use the data for analysis/automation

---

## 🏗️ How It Works (Simple Version)

### The Big Picture

```
1. You run: python main.py --target 192.168.1.1

2. We ask: "What IP? What ports? How many threads?"

3. We check: "Are these valid? Do these files exist?"

4. We scan: "Hello port 22? Port 80? Port 443?"
           (We do this 50 at a time to be fast)

5. We identify: "Port 22 is open → SSH service"

6. We report: "Found 3 open ports! Here's an HTML report"

7. Done! You can view the report in your browser
```

### Threading - Why It's Fast

**Without threading (slow):**
```
Port 1: Check, wait 2 seconds
Port 2: Check, wait 2 seconds
Port 3: Check, wait 2 seconds
...
Total: 2000 seconds for 1000 ports 😴
```

**With threading (fast - our way):**
```
Ports 1-50: Check all at once, wait 2 seconds
Ports 51-100: Check all at once, wait 2 seconds
...
Total: 40 seconds for 1000 ports ⚡
```

We use something called **ThreadPoolExecutor** which is like having 50 workers all checking ports at the same time!

---

## 📖 Command-Line Options

### Required (one of):
```
--target, -t IP           Single IP or comma-separated (192.168.1.1,192.168.1.2)
--file, -f PATH           File containing IPs (one per line)
--interactive             Ask me friendly questions! (recommended for beginners)
```

### Optional:
```
--ports, -p RANGE         Port range: "1-1000" or "all" (default: 1-1000)
                          Examples: "22", "22-443", "1-65535", "all"

--threads INT             Threads per host (default: 50, max: 256)

--timeout FLOAT           Socket timeout in seconds (default: 2.0)

--export FORMATS          Export: json, txt, html, all (default: txt)

--output, -o DIR          Output directory (default: reports)

--verbose, -v             Enable verbose output

--quiet, -q               Minimal output (only results)
```

---

## 📊 Output Examples

### Console Output
```
╔════════════════════════════════════════════════════════════════════╗
║               PortScanner - Starting Multi-Host Scan               ║
║                          5 targets                                 ║
╚════════════════════════════════════════════════════════════════════╝

═════════════════════════════════════════════════════════════════════
=== Scanning Host: 192.168.1.1 ===
═════════════════════════════════════════════════════════════════════

[250/1000]  25% ████████░░░░░░░░░░░░░░░░ 192.168.1.1

[+] 22/tcp OPEN → SSH (Secure Shell)
[+] 80/tcp OPEN → HTTP (HyperText Transfer Protocol)
[+] 443/tcp OPEN → HTTPS (HTTP Secure)

✓ Host 192.168.1.1 scan complete: 3 open, 997 closed, 0 filtered (2.45s)
```

### JSON Report
```json
{
  "metadata": {
    "scan_time": "2024-06-23T14:30:45",
    "tool": "PortScanner",
    "version": "1.0.0"
  },
  "scan_summary": {
    "total_hosts": 1,
    "total_ports_scanned": 1000,
    "total_open_ports": 3,
    "total_closed_ports": 997,
    "total_filtered_ports": 0,
    "total_scan_time": 2.45,
    "avg_time_per_host": 2.45
  },
  "hosts": {
    "192.168.1.1": {
      "open_ports": [22, 80, 443],
      "services": [
        {
          "port": 22,
          "protocol": "tcp",
          "service": "ssh",
          "description": "Secure Shell (SSH)"
        }
      ]
    }
  }
}
```

### HTML Report
Beautiful, interactive HTML report with:
- Summary statistics
- Visual charts and progress bars
- Port details organized by host
- Mobile-responsive design
- Print-friendly layout

---

## 📖 Command-Line Options

### Required (one of):
```
--target, -t IP           Single IP or comma-separated (192.168.1.1,192.168.1.2)
--file, -f PATH           File containing IPs (one per line)
```

### Optional:
```
--ports, -p RANGE         Port range: "1-1000" or "all" (default: 1-1000)
                          Examples: "22", "22-443", "1-65535", "all"

--threads INT             Threads per host (default: 50, max: 256)

--timeout FLOAT           Socket timeout in seconds (default: 2.0)

--export FORMATS          Export: json, txt, html, all (default: txt)

--output, -o DIR          Output directory (default: reports)

--verbose, -v             Enable verbose output

--quiet, -q               Minimal output (only results)
```

---

## 🏗️ Project Structure

```
PortScanner/
├── main.py                      # CLI entry point
├── requirements.txt             # Dependencies (empty - no external deps!)
├── README.md                    # This file
│
├── portscanner/
│   ├── __init__.py
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── validator.py         # Input validation
│   │   └── logger.py            # Logging & colored output
│   │
│   ├── scanner/
│   │   ├── __init__.py
│   │   ├── port_scanner.py      # Core TCP socket scanning
│   │   ├── service_detector.py  # Port-to-service mapping
│   │   └── host_scanner.py      # Multi-host orchestrator
│   │
│   └── exporters/
│       ├── __init__.py
│       ├── json_exporter.py     # JSON export
│       ├── txt_exporter.py      # Plain text export
│       └── html_exporter.py     # HTML report export
│
├── reports/                     # Output directory (auto-created)
│   ├── scanner.log              # Scan log
│   ├── scan_20240623_143045.json
│   ├── scan_20240623_143045.txt
│   └── scan_20240623_143045.html
│
└── targets.txt                  # Example: IPs to scan (one per line)
```

---

## 🔬 Architecture

### Two-Level Threading

**Level 1: Host Parallelism**
- Scan 5 hosts simultaneously
- Each host gets independent resources

**Level 2: Port Parallelism**
- Each host scans 50 ports simultaneously
- Uses ThreadPoolExecutor for thread pool management

**Result:** 5 hosts × 50 ports = scanning 250 ports in parallel!

### Module Dependencies

```
main.py
  ├─ validator.py          (Input validation)
  ├─ logger.py             (Logging)
  ├─ host_scanner.py       (Multi-host orchestrator)
  │   ├─ port_scanner.py   (Single-host TCP scanning)
  │   ├─ service_detector.py (Service mapping)
  │   └─ logger.py
  └─ exporters/
      ├─ json_exporter.py
      ├─ txt_exporter.py
      └─ html_exporter.py
```

---

## 📚 Key Concepts Explained

### Port States

- **OPEN** - Port is listening, connection accepted (service running)
- **CLOSED** - Port is not listening, connection refused by host
- **FILTERED** - Firewall blocks the connection, no response received

### Socket Connection

1. Create TCP socket
2. Attempt connection to `host:port`
3. If succeeds → PORT IS OPEN
4. If refused → PORT IS CLOSED
5. If times out → PORT IS FILTERED (firewall)

### Threading Architecture

```
Sequential (SLOW):
Port 1→3s, Port 2→3s, Port 3→3s = 9 seconds

Parallel (FAST):
Ports 1,2,3 at once = 3 seconds
```

We use `ThreadPoolExecutor` with 50 worker threads to achieve this.

### IANA Port Categories

- **0-1023** (Well-known): System services (SSH, HTTP, DNS, etc.)
- **1024-49151** (Registered): Application-specific (MySQL, PostgreSQL, etc.)
- **49152-65535** (Dynamic): Ephemeral/temporary use by OS

---

## 🔐 Security & Ethics

### What This Tool Does

✅ Attempts TCP connections to ports  
✅ Detects which ports are responding  
✅ Identifies likely services based on port number  
✅ Educational only - no exploitation  

### What This Tool Does NOT Do

❌ Exploit vulnerabilities  
❌ Send malicious payloads  
❌ Brute force or crack passwords  
❌ Perform privilege escalation  
❌ Access or exfiltrate data  

### Legal Use

This tool is intended **ONLY** for:
- Networks you own
- Systems you have explicit written permission to scan
- Educational learning environments
- Your own lab equipment

---

## 📈 Performance Tips

### For Fast Scanning

```bash
# Increase threads, lower timeout (for fast networks)
python main.py --target 192.168.1.1 --ports 1-65535 --threads 100 --timeout 1.0
```

### For Reliable Scanning

```bash
# Decrease threads, increase timeout (for slow/remote networks)
python main.py --target example.com --ports 1-65535 --threads 20 --timeout 5.0
```

### For Many Hosts

```bash
# Scan multiple hosts in parallel
python main.py --file many_targets.txt --ports 1-1000
```

---

## 🐛 Troubleshooting

### Port requires admin/root?

Some systems restrict scanning privileged ports (1-1023). Run with:
```bash
# Windows (Admin Command Prompt)
python main.py --target 192.168.1.1 --ports 1-1023

# Linux/Mac (with sudo)
sudo python3 main.py --target 192.168.1.1 --ports 1-1023
```

### Scan is slow?

Increase threads and decrease timeout:
```bash
python main.py --target 192.168.1.1 --threads 150 --timeout 1.0 --ports 1-1000
```

### No results?

Check if target is reachable:
```bash
ping 192.168.1.1  # Test connectivity first
```

---

## 📝 Example Workflows

### Quick Local Network Scan

```bash
python main.py --target 192.168.1.0/24 --ports 1-1000 --export all
```

### Scan Multiple Hosts from File

```bash
# Create targets.txt with one IP per line
python main.py --file targets.txt --ports 1-1000 --export all --output ./my_reports
```

### Comprehensive Scan with Logging

```bash
python main.py --target 192.168.1.1 --ports all --threads 100 --verbose
# Check reports/ directory for results
```

---

## 🤝 Contributing

This is an educational project. Contributions welcome for:
- Better documentation
- Additional service mappings
- Performance improvements
- Bug fixes

---

## 📜 License

MIT License - See LICENSE file for details

---

## 📚 Learning Resources

Included concepts teach you about:

1. **Networking**
   - TCP/IP Protocol Stack
   - Sockets and Port Communication
   - Network Services

2. **Python Programming**
   - Threading and Concurrency
   - Type Hints and Annotations
   - CLI Development with argparse
   - File I/O and Serialization

3. **Cybersecurity**
   - Reconnaissance Techniques
   - Service Enumeration
   - Defensive Concepts

---

## ⚠️ Disclaimer

Users are responsible for ensuring they have explicit permission to scan any networks or systems. Unauthorized network scanning may be illegal. This tool is provided for educational purposes only.

**Remember: With great power comes great responsibility.** 🦸

---

## 🎯 Future Enhancements

Potential additions (educational):
- UDP port scanning
- Ping sweep for host discovery
- Traceroute functionality
- Banner grabbing (safe version)
- SSL/TLS detection
- Web service fingerprinting
- DNS enumeration

---

## 📞 Questions?

This tool is designed to help you learn cybersecurity concepts safely and responsibly.

Happy scanning! 🎯
