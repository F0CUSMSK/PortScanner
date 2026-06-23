"""
🌐 HTML Exporter - Beautiful Reports!

This module creates a fancy HTML report that you can:
  ✓ Open in your web browser
  ✓ Share with others
  ✓ Print to PDF
  ✓ View on phone or tablet

WHY USE HTML?
  • Beautiful visual presentation
  • Professional looking (great for reports)
  • No special software needed (just a browser)
  • Easy to share

The report includes:
  📊 Summary statistics (how many ports open, etc)
  📈 Charts showing port distribution
  🎨 Color-coded results (green = open, red = closed)
  📱 Works on phones and tablets
  🖨️  Looks great when printed

All the styling is built-in - NO extra files needed!
"""

from datetime import datetime
from pathlib import Path
from portscanner.scanner.host_scanner import HostScanner
from portscanner.scanner.service_detector import ServiceDetector


class HTMLExporter:
    """Create a pretty HTML report from scan results."""

    def __init__(self, output_dir: str = 'reports'):
        """
        Set up to create HTML reports.

        Args:
            output_dir: Where to save the HTML files (usually 'reports')
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export(
        self,
        scanner: HostScanner,
        filename: str = None
    ) -> str:
        """
        Export scan results to HTML file.

        Args:
            scanner: HostScanner instance with completed scan
            filename: Output filename (default: scan_TIMESTAMP.html)

        Returns:
            Path to the exported file

        Example:
            exporter = HTMLExporter('reports')
            filepath = exporter.export(scanner, 'results.html')
        """
        # Generate filename if not provided
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'scan_{timestamp}.html'

        filepath = self.output_dir / filename

        # Build HTML content
        html_content = self._build_html_report(scanner)

        # Write to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)

        return str(filepath)

    def _build_html_report(self, scanner: HostScanner) -> str:
        """
        Build the complete HTML report.

        Args:
            scanner: HostScanner instance

        Returns:
            Complete HTML document as string
        """
        summary = scanner.get_summary()
        open_by_host = scanner.get_all_open_ports()

        # Calculate statistics for visualization
        open_count = summary['total_open_ports']
        closed_count = summary['total_closed_ports']
        filtered_count = summary['total_filtered_ports']
        total = open_count + closed_count + filtered_count

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Port Scanner Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f5f5;
            color: #333;
            line-height: 1.6;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}

        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}

        h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}

        .scan-time {{
            font-size: 0.9em;
            opacity: 0.9;
        }}

        .summary-cards {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}

        .card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 4px solid #667eea;
        }}

        .card.open {{
            border-left-color: #4caf50;
        }}

        .card.closed {{
            border-left-color: #f44336;
        }}

        .card.filtered {{
            border-left-color: #ff9800;
        }}

        .card h3 {{
            color: #666;
            font-size: 0.9em;
            text-transform: uppercase;
            margin-bottom: 10px;
        }}

        .card-value {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}

        .card.open .card-value {{
            color: #4caf50;
        }}

        .card.closed .card-value {{
            color: #f44336;
        }}

        .card.filtered .card-value {{
            color: #ff9800;
        }}

        .chart {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}

        .chart h2 {{
            margin-bottom: 20px;
            color: #333;
        }}

        .progress-bar {{
            height: 30px;
            background: #f0f0f0;
            border-radius: 5px;
            overflow: hidden;
            display: flex;
            margin-bottom: 20px;
        }}

        .progress-segment {{
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 0.9em;
            font-weight: bold;
        }}

        .progress-open {{
            background: #4caf50;
        }}

        .progress-closed {{
            background: #f44336;
        }}

        .progress-filtered {{
            background: #ff9800;
        }}

        .host-section {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}

        .host-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 15px;
            border-bottom: 2px solid #f0f0f0;
            margin-bottom: 15px;
        }}

        .host-name {{
            font-size: 1.3em;
            font-weight: bold;
            color: #333;
        }}

        .port-count {{
            background: #667eea;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
        }}

        .ports-list {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 15px;
        }}

        .port-card {{
            background: #f9f9f9;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #667eea;
        }}

        .port-number {{
            font-size: 1.2em;
            font-weight: bold;
            color: #667eea;
        }}

        .port-service {{
            color: #666;
            margin-top: 5px;
            font-size: 0.95em;
        }}

        .port-description {{
            color: #999;
            margin-top: 5px;
            font-size: 0.9em;
        }}

        .no-ports {{
            color: #999;
            font-style: italic;
            padding: 20px;
            text-align: center;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}

        th {{
            background: #f5f5f5;
            padding: 12px;
            text-align: left;
            font-weight: 600;
            border-bottom: 2px solid #ddd;
        }}

        td {{
            padding: 12px;
            border-bottom: 1px solid #eee;
        }}

        tr:hover {{
            background: #f9f9f9;
        }}

        footer {{
            background: #333;
            color: white;
            text-align: center;
            padding: 20px;
            margin-top: 40px;
            border-radius: 8px;
        }}

        .legend {{
            display: flex;
            gap: 30px;
            justify-content: center;
            margin-top: 20px;
            flex-wrap: wrap;
        }}

        .legend-item {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .legend-box {{
            width: 20px;
            height: 20px;
            border-radius: 3px;
        }}

        @media print {{
            body {{
                background: white;
            }}
            .container {{
                max-width: 100%;
            }}
        }}

        @media (max-width: 768px) {{
            h1 {{
                font-size: 1.8em;
            }}
            .summary-cards {{
                grid-template-columns: 1fr;
            }}
            .ports-list {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🔍 Port Scanner Report</h1>
            <p class="scan-time">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </header>

        <!-- Summary Cards -->
        <div class="summary-cards">
            <div class="card open">
                <h3>Open Ports</h3>
                <div class="card-value">{open_count}</div>
            </div>
            <div class="card closed">
                <h3>Closed Ports</h3>
                <div class="card-value">{closed_count:,}</div>
            </div>
            <div class="card filtered">
                <h3>Filtered Ports</h3>
                <div class="card-value">{filtered_count:,}</div>
            </div>
            <div class="card">
                <h3>Hosts Scanned</h3>
                <div class="card-value">{summary['total_hosts']}</div>
            </div>
            <div class="card">
                <h3>Total Ports Scanned</h3>
                <div class="card-value">{summary['total_ports_scanned']:,}</div>
            </div>
            <div class="card">
                <h3>Scan Duration</h3>
                <div class="card-value">{summary['total_scan_time']:.1f}s</div>
            </div>
        </div>

        <!-- Chart -->
        <div class="chart">
            <h2>Port State Distribution</h2>
            <div class="progress-bar">
"""

        # Build progress bar segments
        if total > 0:
            open_percent = (open_count / total) * 100
            closed_percent = (closed_count / total) * 100
            filtered_percent = (filtered_count / total) * 100

            if open_percent > 0:
                html += f'                <div class="progress-segment progress-open" style="width: {open_percent}%">Open {open_count}</div>\n'
            if closed_percent > 0:
                html += f'                <div class="progress-segment progress-closed" style="width: {closed_percent}%">Closed {closed_count}</div>\n'
            if filtered_percent > 0:
                html += f'                <div class="progress-segment progress-filtered" style="width: {filtered_percent}%">Filtered {filtered_count}</div>\n'

        html += """            </div>
            <div class="legend">
                <div class="legend-item">
                    <div class="legend-box progress-open"></div>
                    <span>Open</span>
                </div>
                <div class="legend-item">
                    <div class="legend-box progress-closed"></div>
                    <span>Closed</span>
                </div>
                <div class="legend-item">
                    <div class="legend-box progress-filtered"></div>
                    <span>Filtered</span>
                </div>
            </div>
        </div>

        <!-- Host Results -->
"""

        # Add host sections
        for host in sorted(open_by_host.keys()):
            ports = open_by_host[host]

            html += f"""        <div class="host-section">
            <div class="host-header">
                <div class="host-name">📍 {host}</div>
                <div class="port-count">{len(ports)} open ports</div>
            </div>
"""

            if ports:
                html += '            <div class="ports-list">\n'
                for port_result in sorted(ports, key=lambda p: p.port):
                    service = ServiceDetector.get_service(port_result.port)
                    service_name = service.name.upper() if service else 'UNKNOWN'
                    description = service.description if service else 'Unknown Service'

                    html += f"""                <div class="port-card">
                    <div class="port-number">:{port_result.port}/tcp</div>
                    <div class="port-service">{service_name}</div>
                    <div class="port-description">{description}</div>
                </div>
"""

                html += '            </div>\n'
            else:
                html += '            <div class="no-ports">No open ports found</div>\n'

            html += '        </div>\n'

        # Footer
        html += f"""        <footer>
            <p>PortScanner Report | Generated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p style="font-size: 0.9em; margin-top: 10px;">Educational Purpose Only</p>
        </footer>
    </div>
</body>
</html>
"""

        return html

    def export_string(self, scanner: HostScanner) -> str:
        """
        Export scan results as HTML string (no file).

        Args:
            scanner: HostScanner instance

        Returns:
            HTML document as string

        Example:
            exporter = HTMLExporter()
            html = exporter.export_string(scanner)
        """
        return self._build_html_report(scanner)


def export_to_html(
    scanner: HostScanner,
    output_dir: str = 'reports',
    filename: str = None
) -> str:
    """
    Convenience function to export scan results to HTML.

    Args:
        scanner: HostScanner instance
        output_dir: Directory to save file
        filename: Output filename

    Returns:
        Path to exported file

    Example:
        filepath = export_to_html(scanner, 'reports', 'my_scan.html')
    """
    exporter = HTMLExporter(output_dir)
    return exporter.export(scanner, filename)
