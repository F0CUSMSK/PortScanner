# Contributing to PortScanner

Thanks for your interest in contributing! This is an educational project, and contributions are welcome.

## Code of Conduct

- Be respectful
- This is an **educational tool**, not for hacking
- Focus on learning and teaching
- Help others understand networking concepts

## How to Contribute

### 1. Fork the Repository
```bash
git clone https://github.com/yourusername/portscanner.git
cd portscanner
```

### 2. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 3. Make Your Changes

#### Code Style
- Use Python 3.7+ compatible code
- Follow PEP 8 style guide
- Add docstrings to all functions and classes
- Use type hints where possible

#### Example:
```python
def scan_port(self, port: int) -> ScanResult:
    """
    Scan a single port and return the result.
    
    Friendly explanation of what this does in plain English.
    
    Args:
        port: The port number (1-65535)
    
    Returns:
        ScanResult object with scan details
    """
    # Your code here
```

### 4. Test Your Changes
```bash
# Run a quick scan to make sure nothing broke
python3 main.py --target 127.0.0.1 --ports 80,443,22
```

### 5. Submit a Pull Request
- Clear description of what you changed
- Explain why this change is needed
- Link any related issues

## Areas for Contribution

### High Priority
- [ ] Add more port-to-service mappings (help users see fewer "UNKNOWN" ports)
- [ ] Improve error messages (make them friendlier)
- [ ] Add more output formats (CSV, XML, etc.)
- [ ] Better banner grabbing for service detection

### Medium Priority
- [ ] Add IPv6 support
- [ ] UDP port scanning
- [ ] Service version detection
- [ ] Performance optimizations
- [ ] More detailed logging options

### Low Priority
- [ ] GUI/Web interface
- [ ] Configuration file support
- [ ] API wrapper

## Project Structure

```
portscanner/
├── utils/
│   ├── validator.py      # Input validation
│   └── logger.py         # Logging & output
├── scanner/
│   ├── port_scanner.py        # Core scanning
│   ├── service_detector.py    # Port-to-service mapping
│   └── host_scanner.py        # Multi-host orchestration
└── exporters/
    ├── json_exporter.py   # JSON output
    ├── txt_exporter.py    # Text output
    └── html_exporter.py   # HTML reports

main.py      # CLI entry point
```

## Adding New Service Ports

In `portscanner/scanner/service_detector.py`:

```python
PORT_SERVICES: Dict[int, Service] = {
    # ... existing ports ...
    1234: Service(1234, "myservice", "tcp", "My Service Description", True),
    # Add your new port here ↑
}
```

Guidelines:
- Port number should be accurate
- Service name should be short (lowercase, hyphens ok)
- Description should be user-friendly
- Mark `common=True` only for well-known services

## Testing Guidelines

### Test Cases to Check
1. **Happy Path**: Normal scan with valid inputs
2. **Edge Cases**: Empty files, invalid IPs, port ranges
3. **Error Handling**: Non-existent files, permission errors
4. **Performance**: Does it still work with 1000+ ports?

### Manual Testing
```bash
# Test interactive mode
python3 main.py --interactive

# Test single target
python3 main.py --target 127.0.0.1 --ports 22,80,443

# Test file input
echo "127.0.0.1" > test_targets.txt
python3 main.py --file test_targets.txt --ports 1-100

# Test all export formats
python3 main.py --target 127.0.0.1 --ports 1-100 --export all
```

## Documentation Guidelines

- Keep docstrings friendly and explain the "why"
- Use emojis sparingly in code (OK in docstrings, not in logic)
- Explain complex concepts with analogies
- Include examples in docstrings

## Before Submitting

- [ ] Code follows PEP 8 style
- [ ] All docstrings are present and friendly
- [ ] No debug print statements left in code
- [ ] Tested on Python 3.7+
- [ ] No external dependencies added (if possible)
- [ ] README/GETTING_STARTED updated if user-facing changes

## Questions?

- Check existing [issues](https://github.com/yourusername/portscanner/issues)
- Read [README.md](README.md) and [GETTING_STARTED.md](GETTING_STARTED.md)
- Ask in discussions or open an issue!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Happy coding! 🎓
