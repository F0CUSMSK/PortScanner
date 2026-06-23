

import argparse
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from portscanner.utils.validator import validate_all_inputs, InputValidator
from portscanner.utils.logger import Logger
from portscanner.scanner.host_scanner import HostScanner
from portscanner.exporters.json_exporter import export_to_json
from portscanner.exporters.txt_exporter import export_to_text
from portscanner.exporters.html_exporter import export_to_html


def interactive_mode():
    """
    🎯 Interactive Mode - Let's set up your scan step by step!
    
    Perfect if you're not sure what command-line options to use.
    Just answer a few friendly questions and we'll do the rest!
    """
    print("\n" + "=" * 70)
    print("🎯 Welcome to PortScanner Interactive Mode!")
    print("=" * 70)
    print("I'll ask you a few questions to set up your port scan.\n")
    
    # Question 1: What do you want to scan?
    print("Step 1️⃣  : What would you like to scan?")
    print("   a) A single computer (IP address)")
    print("   b) Multiple computers")
    print("   c) Computers from a file")
    choice = input("\nEnter a, b, or c: ").strip().lower()
    
    if choice == 'a':
        while True:
            target = input("📍 Enter the IP address (e.g., 192.168.1.1): ").strip()
            if InputValidator.validate_ip_address(target):
                targets = [target]
                break
            else:
                print(f"❌ '{target}' is not a valid IP address.")
                print("💡 Tip: Use 4 numbers (0-255) separated by dots, e.g., 192.168.1.1")
    elif choice == 'b':
        while True:
            target_str = input("📍 Enter IPs separated by commas (e.g., 192.168.1.1,192.168.1.2): ").strip()
            candidates = [t.strip() for t in target_str.split(',')]
            invalid = [ip for ip in candidates if not InputValidator.validate_ip_address(ip)]
            if not invalid:
                targets = candidates
                break
            else:
                print(f"❌ Invalid IP address(es): {', '.join(invalid)}")
                print("💡 Tip: Use 4 numbers (0-255) separated by dots, e.g., 192.168.1.1")
    elif choice == 'c':
        target_file = input("📁 Enter the filename (e.g., targets.txt): ").strip()
        try:
            targets = InputValidator.read_targets_from_file(target_file)
            print(f"✓ Loaded {len(targets)} target(s) from {target_file}")
        except (FileNotFoundError, ValueError, IOError) as e:
            print(f"❌ {e}")
            sys.exit(1)
    else:
        print("❌ Invalid choice. Using default: single computer")
        while True:
            target = input("📍 Enter the IP address: ").strip()
            if InputValidator.validate_ip_address(target):
                targets = [target]
                break
            else:
                print(f"❌ '{target}' is not a valid IP address.")
                print("💡 Tip: Use 4 numbers (0-255) separated by dots, e.g., 192.168.1.1")
    
    # Question 2: Which ports to scan?
    print("\n\nStep 2️⃣  : Which ports do you want to scan?")
    print("   a) Common ports (1-1000) - FAST ⚡")
    print("   b) Well-known ports (1-1023)")
    print("   c) All ports (1-65535) - SLOW 🐢")
    print("   d) Custom range (e.g., 20-443)")
    ports_choice = input("\nEnter a, b, c, or d: ").strip().lower()
    
    if ports_choice == 'a':
        port_range = '1-1000'
        print("✓ Will scan ports 1-1000 (should take ~2 seconds)")
    elif ports_choice == 'b':
        port_range = '1-1023'
        print("✓ Will scan ports 1-1023 (system ports)")
    elif ports_choice == 'c':
        port_range = 'all'
        print("✓ Will scan ALL ports (this will take a while...)")
    elif ports_choice == 'd':
        port_range = input("Enter port range (e.g., 22-443): ").strip()
        print(f"✓ Will scan ports {port_range}")
    else:
        port_range = '1-1000'
        print("✓ Using default: ports 1-1000")
    
    # Question 3: Export format?
    print("\n\nStep 3️⃣  : How would you like to save the results?")
    print("   a) HTML Report (pretty and interactive) 🎨")
    print("   b) Text Report (simple and readable) 📄")
    print("   c) JSON Data (for analysis) 📊")
    print("   d) All formats")
    export_choice = input("\nEnter a, b, c, or d: ").strip().lower()
    
    if export_choice == 'a':
        export_format = 'html'
        print("✓ Will create a beautiful HTML report")
    elif export_choice == 'b':
        export_format = 'txt'
        print("✓ Will create a text report")
    elif export_choice == 'c':
        export_format = 'json'
        print("✓ Will create a JSON data file")
    elif export_choice == 'd':
        export_format = 'all'
        print("✓ Will create all formats (JSON, TXT, HTML)")
    else:
        export_format = 'html'
        print("✓ Using default: HTML report")
    
    # Summary
    print("\n\n" + "=" * 70)
    print("✅ Great! Here's what we'll do:")
    print("=" * 70)
    print(f"  • Scan: {len(targets)} target(s)")
    print(f"  • Ports: {port_range}")
    print(f"  • Export: {export_format}")
    print("  • Speed: Using 50 threads per computer")
    print("\nReady to start? Press Enter to begin scanning...\n")
    input()
    
    # Convert back to command-line arguments
    return {
        'targets': targets,
        'ports': port_range,
        'export': export_format,
        'threads': 50,
        'timeout': 2.0,
        'output': 'reports',
        'verbose': False,
        'quiet': False
    }


