"""
📋 JSON Exporter - Data Format!

This creates a JSON file (structured data) that:
  ✓ Computers can read and understand
  ✓ Other programs can analyze
  ✓ You can parse with scripts

WHY USE JSON?
  • Structured data (not just text)
  • Easy for scripts/programming to read
  • Good for automation and analysis
  • Industry standard format

The output looks like:
{
    "metadata": {
        "scan_time": "2024-06-23T14:30:45",
        "tool": "PortScanner",
        "version": "1.0.0"
    },
    "scan_summary": {
        "total_hosts": 1,
        "total_ports_scanned": 1000,
        "total_open_ports": 3
    },
    "hosts": {
        "192.168.1.1": {
            "open_ports": [22, 80, 443],
            "services": [...]
        }
    }
}

Good for:
  • Importing into databases
  • Analyzing with Python/JavaScript
  • Creating custom reports
  • Automation scripts
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
from portscanner.scanner.host_scanner import HostScanner


class JSONExporter:
    """Exports scan results to JSON format."""

    def __init__(self, output_dir: str = 'reports'):
        """
        Initialize the JSON exporter.

        Args:
            output_dir: Directory to save JSON files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export(
        self,
        scanner: HostScanner,
        filename: str = None,
        pretty: bool = True
    ) -> str:
        """
        Export scan results to JSON file.

        Args:
            scanner: HostScanner instance with completed scan
            filename: Output filename (default: scan_TIMESTAMP.json)
            pretty: Whether to pretty-print JSON (default: True)

        Returns:
            Path to the exported file

        Example:
            exporter = JSONExporter('reports')
            filepath = exporter.export(scanner, 'results.json')
            print(f"Saved to: {filepath}")
        """
        # Generate filename if not provided
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'scan_{timestamp}.json'

        filepath = self.output_dir / filename

        # Build the export data
        data = self._build_export_data(scanner)

        # Write to file
        with open(filepath, 'w', encoding='utf-8') as f:
            if pretty:
                json.dump(data, f, indent=2, ensure_ascii=False)
            else:
                json.dump(data, f, ensure_ascii=False)

        return str(filepath)

    def _build_export_data(self, scanner: HostScanner) -> Dict[str, Any]:
        """
        Build the complete export data structure.

        Args:
            scanner: HostScanner instance

        Returns:
            Dictionary ready for JSON serialization
        """
        return {
            'metadata': {
                'scan_time': datetime.now().isoformat(),
                'tool': 'PortScanner',
                'version': '1.0.0'
            },
            'scan_summary': scanner.get_summary(),
            'hosts': scanner.export_results()
        }

    def export_string(self, scanner: HostScanner, pretty: bool = True) -> str:
        """
        Export scan results as JSON string (no file).

        Args:
            scanner: HostScanner instance
            pretty: Whether to pretty-print JSON

        Returns:
            JSON string

        Example:
            exporter = JSONExporter()
            json_str = exporter.export_string(scanner)
            print(json_str)
        """
        data = self._build_export_data(scanner)

        if pretty:
            return json.dumps(data, indent=2, ensure_ascii=False)
        else:
            return json.dumps(data, ensure_ascii=False)


def export_to_json(
    scanner: HostScanner,
    output_dir: str = 'reports',
    filename: str = None
) -> str:
    """
    Convenience function to export scan results to JSON.

    Args:
        scanner: HostScanner instance
        output_dir: Directory to save file
        filename: Output filename

    Returns:
        Path to exported file

    Example:
        filepath = export_to_json(scanner, 'reports', 'my_scan.json')
    """
    exporter = JSONExporter(output_dir)
    return exporter.export(scanner, filename)
