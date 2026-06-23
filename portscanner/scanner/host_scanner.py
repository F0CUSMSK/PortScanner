

import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Tuple
from dataclasses import dataclass, field

from portscanner.scanner.port_scanner import PortScanner, PortState, ScanResult
from portscanner.scanner.service_detector import ServiceDetector
from portscanner.utils.logger import Logger


@dataclass
class HostScanResult:
    """
    Results from scanning ONE computer.
    
    Think of this as a "report card" for one computer:
      - host: Which computer?
      - port_results: What ports did we check?
      - scan_time: How long did it take?
      - total_ports: How many ports did we check?
    """
    host: str
    port_results: List[ScanResult] = field(default_factory=list)
    scan_time: float = 0.0
    total_ports: int = 0

    def get_open_ports(self) -> List[ScanResult]:
        """Get all the open ports (services that answered!)."""
        return [r for r in self.port_results if r.state == PortState.OPEN]

    def get_closed_ports(self) -> List[ScanResult]:
        """Get all the closed ports (nothing listening)."""
        return [r for r in self.port_results if r.state == PortState.CLOSED]

    def get_filtered_ports(self) -> List[ScanResult]:
        """Get all the filtered ports (firewall blocked them)."""
        return [r for r in self.port_results if r.state == PortState.FILTERED]

    def get_summary(self) -> Dict:
        """Get a quick summary of this computer's scan."""
        return {
            'host': self.host,
            'total_ports': self.total_ports,
            'open_count': len(self.get_open_ports()),
            'closed_count': len(self.get_closed_ports()),
            'filtered_count': len(self.get_filtered_ports()),
            'scan_time': self.scan_time
        }


