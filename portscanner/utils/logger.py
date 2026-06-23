
import os
import sys
from datetime import datetime
from typing import Optional


class Colors:
    """ANSI color codes for terminal output."""

    # Reset color
    RESET = '\033[0m'

    # Foreground colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

    # Bright colors
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_CYAN = '\033[96m'

    # Styles
    BOLD = '\033[1m'
    DIM = '\033[2m'

    @staticmethod
    def disable():
        """Disable colors (useful for piping to files)."""
        for attr in dir(Colors):
            if not attr.startswith('_'):
                setattr(Colors, attr, '')


class Logger:
    """Professional logging system for port scanner."""

    def __init__(self, log_dir: str = 'reports', log_file: str = 'scanner.log'):
        """
        Initialize the logger.

        Args:
            log_dir: Directory to store log files
            log_file: Filename for the log file

        Example:
            logger = Logger('reports', 'scan_2024.log')
        """
        self.log_dir = log_dir
        self.log_file = os.path.join(log_dir, log_file)
        self.start_time = datetime.now()

        # Create log directory if it doesn't exist
        if not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

        # Initialize log file with header
        self._write_to_file(f"\n{'='*70}")
        self._write_to_file(f"SCAN STARTED: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        self._write_to_file(f"{'='*70}\n")

    def _write_to_file(self, message: str) -> None:
        """
        Write message to log file.

        Args:
            message: Message to log
        """
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(message + '\n')
        except IOError as e:
            print(f"Error writing to log file: {e}")

    def _strip_ansi(self, text: str) -> str:
        """
        Remove ANSI color codes from text.

        Args:
            text: Text with potential ANSI codes

        Returns:
            Plain text without colors

        Example:
            >>> logger._strip_ansi(f"{Colors.RED}Error{Colors.RESET}")
            'Error'
        """
        import re
        ansi_pattern = re.compile(r'\033\[[0-9;]*m')
        return ansi_pattern.sub('', text)

    def info(self, message: str) -> None:
        """
        Log info message (blue).

        Args:
            message: Message to log

        Example:
            logger.info("Starting scan...")
        """
        colored = f"{Colors.BLUE}ℹ{Colors.RESET} {message}"
        print(colored)
        self._write_to_file(f"[INFO] {self._strip_ansi(message)}")

    def success(self, message: str) -> None:
        """
        Log success message (green).

        Args:
            message: Message to log

        Example:
            logger.success("Scan completed!")
        """
        colored = f"{Colors.BRIGHT_GREEN}✓{Colors.RESET} {message}"
        print(colored)
        self._write_to_file(f"[SUCCESS] {self._strip_ansi(message)}")

    def warning(self, message: str) -> None:
        """
        Log warning message (yellow).

        Args:
            message: Message to log

        Example:
            logger.warning("High CPU usage detected")
        """
        colored = f"{Colors.BRIGHT_YELLOW}⚠{Colors.RESET} {message}"
        print(colored)
        self._write_to_file(f"[WARNING] {self._strip_ansi(message)}")

    def error(self, message: str) -> None:
        """
        Log error message (red).

        Args:
            message: Message to log

        Example:
            logger.error("Invalid IP address")
        """
        colored = f"{Colors.BRIGHT_RED}✗{Colors.RESET} {message}"
        print(colored, file=sys.stderr)
        self._write_to_file(f"[ERROR] {self._strip_ansi(message)}")

    def debug(self, message: str) -> None:
        """
        Log debug message (dim gray).

        Args:
            message: Message to log

        Example:
            logger.debug("Thread 5 started")
        """
        colored = f"{Colors.DIM}[DEBUG]{Colors.RESET} {message}"
        print(colored)
        self._write_to_file(f"[DEBUG] {self._strip_ansi(message)}")

    def header(self, title: str) -> None:
        """
        Print a fancy section header.

        Great for separating different parts of the scan output.

        Args:
            title: What to say in the header

        Example:
            logger.header("Scanning Host 192.168.1.1")
            # Prints a nice box with that title
        """
        width = 70
        line = f"{Colors.CYAN}{'='*width}{Colors.RESET}"
        title_line = f"{Colors.CYAN}{Colors.BOLD}=== {title} ==={Colors.RESET}".ljust(width)

        print()
        print(line)
        print(title_line)
        print(line)
        print()

        self._write_to_file(f"\n{'='*width}")
        self._write_to_file(f"=== {title} ===")
        self._write_to_file(f"{'='*width}\n")

    def port_result(self, port: int, protocol: str, state: str, service: str = '') -> None:
        """
        Log a port scanning result in formatted style.

        Args:
            port: Port number
            protocol: Protocol (tcp/udp)
            state: State (OPEN, CLOSED, FILTERED)
            service: Service name (optional)

        Example:
            logger.port_result(22, 'tcp', 'OPEN', 'SSH')
            # Output: [+] 22/tcp OPEN  → SSH
        """
        if state.upper() == 'OPEN':
            symbol = f"{Colors.BRIGHT_GREEN}[+]{Colors.RESET}"
            state_colored = f"{Colors.BRIGHT_GREEN}{state}{Colors.RESET}"
        elif state.upper() == 'CLOSED':
            symbol = f"{Colors.BRIGHT_RED}[-]{Colors.RESET}"
            state_colored = f"{Colors.BRIGHT_RED}{state}{Colors.RESET}"
        else:  # FILTERED
            symbol = f"{Colors.BRIGHT_YELLOW}[?]{Colors.RESET}"
            state_colored = f"{Colors.BRIGHT_YELLOW}{state}{Colors.RESET}"

        service_info = f" → {Colors.CYAN}{service}{Colors.RESET}" if service else ""
        message = f"{symbol} {port}/{protocol.upper()} {state_colored}{service_info}"

        print(message)
        self._write_to_file(
            f"[RESULT] {port}/{protocol.upper()} {state.upper()}{f' → {service}' if service else ''}"
        )

    def progress(self, current: int, total: int, host: str = '') -> None:
        """
        Display scan progress.

        Args:
            current: Current item number
            total: Total items
            host: Optional host being scanned

        Example:
            logger.progress(50, 100, "192.168.1.1")
            # Output: [50/100] Scanning 192.168.1.1
        """
        percentage = int((current / total) * 100) if total > 0 else 0
        bar_length = 30
        filled = int((percentage / 100) * bar_length)
        bar = '█' * filled + '░' * (bar_length - filled)

        progress_text = f"[{current:5d}/{total}] {percentage:3d}% {bar}"
        if host:
            progress_text += f" {Colors.DIM}{host}{Colors.RESET}"

        print(f"\r{progress_text}", end='', flush=True)

    def print_table(self, data: list, headers: list) -> None:
        """
        Print a formatted table.

        Args:
            data: List of rows, each row is a list of values
            headers: Column headers

        Example:
            logger.print_table(
                [['22', 'SSH', 'OPEN'], ['80', 'HTTP', 'OPEN']],
                ['Port', 'Service', 'State']
            )
        """
        if not data:
            print("No data to display")
            return

        # Calculate column widths
        col_widths = [len(str(h)) for h in headers]
        for row in data:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))

        # Print header
        header_row = " | ".join(
            f"{Colors.BOLD}{h:<{col_widths[i]}}{Colors.RESET}"
            for i, h in enumerate(headers)
        )
        print(header_row)
        print("-" * (sum(col_widths) + len(headers) * 3 - 1))

        # Print rows
        for row in data:
            row_str = " | ".join(
                f"{str(cell):<{col_widths[i]}}"
                for i, cell in enumerate(row)
            )
            print(row_str)

    def scan_summary(self, total_hosts: int, total_ports: int, elapsed_time: float) -> None:
        """
        Print a nice summary at the end of the scan.

        Shows you:
          • How many computers were scanned
          • How many ports were checked
          • How long it took

        Args:
            total_hosts: Number of computers scanned
            total_ports: Number of ports checked
            elapsed_time: How many seconds the scan took

        Example:
            logger.scan_summary(10, 5000, 45.3)
            # Shows a beautiful summary box
        """
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)

        summary = f"""
{Colors.CYAN}{Colors.BOLD}═══════════════════════════════════════{Colors.RESET}
{Colors.BRIGHT_GREEN}✓ SCAN FINISHED - Great Job!{Colors.RESET}
{Colors.CYAN}{Colors.BOLD}═══════════════════════════════════════{Colors.RESET}
  🎯 Computers Scanned:  {Colors.BRIGHT_CYAN}{total_hosts}{Colors.RESET}
  🔍 Ports Checked:      {Colors.BRIGHT_CYAN}{total_ports:,}{Colors.RESET}
  ⏱️  Time Taken:         {Colors.BRIGHT_CYAN}{minutes}m {seconds}s{Colors.RESET}
{Colors.CYAN}{Colors.BOLD}═══════════════════════════════════════{Colors.RESET}
"""
        print(summary)
        self._write_to_file(f"\n[SUMMARY]")
        self._write_to_file(f"Hosts Scanned: {total_hosts}")
        self._write_to_file(f"Ports Checked: {total_ports:,}")
        self._write_to_file(f"Time Elapsed: {minutes}m {seconds}s")
        self._write_to_file(f"Log file saved: {self.log_file}")

    def get_elapsed_time(self) -> float:
        """
        Get elapsed time since logger initialization.

        Returns:
            Elapsed time in seconds

        Example:
            elapsed = logger.get_elapsed_time()
            print(f"Scanned in {elapsed:.2f} seconds")
        """
        return (datetime.now() - self.start_time).total_seconds()

    def finalize(self) -> str:
        """
        Finalize logging and return log file path.

        Returns:
            Path to the log file

        Example:
            log_path = logger.finalize()
            print(f"Full log saved to: {log_path}")
        """
        end_time = datetime.now()
        elapsed = (end_time - self.start_time).total_seconds()

        footer = f"""
{'-'*70}
SCAN FINISHED: {end_time.strftime('%Y-%m-%d %H:%M:%S')}
TOTAL TIME: {int(elapsed // 60)}m {int(elapsed % 60)}s
{'-'*70}
"""
        self._write_to_file(footer)
        return self.log_file


# Singleton logger instance (optional, for convenience)
_logger_instance: Optional[Logger] = None


def get_logger(log_dir: str = 'reports', log_file: str = 'scanner.log') -> Logger:
    """
    Get or create a logger instance (singleton pattern).

    Args:
        log_dir: Directory for logs
        log_file: Log filename

    Returns:
        Logger instance

    Example:
        logger = get_logger()
        logger.info("Starting scan")
    """
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = Logger(log_dir, log_file)
    return _logger_instance
