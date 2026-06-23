"""
📄 Plain Text Exporter - Simple & Readable!

This creates a simple text file that:
  ✓ Anyone can read (no special software needed)
  ✓ Easy to email or share
  ✓ Looks good when printed
  ✓ Works everywhere (Windows, Mac, Linux)

WHY USE TEXT?
  • Super simple and readable
  • No special tools needed
  • Good for email or documentation
  • Prints beautifully

The output looks like:
═══════════════════════════════════════
PORT SCANNER RESULTS
═══════════════════════════════════════

SCAN SUMMARY:
  Total Hosts: 5
  Total Ports Scanned: 5000
  Open Ports: 23 ✓
  Closed Ports: 4977 ✗
  Filtered Ports: 0 🟡
  Total Time: 45.3 seconds ⏱️

HOST RESULTS:
─────────────────────────────────────

Host: 192.168.1.1
  Open Ports: 22, 80, 443
  Details:
    22/tcp: SSH (Remote login)
    80/tcp: HTTP (Websites)
    443/tcp: HTTPS (Secure websites)

Good for:
  • Quick reports
  • Email summaries
  • Print documentation
  • General viewing
"""

from datetime import datetime
from pathlib import Path
from typing import List
from portscanner.scanner.host_scanner import HostScanner
from portscanner.scanner.service_detector import ServiceDetector


class TextExporter:
    """Exports scan results to plain text format."""

    def __init__(self, output_dir: str = 'reports'):
        """
        Initialize the text exporter.

        Args:
            output_dir: Directory to save text files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export(
        self,
        scanner: HostScanner,
        filename: str = None
    ) -> str:
        """
        Export scan results to plain text file.

        Args:
            scanner: HostScanner instance with completed scan
            filename: Output filename (default: scan_TIMESTAMP.txt)

        Returns:
            Path to the exported file

        Example:
            exporter = TextExporter('reports')
            filepath = exporter.export(scanner, 'results.txt')
        """
        # Generate filename if not provided
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'scan_{timestamp}.txt'

        filepath = self.output_dir / filename

        # Build the text output
        text_content = self._build_text_report(scanner)

        # Write to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text_content)

        return str(filepath)

    def _build_text_report(self, scanner: HostScanner) -> str:
        """
        Build the complete text report.

        Args:
            scanner: HostScanner instance

        Returns:
            Formatted text report as string
        """
        lines = []

        # Header
        lines.append('=' * 70)
        lines.append('PORT SCANNER RESULTS'.center(70))
        lines.append('=' * 70)
        lines.append('')

        # Metadata
        lines.append('SCAN INFORMATION:')
        lines.append(f"  Scan Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append('')

        # Summary
        summary = scanner.get_summary()
        lines.append('SCAN SUMMARY:')
        lines.append(f"  Total Hosts Scanned: {summary['total_hosts']}")
        lines.append(f"  Total Ports Scanned: {summary['total_ports_scanned']:,}")
        lines.append(f"  Open Ports Found: {summary['total_open_ports']}")
        lines.append(f"  Closed Ports: {summary['total_closed_ports']:,}")
        lines.append(f"  Filtered Ports: {summary['total_filtered_ports']:,}")
        lines.append(f"  Total Scan Time: {summary['total_scan_time']:.2f} seconds")
        lines.append(f"  Average Time Per Host: {summary['avg_time_per_host']:.2f} seconds")
        lines.append('')

        # Host results
        lines.append('=' * 70)
        lines.append('HOST RESULTS')
        lines.append('=' * 70)
        lines.append('')

        # Get all open ports grouped by host
        open_by_host = scanner.get_all_open_ports()

        for host in sorted(open_by_host.keys()):
            ports = open_by_host[host]

            if ports:
                lines.append(f"Host: {host}")
                lines.append(f"  Status: SCANNED")
                lines.append(f"  Open Ports Found: {len(ports)}")

                # Open port numbers
                port_numbers = sorted([p.port for p in ports])
                lines.append(f"  Ports: {', '.join(map(str, port_numbers))}")
                lines.append('')

                # Detailed port information
                lines.append('  PORT DETAILS:')
                for port_result in sorted(ports, key=lambda p: p.port):
                    service = ServiceDetector.get_service(port_result.port)
                    service_name = service.name.upper() if service else 'UNKNOWN'
                    description = service.description if service else 'Unknown Service'

                    lines.append(f"    • {port_result.port}/tcp: {service_name}")
                    lines.append(f"      └─ {description}")

                lines.append('')
                lines.append('-' * 70)
                lines.append('')
            else:
                lines.append(f"Host: {host}")
                lines.append('  Status: SCANNED')
                lines.append('  Open Ports Found: 0')
                lines.append('')
                lines.append('-' * 70)
                lines.append('')

        # Footer
        lines.append('')
        lines.append('=' * 70)
        lines.append('END OF REPORT')
        lines.append('=' * 70)

        return '\n'.join(lines)

    def export_string(self, scanner: HostScanner) -> str:
        """
        Export scan results as text string (no file).

        Args:
            scanner: HostScanner instance

        Returns:
            Text report as string

        Example:
            exporter = TextExporter()
            report = exporter.export_string(scanner)
            print(report)
        """
        return self._build_text_report(scanner)


def export_to_text(
    scanner: HostScanner,
    output_dir: str = 'reports',
    filename: str = None
) -> str:
    """
    Convenience function to export scan results to text.

    Args:
        scanner: HostScanner instance
        output_dir: Directory to save file
        filename: Output filename

    Returns:
        Path to exported file

    Example:
        filepath = export_to_text(scanner, 'reports', 'my_scan.txt')
    """
    exporter = TextExporter(output_dir)
    return exporter.export(scanner, filename)
