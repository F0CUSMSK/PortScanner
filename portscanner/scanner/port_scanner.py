"""
🔌 Core Port Scanning - The Heart of the Tool!

This is where the magic happens! Here's what we do:

1. CREATE A SOCKET
   Think of a socket like a telephone line. We create a line,
   then try to dial each port number.

2. TRY TO CONNECT
   We send a "hello, are you there?" message to each port.
   - If it says "yes!" → PORT IS OPEN ✓
   - If it says "no!" → PORT IS CLOSED ✗
   - If it doesn't answer → PORT IS FILTERED (firewall) 🟡

3. DO IT REALLY FAST
   Instead of checking one port at a time (SLOW),
   we check 50 ports at the SAME TIME using threading!

KEY CONCEPTS YOU'RE LEARNING:
- Sockets: Network connections (like phone lines for computers)
- TCP/IP: The protocol used on the internet
- Ports: Special "doors" on a computer (0-65535 of them!)
- Threading: Doing many things at once (why we're FAST ⚡)
- Timeout: Waiting a maximum time before giving up

REAL EXAMPLE:
Think of scanning a building:
  Building = Computer (IP address)
  Doors = Ports (22, 80, 443, etc.)
  Knocking on doors = Attempting connections
  Answers door = Open port (service listening)
  Doesn't answer = Closed or filtered port
"""

import socket
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum


class PortState(Enum):
    """What does a port look like when we check it?"""
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    FILTERED = "FILTERED"


@dataclass
class ScanResult:
    """Result from checking ONE port.
    
    Think of this as a receipt from one knock on a door:
      - host: Which computer?
      - port: Which door?
      - state: Did it answer? (OPEN/CLOSED/FILTERED)
      - protocol: How did we knock? (tcp, udp)
      - banner: What did the door say back? (optional service info)
      - response_time: How long did it take to answer?
    """
    host: str
    port: int
    state: PortState
    protocol: str = "tcp"
    banner: str = ""
    response_time: float = 0.0

    def __repr__(self) -> str:
        """String representation of scan result."""
        banner_info = f" ({self.banner})" if self.banner else ""
        return f"Port {self.port}/{self.protocol.upper()}: {self.state.value}{banner_info}"


