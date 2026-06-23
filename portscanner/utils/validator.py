

import os
import re
from typing import List, Tuple, Set


class InputValidator:
    """Validates user inputs for the port scanner."""

    # Regular expression pattern for validating IPv4 addresses
    # Matches: 0-255.0-255.0-255.0-255
    IPV4_PATTERN = re.compile(
        r'^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}'
        r'([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$'
    )

    @staticmethod
    def validate_ip_address(ip: str) -> bool:
      
        return bool(InputValidator.IPV4_PATTERN.match(ip.strip()))

    @staticmethod
    def parse_targets(targets_input: str) -> List[str]:
       
        ips = [ip.strip() for ip in targets_input.split(',')]
        invalid_ips = [ip for ip in ips if not InputValidator.validate_ip_address(ip)]

        if invalid_ips:
            raise ValueError(
                f"❌ Some IP addresses don't look right:\n"
                f"   Invalid: {', '.join(invalid_ips)}\n\n"
                f"💡 Tip: IP addresses should have 4 numbers separated by dots,\n"
                f"   like: 192.168.1.1 or 8.8.8.8"
            )

        return ips

    @staticmethod
    def read_targets_from_file(filepath: str) -> List[str]:
        """
        Read IP addresses from a file (one IP per line).

        Args:
            filepath: Path to file containing IP addresses

        Returns:
            List of validated IP addresses

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file is empty or contains invalid IPs

        Example:
            File content (targets.txt):
            192.168.1.1
            192.168.1.2

            >>> InputValidator.read_targets_from_file("targets.txt")
            ['192.168.1.1', '192.168.1.2']
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Target file not found: {filepath}")

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except IOError as e:
            raise IOError(f"Error reading file {filepath}: {e}")

        # Remove empty lines and whitespace
        ips = [line.strip() for line in lines if line.strip() and not line.strip().startswith('#')]

        if not ips:
            raise ValueError(f"No valid IP addresses found in {filepath}")

        # Validate all IPs
        invalid_ips = [ip for ip in ips if not InputValidator.validate_ip_address(ip)]

        if invalid_ips:
            raise ValueError(
                f"Invalid IP addresses in file:\n" +
                "\n".join(f"  • {ip}" for ip in invalid_ips[:5]) +
                (f"\n  ... and {len(invalid_ips) - 5} more" if len(invalid_ips) > 5 else "")
            )

        return ips

    @staticmethod
    def validate_port_range(port_range: str) -> Tuple[int, int]:
        """
        Parse and validate a port range string.

        Args:
            port_range: Port range in format "start-end" (e.g., "1-1000")
                       If None or empty, returns (1, 65535) for full scan

        Returns:
            Tuple of (start_port, end_port)

        Raises:
            ValueError: If format is invalid or ports are out of range

        Example:
            >>> InputValidator.validate_port_range("80-443")
            (80, 443)
            >>> InputValidator.validate_port_range("22")
            ValueError: Port range must be in format "start-end"
        """
        if not port_range or port_range.lower() == "all":
            return (1, 65535)

        try:
            parts = port_range.split('-')
            if len(parts) != 2:
                raise ValueError(
                    f"Invalid port range format: '{port_range}'\n"
                    f"Use format: '1-1000' or '--ports all' for 1-65535"
                )

            start_port = int(parts[0].strip())
            end_port = int(parts[1].strip())

            # Validate port numbers (1-65535 are valid TCP/UDP ports)
            if not (1 <= start_port <= 65535):
                raise ValueError(f"Start port {start_port} out of valid range (1-65535)")

            if not (1 <= end_port <= 65535):
                raise ValueError(f"End port {end_port} out of valid range (1-65535)")

            if start_port > end_port:
                raise ValueError(
                    f"Start port ({start_port}) cannot be greater than end port ({end_port})"
                )

            return (start_port, end_port)

        except ValueError as e:
            raise ValueError(str(e))

    @staticmethod
    def validate_export_formats(formats: str) -> Set[str]:
        """
        Validate export format choices.

        Args:
            formats: Comma-separated export formats or 'all'
                    Valid options: json, txt, html, all

        Returns:
            Set of valid export formats

        Raises:
            ValueError: If invalid format is specified

        Example:
            >>> InputValidator.validate_export_formats("json,txt")
            {'json', 'txt'}
            >>> InputValidator.validate_export_formats("all")
            {'json', 'txt', 'html'}
        """
        valid_formats = {'json', 'txt', 'html'}

        if formats.lower() == 'all':
            return valid_formats

        formats_list = [f.strip().lower() for f in formats.split(',')]
        invalid = [f for f in formats_list if f not in valid_formats]

        if invalid:
            raise ValueError(
                f"Invalid export format(s): {', '.join(invalid)}\n"
                f"Valid options: json, txt, html, all"
            )

        return set(formats_list)

    @staticmethod
    def validate_thread_count(threads: int) -> int:
        """
        Validate and adjust thread count for scanning.

        Args:
            threads: Number of threads requested

        Returns:
            Validated thread count (1-256)

        Raises:
            ValueError: If threads is not a positive integer
        """
        try:
            thread_count = int(threads)

            if thread_count < 1:
                raise ValueError("Thread count must be at least 1")

            if thread_count > 256:
                print(f"⚠️  Warning: Limiting threads to 256 (requested {thread_count})")
                return 256

            return thread_count

        except ValueError as e:
            raise ValueError(f"Invalid thread count: {e}")


def validate_all_inputs(
    targets: str,
    ports: str,
    threads: int,
    export: str,
    target_file: str = None,
    targets_list: List[str] = None
) -> dict:
    """
    Validate all user inputs at once.

    Args:
        targets: Comma-separated IPs or single IP
        ports: Port range in "start-end" format
        threads: Number of threads
        export: Export formats
        target_file: Optional file path for targets
        targets_list: Pre-validated list of targets (from interactive mode)

    Returns:
        Dictionary with validated inputs

    Raises:
        ValueError: If any input is invalid

    Example:
        >>> result = validate_all_inputs(
        ...     targets="192.168.1.1",
        ...     ports="22-443",
        ...     threads=10,
        ...     export="json"
        ... )
        >>> result['targets']
        ['192.168.1.1']
    """
    validator = InputValidator()

    # Validate targets
    if targets_list:
        # Use pre-validated targets from interactive mode
        target_list = targets_list
    elif target_file:
        try:
            target_list = validator.read_targets_from_file(target_file)
        except (FileNotFoundError, ValueError, IOError) as e:
            raise ValueError(f"Target file error: {e}")
    elif targets:
        try:
            target_list = validator.parse_targets(targets)
        except ValueError as e:
            raise ValueError(f"Target error: {e}")
    else:
        raise ValueError("Please provide targets (--target or --file)")

    # Validate ports
    try:
        port_range = validator.validate_port_range(ports)
    except ValueError as e:
        raise ValueError(f"Port error: {e}")

    # Validate threads
    try:
        thread_count = validator.validate_thread_count(threads)
    except ValueError as e:
        raise ValueError(f"Thread error: {e}")

    # Validate export formats
    try:
        export_formats = validator.validate_export_formats(export)
    except ValueError as e:
        raise ValueError(f"Export error: {e}")

    return {
        'targets': target_list,
        'port_range': port_range,
        'threads': thread_count,
        'export_formats': export_formats
    }