class HostScanner:
    """
    Orchestrates scanning of multiple hosts.

    This is the main coordinator that:
    1. Takes a list of target hosts
    2. Creates a PortScanner for each host
    3. Scans ports in parallel (multiple hosts simultaneously)
    4. Enriches results with service detection
    5. Logs progress and results
    """

    def __init__(
        self,
        hosts: List[str],
        port_range: Tuple[int, int] = (1, 65535),
        threads_per_host: int = 50,
        hosts_parallel: int = 5,
        logger: Logger = None,
        timeout: float = 2.0
    ):
        """
        Initialize the host scanner.

        Args:
            hosts: List of IP addresses to scan
            port_range: Tuple of (start_port, end_port)
            threads_per_host: Threads for scanning ports on ONE host (default 50)
            hosts_parallel: Number of hosts to scan in parallel (default 5)
            logger: Logger instance (optional)
            timeout: Socket timeout in seconds

        Example:
            hosts = ["192.168.1.1", "192.168.1.2", "192.168.1.3"]
            scanner = HostScanner(hosts, port_range=(1, 1000))
            results = scanner.scan_all()

        Threading Architecture:

        The scanner uses TWO levels of threading:

        Level 1: Host-level parallelism (threads_parallel = 5)
            ┌─────────────────────────────────┐
            │ Scanning Host 1 (ports 1-1000)  │
            │ Scanning Host 2 (ports 1-1000)  │
            │ Scanning Host 3 (ports 1-1000)  │
            │ Scanning Host 4 (ports 1-1000)  │
            │ Scanning Host 5 (ports 1-1000)  │
            └─────────────────────────────────┘

        Level 2: Port-level parallelism (threads_per_host = 50)
            Within each host scan:
            ┌──────────────────────────────────┐
            │ Host 1 - Scan 50 ports at once   │
            │ (Then scan next 50, etc)         │
            └──────────────────────────────────┘

        This 2-tier approach balances speed and resource usage.
        """
        self.hosts = hosts
        self.port_range = port_range
        self.threads_per_host = threads_per_host
        self.hosts_parallel = hosts_parallel
        self.logger = logger
        self.timeout = timeout

        # Results storage
        self.results: Dict[str, HostScanResult] = {}
        self.lock = threading.Lock()

    def scan_single_host(self, host: str) -> HostScanResult:
        """
        Scan a single host.

        This method:
        1. Creates a PortScanner for the host
        2. Scans all specified ports
        3. Detects services for open ports
        4. Returns organized results

        Args:
            host: IP address to scan

        Returns:
            HostScanResult with port information

        Example:
            result = scanner.scan_single_host("192.168.1.1")
            print(f"Found {len(result.get_open_ports())} open ports")
        """
        if self.logger:
            self.logger.header(f"Scanning Host: {host}")

        # Create a port scanner for this host
        port_scanner = PortScanner(
            host=host,
            timeout=self.timeout,
            banner_grab=False,
            max_workers=self.threads_per_host
        )

        # Define a callback for progress updates
        scanned_count = [0]  # Use list so closure can modify it
        total_ports = self.port_range[1] - self.port_range[0] + 1

        def on_port_scanned(result: ScanResult):
            """Callback when a port scan completes."""
            scanned_count[0] += 1

            # Log progress
            if self.logger:
                self.logger.progress(scanned_count[0], total_ports, host)

            # Log result if port is OPEN
            if result.state == PortState.OPEN:
                service_name = ServiceDetector.get_service_name(result.port)
                if self.logger:
                    self.logger.port_result(
                        result.port,
                        result.protocol,
                        result.state.value,
                        service_name
                    )

        # Scan the port range
        import time
        start_time = time.time()

        port_results = port_scanner.scan_range(
            self.port_range[0],
            self.port_range[1],
            callback=on_port_scanned
        )

        elapsed = time.time() - start_time

        # Clear the progress line
        if self.logger:
            print()  # New line after progress bar

        # Create result object
        result = HostScanResult(
            host=host,
            port_results=port_results,
            scan_time=elapsed,
            total_ports=len(port_results)
        )

        # Log summary for this host
        if self.logger:
            summary = result.get_summary()
            self.logger.success(
                f"Host {host} scan complete: "
                f"{summary['open_count']} open, "
                f"{summary['closed_count']} closed, "
                f"{summary['filtered_count']} filtered "
                f"({summary['scan_time']:.2f}s)"
            )

        return result

    def scan_all(self) -> Dict[str, HostScanResult]:
        """
        Scan all hosts in parallel.

        This scans multiple hosts simultaneously (up to hosts_parallel at once).

        Returns:
            Dictionary mapping host → HostScanResult

        Example:
            results = scanner.scan_all()
            for host, host_result in results.items():
                print(f"{host}: {len(host_result.get_open_ports())} open ports")
        """
        if self.logger:
            self.logger.header(
                f"Starting Multi-Host Scan: {len(self.hosts)} targets"
            )

        # Use ThreadPoolExecutor to scan multiple hosts in parallel
        with ThreadPoolExecutor(max_workers=self.hosts_parallel) as executor:
            # Submit all host scans
            futures = {
                executor.submit(self.scan_single_host, host): host
                for host in self.hosts
            }

            # Collect results as they complete
            for future in as_completed(futures):
                try:
                    host = futures[future]
                    result = future.result()

                    # Store with thread safety
                    with self.lock:
                        self.results[host] = result

                except Exception as e:
                    host = futures[future]
                    if self.logger:
                        self.logger.error(f"Error scanning {host}: {e}")
                    else:
                        print(f"Error scanning {host}: {e}")

        return self.results

    def get_all_open_ports(self) -> Dict[str, List[ScanResult]]:
        """
        Get all open ports across all hosts.

        Returns:
            Dictionary mapping host → list of open ScanResult objects

        Example:
            open_ports = scanner.get_all_open_ports()
            for host, ports in open_ports.items():
                print(f"{host}: {len(ports)} open ports")
                for port in ports:
                    service = ServiceDetector.get_service_name(port.port)
                    print(f"  - {port.port}: {service}")
        """
        return {
            host: result.get_open_ports()
            for host, result in self.results.items()
        }

    def get_summary(self) -> Dict:
        """
        Get overall scan summary.

        Returns:
            Dictionary with aggregate statistics

        Example:
            summary = scanner.get_summary()
            print(f"Total hosts: {summary['total_hosts']}")
            print(f"Total open ports: {summary['total_open_ports']}")
        """
        total_open = sum(len(r.get_open_ports()) for r in self.results.values())
        total_closed = sum(len(r.get_closed_ports()) for r in self.results.values())
        total_filtered = sum(len(r.get_filtered_ports()) for r in self.results.values())
        total_time = sum(r.scan_time for r in self.results.values())

        return {
            'total_hosts': len(self.results),
            'total_ports_scanned': sum(r.total_ports for r in self.results.values()),
            'total_open_ports': total_open,
            'total_closed_ports': total_closed,
            'total_filtered_ports': total_filtered,
            'total_scan_time': total_time,
            'avg_time_per_host': total_time / len(self.results) if self.results else 0
        }

    def print_results(self):
        """
        Print formatted results for all hosts.

        Example:
            scanner.scan_all()
            scanner.print_results()
        """
        if not self.results:
            print("No scan results available")
            return

        if self.logger:
            self.logger.header("SCAN RESULTS")

        # Print results for each host
        for host, result in sorted(self.results.items()):
            open_ports = result.get_open_ports()

            if open_ports:
                if self.logger:
                    print(f"\n{host}:")
                    data = []
                    for port_result in sorted(open_ports, key=lambda x: x.port):
                        service = ServiceDetector.get_service_name(port_result.port)
                        data.append([
                            str(port_result.port),
                            port_result.protocol.upper(),
                            port_result.state.value,
                            service
                        ])
                    self.logger.print_table(
                        data,
                        ['Port', 'Protocol', 'State', 'Service']
                    )
                else:
                    print(f"\n{host}:")
                    for port_result in sorted(open_ports, key=lambda x: x.port):
                        service = ServiceDetector.get_service_name(port_result.port)
                        print(f"  {port_result.port}/tcp: {service}")
            else:
                if self.logger:
                    self.logger.warning(f"{host}: No open ports found")
                else:
                    print(f"{host}: No open ports found")

    def export_results(self) -> Dict:
        """
        Export results in a structured format.

        Used by exporters to save results to files.

        Returns:
            Dictionary suitable for JSON/CSV export

        Example:
            data = scanner.export_results()
            # {
            #     '192.168.1.1': {
            #         'open_ports': [22, 80, 443],
            #         'services': {...}
            #     },
            #     ...
            # }
        """
        export_data = {}

        for host, result in self.results.items():
            open_ports = result.get_open_ports()
            open_port_list = []

            for port_result in open_ports:
                service_info = ServiceDetector.get_service(port_result.port)
                open_port_list.append({
                    'port': port_result.port,
                    'protocol': port_result.protocol,
                    'service': service_info.name if service_info else 'Unknown',
                    'description': service_info.description if service_info else 'Unknown'
                })

            export_data[host] = {
                'open_ports': sorted([p['port'] for p in open_port_list]),
                'services': open_port_list,
                'summary': result.get_summary()
            }

        return export_data


# Convenience functions
def quick_scan(hosts: List[str], port_range: Tuple[int, int] = (1, 1000)):
    """
    Quick scan of hosts without logging.

    Args:
        hosts: List of IP addresses
        port_range: Port range to scan

    Returns:
        Dictionary of HostScanResult objects

    Example:
        results = quick_scan(["192.168.1.1"], (1, 1000))
        for host, result in results.items():
            print(f"Open ports on {host}: {[p.port for p in result.get_open_ports()]}")
    """
    scanner = HostScanner(hosts, port_range=port_range)
    return scanner.scan_all()