class PortScanner:
    """
    Low-level port scanner using TCP sockets.

    This is the core scanning engine. It attempts to establish TCP connections
    to individual ports and detects their state based on the response.
    """

    def __init__(
        self,
        host: str,
        timeout: float = 2.0,
        banner_grab: bool = False,
        max_workers: int = 50
    ):
        """
        Set up a port scanner for ONE computer.

        Think of this as "preparing your detective equipment before
        you start knocking on doors."

        Args:
            host: The IP address to scan (e.g., "192.168.1.1")
            timeout: How long to wait for an answer before giving up
                    - Fast (1 second): Quick but might miss ports on slow networks
                    - Normal (2 seconds): Good balance
                    - Slow (5 seconds): Patient, catches everything
            banner_grab: Try to read what the service says when it answers
            max_workers: How many "workers" to send at once (default 50)
                        - More = faster but uses more computer power
                        - Less = slower but less demanding

        Example:
            # Create scanner with default settings
            scanner = PortScanner("192.168.1.1")
            
            # Create scanner with fast settings
            fast_scanner = PortScanner("8.8.8.8", timeout=1.0, max_workers=100)
        """
        self.host = host
        self.timeout = timeout
        self.banner_grab = banner_grab
        self.max_workers = max_workers

        # Lock for thread-safe operations
        # (Don't worry about this yet - it's for advanced threading concepts)
        self.lock = threading.Lock()

        # Store results
        self.results: List[ScanResult] = []

    def _attempt_connection(self, port: int) -> Tuple[PortState, float, str]:
        """
        Attempt a TCP connection to a specific port.

        This is the core scanning function. Here's how it works:

        1. Create a socket object
        2. Set a timeout (so we don't wait forever)
        3. Attempt to connect to host:port
        4. If connection succeeds → OPEN
        5. If connection refused → CLOSED
        6. If connection times out → FILTERED

        Args:
            port: Port number to scan (1-65535)

        Returns:
            Tuple of (port_state, response_time, banner)

        Networking Concepts:
            - Socket: Think of it like a telephone jack. You plug in and try to call.
            - TCP: You're trying to establish a 3-way handshake connection.
            - If the port is open, the handshake succeeds.
            - If closed, the host says "no thanks" (RST packet).
            - If filtered, firewall blocks everything (no response).
        """
        start_time = time.time()
        banner = ""

        try:
            # Create a TCP socket
            # socket.AF_INET = IPv4 (not IPv6)
            # socket.SOCK_STREAM = TCP (not UDP)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Set socket timeout (seconds)
            # If the operation takes longer than this, raise socket.timeout
            sock.settimeout(self.timeout)

            # Attempt to establish TCP connection
            # This tries the 3-way handshake: SYN → SYN-ACK → ACK
            # If succeeds, connection is OPEN
            result = sock.connect_ex((self.host, port))

            # socket.connect_ex() returns:
            # 0 = Success (port is OPEN)
            # non-0 = Failure (port is CLOSED or FILTERED)

            if result == 0:
                # Port is OPEN - connection succeeded
                state = PortState.OPEN

                # Try to grab banner (service info)
                if self.banner_grab:
                    try:
                        # Receive up to 1024 bytes of data from the service
                        # Services like SSH, HTTP, FTP send a greeting message
                        banner_data = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                        # Take first 50 chars to avoid spam
                        banner = banner_data[:50]
                    except (socket.timeout, socket.error):
                        # If we can't grab banner, that's OK
                        banner = ""
            else:
                # Connection failed
                # Could be CLOSED or FILTERED
                # We'll assume CLOSED (typical case)
                # In a more advanced scanner, we'd use ICMP to distinguish
                state = PortState.CLOSED

            sock.close()

            response_time = time.time() - start_time
            return state, response_time, banner

        except socket.timeout:
            # Connection timed out
            # This usually means firewall is blocking (FILTERED)
            response_time = time.time() - start_time
            return PortState.FILTERED, response_time, ""

        except socket.error as e:
            # Other socket errors
            response_time = time.time() - start_time
            # Default to CLOSED on error
            return PortState.CLOSED, response_time, ""

        except Exception as e:
            # Unexpected error
            response_time = time.time() - start_time
            return PortState.FILTERED, response_time, ""

    def scan_port(self, port: int) -> ScanResult:
        """
        Scan ONE port and return the result.

        This is a simple wrapper that:
        1. Attempts connection to the port
        2. Records how long it took
        3. Returns the result in a nice container

        Args:
            port: The port number to check (1-65535)

        Returns:
            ScanResult object with all the info about that port

        Example:
            result = scanner.scan_port(22)
            if result.state == PortState.OPEN:
                print(f"SSH is open on port 22!")
        """
        state, response_time, banner = self._attempt_connection(port)
        result = ScanResult(
            host=self.host,
            port=port,
            state=state,
            banner=banner,
            response_time=response_time
        )
        return result

    def scan_ports(
        self,
        ports: List[int],
        callback=None
    ) -> List[ScanResult]:
        """
        Scan multiple ports using parallel threading.

        This is where ThreadPoolExecutor makes the magic happen.
        Instead of scanning ports one-by-one (slow), we scan 50 at a time (fast).

        Threading Explanation:
        - Sequential: port1 (2s) → port2 (2s) → port3 (2s) = 6 seconds
        - Parallel (50 threads): all ports (2s) = 2 seconds
        - That's 3x faster!

        Args:
            ports: List of port numbers to scan
            callback: Optional function to call after each port scan
                     Useful for progress updates
                     callback(result) where result is ScanResult

        Returns:
            List of ScanResult objects for all scanned ports

        Example:
            ports = [22, 80, 443, 3306]
            results = scanner.scan_ports(ports)
            for result in results:
                print(result)

            # With progress callback:
            def on_port_scanned(result):
                print(f"Scanned {result.port}: {result.state.value}")

            results = scanner.scan_ports(ports, callback=on_port_scanned)
        """
        results = []

        # ThreadPoolExecutor manages a pool of worker threads
        # max_workers=50 means up to 50 threads running simultaneously
        # This is a "pool" because threads are reused (not recreated each time)
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all port scans to the thread pool
            # This returns immediately (doesn't wait for completion)
            futures = {
                executor.submit(self.scan_port, port): port
                for port in ports
            }

            # as_completed() yields futures as they complete
            # This lets us process results in the order they finish
            # (not necessarily the order we submitted them)
            for future in as_completed(futures):
                try:
                    result = future.result()  # Get the ScanResult
                    results.append(result)

                    # Call the callback if provided
                    if callback:
                        callback(result)

                except Exception as e:
                    # Handle any exceptions from the scan
                    port = futures[future]
                    print(f"Error scanning port {port}: {e}")

        return results

    def scan_range(
        self,
        start_port: int,
        end_port: int,
        callback=None
    ) -> List[ScanResult]:
        """
        Scan a range of ports.

        Args:
            start_port: Starting port number (inclusive)
            end_port: Ending port number (inclusive)
            callback: Optional callback function

        Returns:
            List of ScanResult objects

        Example:
            # Scan ports 1-1000
            results = scanner.scan_range(1, 1000)

            # Scan with callback for progress
            results = scanner.scan_range(22, 65535, callback=on_port_scanned)
        """
        ports = list(range(start_port, end_port + 1))
        return self.scan_ports(ports, callback=callback)

    def get_open_ports(self) -> List[ScanResult]:
        """
        Get only the OPEN ports from results.

        Returns:
            List of ScanResult objects where state is OPEN

        Example:
            scanner.scan_range(1, 1000)
            open_ports = scanner.get_open_ports()
            for port in open_ports:
                print(f"Port {port.port}: {port.state.value}")
        """
        return [r for r in self.results if r.state == PortState.OPEN]

    def get_closed_ports(self) -> List[ScanResult]:
        """Get only the CLOSED ports from results."""
        return [r for r in self.results if r.state == PortState.CLOSED]

    def get_filtered_ports(self) -> List[ScanResult]:
        """Get only the FILTERED ports from results."""
        return [r for r in self.results if r.state == PortState.FILTERED]

    def get_summary(self) -> Dict:
        """
        Get a summary of scan results.

        Returns:
            Dictionary with summary statistics

        Example:
            summary = scanner.get_summary()
            print(f"Open ports: {summary['open_count']}")
            print(f"Closed ports: {summary['closed_count']}")
        """
        return {
            'host': self.host,
            'total_scanned': len(self.results),
            'open_count': len(self.get_open_ports()),
            'closed_count': len(self.get_closed_ports()),
            'filtered_count': len(self.get_filtered_ports()),
            'avg_response_time': (
                sum(r.response_time for r in self.results) / len(self.results)
                if self.results else 0
            )
        }


class PortScannerFactory:
    """
    Factory for creating preconfigured port scanners.

    Provides convenient preset configurations for common scanning scenarios.
    """

    @staticmethod
    def create_fast_scanner(host: str) -> PortScanner:
        """
        Create a fast but potentially less reliable scanner.

        Uses:
        - Low timeout (1.0 seconds)
        - More threads (100)

        Good for: Local networks, fast targets
        Bad for: Remote targets, slow networks
        """
        return PortScanner(host, timeout=1.0, max_workers=100)

    @staticmethod
    def create_balanced_scanner(host: str) -> PortScanner:
        """
        Create a balanced scanner (recommended).

        Uses:
        - Medium timeout (2.0 seconds)
        - Medium threads (50)

        Good for: General purpose scanning
        """
        return PortScanner(host, timeout=2.0, max_workers=50)

    @staticmethod
    def create_thorough_scanner(host: str) -> PortScanner:
        """
        Create a thorough but slow scanner.

        Uses:
        - High timeout (5.0 seconds)
        - Fewer threads (20)
        - Banner grabbing enabled

        Good for: Remote targets, unreliable networks
        Bad for: Speed
        """
        return PortScanner(host, timeout=5.0, max_workers=20, banner_grab=True)
