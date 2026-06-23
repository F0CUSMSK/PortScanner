# 🚀 Getting Started with PortScanner

Welcome! This guide will get you up and running in 5 minutes.

## Installation

### Option 1: Direct Installation (Fastest)

```bash
# Clone the repository
git clone https://github.com/F0CUSMSK/PortScanner.git
cd portscanner

# Run directly (no installation needed!)
python3 main.py --interactive
```

### Option 2: Install as a Package

```bash
git clone https://github.com/F0CUSMSK/PortScanner.git
cd portscanner

# Install in development mode
pip install -e .

# Now you can run from anywhere
portscanner --interactive
```

## Quick Start

### 1️⃣ **Interactive Mode (Easiest)**
```bash
python3 main.py --interactive
```
Answer a few friendly questions and we'll handle the rest!

### 2️⃣ **Scan Your Own Computer**
```bash
# Scan localhost (your own computer)
python3 main.py --target 127.0.0.1 --ports 1-1000
```

### 3️⃣ **Scan Your Network**
```bash
# Scan a specific computer (get permission first!)
python3 main.py --target 192.168.1.1 --ports 1-1000

# Scan multiple computers
python3 main.py --target 192.168.1.1,192.168.1.2,192.168.1.3 --ports 1-1000
```

### 4️⃣ **Scan from a File**
Create `targets.txt`:
```
192.168.1.1
192.168.1.2
192.168.1.3
```

Then run:
```bash
python3 main.py --file targets.txt --ports 1-1000
```

## View Your Results

After scanning, check the `reports/` folder:

- **scan_*.html** - Open in your browser for a beautiful interactive report 🎨
- **scan_*.txt** - Simple text report 📄
- **scan_*.json** - Data in JSON format for analysis 📊
- **scanner.log** - Detailed scan log 📝

## All Commands

### Basic Options
```bash
# Scan specific ports
python3 main.py --target 192.168.1.1 --ports 22,80,443

# Scan a range
python3 main.py --target 192.168.1.1 --ports 1-1000

# Scan all ports (takes longer)
python3 main.py --target 192.168.1.1 --ports all
```

### Performance Options
```bash
# Speed it up (more threads)
python3 main.py --target 192.168.1.1 --ports 1-1000 --threads 100

# Slower but more reliable (for distant networks)
python3 main.py --target 192.168.1.1 --ports 1-1000 --timeout 5.0
```

### Export Options
```bash
# Export in multiple formats
python3 main.py --target 192.168.1.1 --ports 1-1000 --export all

# Specific format
python3 main.py --target 192.168.1.1 --ports 1-1000 --export html
```

### Output Options
```bash
# Save to custom directory
python3 main.py --target 192.168.1.1 --ports 1-1000 --output ./my_reports

# Verbose output
python3 main.py --target 192.168.1.1 --ports 1-1000 --verbose

# Quiet mode (minimal output)
python3 main.py --target 192.168.1.1 --ports 1-1000 --quiet
```

## Get Help

```bash
python3 main.py --help
```

## Requirements

- **Python 3.7+** (check with `python3 --version`)
- **No external packages needed!** We use only Python's standard library

## Troubleshooting

### "Permission denied" for low ports (1-1023)
Some systems require admin/root privileges for ports below 1024.

**Windows:**
```bash
# Run Command Prompt as Administrator, then:
python3 main.py --target 192.168.1.1 --ports 1-1023
```

**Mac/Linux:**
```bash
sudo python3 main.py --target 192.168.1.1 --ports 1-1023
```

### "Command not found: python3"
Try `python` instead:
```bash
python main.py --interactive
```

### Report not saving
Make sure the `reports/` folder exists and you have write permissions:
```bash
mkdir reports
```

## Learning Path

1. **Beginner**: Scan localhost (127.0.0.1) to learn concepts
2. **Intermediate**: Scan your home network with permission
3. **Advanced**: Read the code and understand the threading architecture

See [README.md](README.md) for more details on concepts!

## Legal Notice

⚠️ **Important!**
- ✅ Scan only computers you own
- ✅ Scan only with explicit written permission
- ❌ DO NOT scan other people's networks without permission
- ❌ Unauthorized scanning may be illegal

This is an **educational tool** for learning networking concepts.

## Next Steps

- Read the full [README.md](README.md)
- Check [portscanner/](portscanner/) for code structure
- Explore the scan results in HTML reports
- Modify the code to learn more!

Happy scanning! 🎓