def create_argument_parser():
    """
    Create and return the command-line argument parser.

    Returns:
        ArgumentParser configured with all required arguments
    """
    parser = argparse.ArgumentParser(
        prog='PortScanner',
        description='🔍 Learn How Networks Work - Educational Port Scanning Tool',
        epilog='''
Examples:
  # Scan a single host
  python main.py --target 192.168.1.1 --ports 1-1000

  # Scan multiple hosts
  python main.py --target 192.168.1.1,192.168.1.2 --ports 22,80,443

  # Scan all ports
  python main.py --target 192.168.1.1 --ports all

  # Scan from file
  python main.py --file targets.txt --ports 1-65535

  # Export results in multiple formats
  python main.py --target 192.168.1.1 --ports 1-1000 --export all

  # Custom thread count and timeout
  python main.py --target 192.168.1.1 --ports 1-1000 --threads 100 --timeout 1.0

Note: ONLY scan networks and systems you own or have permission to scan.
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Target input options
    target_group = parser.add_mutually_exclusive_group(required=False)
    target_group.add_argument(
        '--target', '-t',
        type=str,
        help='Target IP(s) - single IP or comma-separated (e.g., 192.168.1.1,192.168.1.2)'
    )
    target_group.add_argument(
        '--file', '-f',
        type=str,
        help='File containing target IPs (one per line)'
    )
    target_group.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='Interactive mode - answer friendly questions to set up your scan'
    )

    # Port options
    parser.add_argument(
        '--ports', '-p',
        type=str,
        default='1-1000',
        help='Port range to scan (e.g., "1-1000" or "all" for 1-65535, default: 1-1000)'
    )

    # Threading options
    parser.add_argument(
        '--threads',
        type=int,
        default=50,
        help='Number of threads per host (default: 50, max: 256)'
    )

    parser.add_argument(
        '--timeout',
        type=float,
        default=2.0,
        help='Socket timeout in seconds (default: 2.0)'
    )

    # Export options
    parser.add_argument(
        '--export', '-e',
        type=str,
        default='txt',
        help='Export formats (json, txt, html, or all, default: txt)'
    )

    parser.add_argument(
        '--output', '-o',
        type=str,
        default='reports',
        help='Output directory for reports (default: reports)'
    )

    # Logging options
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )

    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Minimal output (only results)'
    )

    return parser


def main():
    """
    🚀 Main entry point for the port scanner.

    This function:
    1. Lets you choose: command-line or interactive mode
    2. Validates your choices
    3. Sets up the scanning
    4. Runs the scan
    5. Saves the results
    6. Shows you a nice summary
    
    Think of it like a cooking recipe - we follow each step in order!
    """
    # Parse arguments
    parser = create_argument_parser()
    args = parser.parse_args()
    
    # Check if interactive mode was requested
    if args.interactive:
        interactive_config = interactive_mode()
        targets = interactive_config['targets']
        port_range_str = interactive_config['ports']
        threads = interactive_config['threads']
        export_formats_str = interactive_config['export']
        output_dir = interactive_config['output']
        timeout = interactive_config['timeout']
    elif not args.target and not args.file:
        print("\n" + "=" * 70)
        print("👋 Welcome to PortScanner!")
        print("=" * 70)
        print("\nI see you haven't told me what to scan.")
        print("Would you like help? (Press Enter for interactive mode, or Ctrl+C to exit)\n")
        print("Try: python main.py --help")
        print("  Or: python main.py --interactive\n")
        sys.exit(1)
    else:
        port_range_str = args.ports
        threads = args.threads
        export_formats_str = args.export
        output_dir = args.output
        timeout = args.timeout
        targets = None

    try:
        # Validate all inputs
        print("\n✓ Checking your settings...")
        
        # Determine which target input to use
        if args.interactive:
            target_input = None  # We already have targets from interactive mode
            target_file_input = None
        else:
            target_input = args.target
            target_file_input = args.file
        
        validated = validate_all_inputs(
            targets=target_input,
            ports=port_range_str,
            threads=threads,
            export=export_formats_str,
            target_file=target_file_input,
            targets_list=targets if args.interactive else None  # Pass the targets from interactive mode
        )

        targets = validated['targets']
        port_range = validated['port_range']
        threads = validated['threads']
        export_formats = validated['export_formats']

        print(f"✓ Everything looks good!")
        print(f"  📍 Targets: {len(targets)} computer(s)")
        print(f"  🔍 Ports: {port_range[0]}-{port_range[1]}")
        print(f"  ⚡ Threads: {threads} per computer")
        print()

        # Create logger
        logger = Logger(output_dir, 'scanner.log')

        if not args.quiet:
            logger.info(f"🚀 Starting scan of {len(targets)} computer(s)...")

        # Create host scanner
        scanner = HostScanner(
            hosts=targets,
            port_range=port_range,
            threads_per_host=threads,
            hosts_parallel=min(5, len(targets)),
            logger=logger,
            timeout=timeout
        )

        # Execute scan
        print("📡 Scanning... (this might take a moment)\n")
        results = scanner.scan_all()

        # Clear progress line
        print()

        # Display results
        if not args.quiet:
            scanner.print_results()

        # Get summary
        summary = scanner.get_summary()

        print()
        logger.scan_summary(
            total_hosts=summary['total_hosts'],
            total_ports=summary['total_ports_scanned'],
            elapsed_time=summary['total_scan_time']
        )

        # Export results
        print("\n💾 Saving your results...")
        exported_files = []

        if 'json' in export_formats:
            json_file = export_to_json(scanner, output_dir)
            exported_files.append(json_file)
            logger.success(f"📊 JSON data: {json_file}")

        if 'txt' in export_formats:
            txt_file = export_to_text(scanner, output_dir)
            exported_files.append(txt_file)
            logger.success(f"📄 Text report: {txt_file}")

        if 'html' in export_formats:
            html_file = export_to_html(scanner, output_dir)
            exported_files.append(html_file)
            logger.success(f"🎨 HTML report: {html_file}")

        # Finalize logging
        log_file = logger.finalize()
        print(f"📝 Full log: {log_file}")

        # Summary
        print("\n" + "=" * 70)
        print(f"🎉 All Done! Scan Complete!")
        print("=" * 70)
        print(f"📊 Results Summary:")
        print(f"   • Computers scanned: {summary['total_hosts']}")
        print(f"   • Ports checked: {summary['total_ports_scanned']:,}")
        print(f"   • Open ports found: {summary['total_open_ports']} 🎯")
        print(f"   • Time taken: {summary['total_scan_time']:.2f} seconds ⏱️")
        print()
        print(f"📂 All reports saved to: {output_dir}/")
        print("=" * 70)
        print("\n💡 Next steps:")
        print("   • Check the HTML report in a web browser for a nice view")
        print("   • Review the JSON file to process data further")
        print("   • Check the log file for detailed information")
        print()

        return 0

    except ValueError as e:
        print(f"\n❌ Oops! I found an issue: {e}", file=sys.stderr)
        return 1
    except FileNotFoundError as e:
        print(f"\n❌ File Error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\n\n⚠️  Scan stopped (you pressed Ctrl+C)")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
