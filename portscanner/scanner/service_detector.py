

from typing import Dict, Optional, List
from dataclasses import dataclass


@dataclass
class Service:
    """
    Information about a service.
    
    Think of this as a "business card" for a service:
      - port: Door number (1-65535)
      - name: Short name (ssh, http, mysql)
      - protocol: How it talks (tcp, udp)
      - description: What it does in plain English
      - common: Is this a port we see a lot?
    """
    port: int
    name: str
    protocol: str  # tcp, udp, or both
    description: str
    common: bool = False  # Is this a commonly-used port?


class ServiceDetector:
    """
    Find out what service is probably running on a port.

    This uses the official IANA (Internet Assigned Numbers Authority)
    port assignments. It's like a phonebook for ports!
    
    Examples:
        detector = ServiceDetector()
        ssh_service = detector.get_service(22)
        print(ssh_service.description)  # "Secure Shell (SSH)"
    """

    # Comprehensive port-to-service mapping
    # Based on IANA Service Name and Transport Protocol Port Number Registry
    PORT_SERVICES: Dict[int, Service] = {
        # Well-known ports (1-1023) - System services like SSH, HTTP
        1: Service(1, "tcpmux", "tcp", "TCP Port Service Multiplexer", False),
        7: Service(7, "echo", "tcp/udp", "Echo Protocol", False),
        13: Service(13, "daytime", "tcp/udp", "Daytime Protocol", False),
        15: Service(15, "netstat", "tcp", "Netstat", False),
        17: Service(17, "qotd", "tcp/udp", "Quote of the Day", False),
        19: Service(19, "chargen", "tcp/udp", "Character Generator", False),
        20: Service(20, "ftp-data", "tcp", "FTP Data Transfer", True),
        21: Service(21, "ftp", "tcp", "File Transfer Protocol (FTP)", True),
        22: Service(22, "ssh", "tcp", "Secure Shell (SSH)", True),
        23: Service(23, "telnet", "tcp", "Telnet", True),
        25: Service(25, "smtp", "tcp", "Simple Mail Transfer Protocol (SMTP)", True),
        37: Service(37, "time", "tcp/udp", "Time Protocol", False),
        42: Service(42, "name", "tcp/udp", "Name Server", False),
        43: Service(43, "whois", "tcp", "WHOIS", False),
        49: Service(49, "tacacs", "tcp/udp", "TACACS", False),
        50: Service(50, "re-mail-ck", "tcp", "Remote Mail Check", False),
        53: Service(53, "dns", "tcp/udp", "Domain Name System (DNS)", True),
        69: Service(69, "tftp", "udp", "Trivial File Transfer Protocol (TFTP)", True),
        70: Service(70, "gopher", "tcp", "Gopher", False),
        79: Service(79, "finger", "tcp", "Finger", False),
        80: Service(80, "http", "tcp", "HyperText Transfer Protocol (HTTP)", True),
        88: Service(88, "kerberos", "tcp/udp", "Kerberos Authentication", True),
        110: Service(110, "pop3", "tcp", "Post Office Protocol v3 (POP3)", True),
        123: Service(123, "ntp", "udp", "Network Time Protocol (NTP)", True),
        135: Service(135, "epmap", "tcp/udp", "RPC Endpoint Mapper", True),
        139: Service(139, "netbios-ssn", "tcp", "NetBIOS Session Service", True),
        143: Service(143, "imap", "tcp", "Internet Message Access Protocol (IMAP)", True),
        161: Service(161, "snmp", "udp", "Simple Network Management Protocol (SNMP)", True),
        162: Service(162, "snmptrap", "udp", "SNMP Trap", True),
        179: Service(179, "bgp", "tcp", "Border Gateway Protocol (BGP)", True),
        194: Service(194, "irc", "tcp", "Internet Relay Chat (IRC)", False),
        389: Service(389, "ldap", "tcp/udp", "Lightweight Directory Access Protocol (LDAP)", True),
        427: Service(427, "afp", "tcp/udp", "Service Location Protocol", False),
        443: Service(443, "https", "tcp", "HTTP Secure (HTTPS)", True),
        445: Service(445, "microsoft-ds", "tcp", "Microsoft-DS (SMB/CIFS)", True),
        465: Service(465, "smtps", "tcp", "SMTP Secure", True),
        512: Service(512, "exec", "tcp", "Remote Process Execution", False),
        513: Service(513, "login", "tcp", "Remote Login", False),
        514: Service(514, "shell", "tcp", "Remote Shell (rsh)", False),
        514: Service(514, "syslog", "udp", "System Logging", False),
        587: Service(587, "submission", "tcp", "SMTP Submission", True),
        636: Service(636, "ldaps", "tcp", "LDAP Secure", True),
        749: Service(749, "kerberos-adm", "tcp/udp", "Kerberos Administration", False),
        853: Service(853, "dns-over-tls", "tcp/udp", "DNS over TLS (DoT)", True),
        873: Service(873, "rsync", "tcp", "Rsync File Synchronization", False),
        902: Service(902, "iss-realsec", "tcp/udp", "ISS RealSec", False),
        912: Service(912, "apex", "tcp", "Apex Protocol", False),
        953: Service(953, "rndc", "tcp/udp", "RNDC (Named Control)", True),
        989: Service(989, "ftps-data", "tcp", "FTP over SSL Data", True),
        990: Service(990, "ftps", "tcp", "FTP over SSL Control", True),
        993: Service(993, "imaps", "tcp", "IMAP Secure", True),
        995: Service(995, "pop3s", "tcp", "POP3 Secure", True),

        # Registered ports (1024-49151)
        1025: Service(1025, "blackjack", "tcp", "Blackjack", False),
        1433: Service(1433, "ms-sql-s", "tcp", "Microsoft SQL Server", True),
        1521: Service(1521, "oracle", "tcp", "Oracle Database", True),
        1723: Service(1723, "pptp", "tcp", "Point-to-Point Tunneling Protocol", True),
        1900: Service(1900, "upnp", "udp", "Universal Plug and Play (UPnP)", False),
        2049: Service(2049, "nfs", "tcp/udp", "Network File System (NFS)", True),
        3000: Service(3000, "http-alt", "tcp", "HTTP Alternative / Development", False),
        3306: Service(3306, "mysql", "tcp", "MySQL Database", True),
        3389: Service(3389, "rdp", "tcp", "Remote Desktop Protocol (RDP)", True),
        5432: Service(5432, "postgresql", "tcp", "PostgreSQL Database", True),
        5500: Service(5500, "hotline", "tcp", "Hotline", False),
        5631: Service(5631, "pcanywheredata", "tcp", "pcAnywhere Data", False),
        5632: Service(5632, "pcanywherestat", "tcp", "pcAnywhere Status", False),
        5672: Service(5672, "amqp", "tcp", "Advanced Message Queuing Protocol", True),
        5900: Service(5900, "vnc", "tcp", "Virtual Network Computing (VNC)", True),
        6000: Service(6000, "x11", "tcp", "X Window System", False),
        6379: Service(6379, "redis", "tcp", "Redis", True),
        7001: Service(7001, "weblogic", "tcp", "WebLogic", False),
        8000: Service(8000, "http-alt", "tcp", "HTTP Alternative", False),
        8080: Service(8080, "http-proxy", "tcp", "HTTP Proxy", True),
        8443: Service(8443, "https-alt", "tcp", "HTTPS Alternative", True),
        8888: Service(8888, "http-alt", "tcp", "HTTP Alternative", False),
        9000: Service(9000, "cslistener", "tcp", "CSlistener", False),
        9090: Service(9090, "websm", "tcp", "WebSM", False),
        9200: Service(9200, "elasticsearch", "tcp", "Elasticsearch", True),
        9300: Service(9300, "elasticsearch-node", "tcp", "Elasticsearch Node", True),
        11211: Service(11211, "memcached", "tcp/udp", "Memcached", True),
        27017: Service(27017, "mongodb", "tcp", "MongoDB", True),
        27018: Service(27018, "mongodb-alt", "tcp", "MongoDB Alternative", True),
        27019: Service(27019, "mongodb-alt", "tcp", "MongoDB Alternative", True),
        27020: Service(27020, "mongodb-alt", "tcp", "MongoDB Alternative", True),
        50500: Service(50500, "sap", "tcp", "SAP", False),
    }

    @classmethod
    def get_service(cls, port: int, protocol: str = "tcp") -> Optional[Service]:
        """
        Get service information for a specific port.

        Args:
            port: Port number (1-65535)
            protocol: Protocol (tcp/udp), case-insensitive

        Returns:
            Service object if found, None otherwise

        Example:
            service = ServiceDetector.get_service(22)
            print(service.name)  # "ssh"
            print(service.description)  # "Secure Shell (SSH)"
        """
        if port in cls.PORT_SERVICES:
            return cls.PORT_SERVICES[port]
        return None

    @classmethod
    def get_service_name(cls, port: int) -> str:
        """
        Get just the service name for a port.

        Args:
            port: Port number

        Returns:
            Service name or "Unknown" if not found

        Example:
            name = ServiceDetector.get_service_name(80)
            print(name)  # "HTTP"
        """
        service = cls.get_service(port)
        if service:
            return service.name.upper()
        return "Unknown"

    @classmethod
    def get_service_description(cls, port: int) -> str:
        """
        Get full description of a service.

        Args:
            port: Port number

        Returns:
            Service description or "Unknown Service" if not found

        Example:
            desc = ServiceDetector.get_service_description(22)
            # "Secure Shell (SSH)"
        """
        service = cls.get_service(port)
        if service:
            return service.description
        return "Unknown Service"

    @classmethod
    def is_well_known_port(cls, port: int) -> bool:
        """
        Check if a port is a well-known port (1-1023).

        Args:
            port: Port number

        Returns:
            True if well-known, False otherwise

        Example:
            >>> ServiceDetector.is_well_known_port(22)
            True
            >>> ServiceDetector.is_well_known_port(3306)
            False
        """
        return 1 <= port <= 1023

    @classmethod
    def is_registered_port(cls, port: int) -> bool:
        """
        Check if a port is a registered port (1024-49151).

        Args:
            port: Port number

        Returns:
            True if registered, False otherwise
        """
        return 1024 <= port <= 49151

    @classmethod
    def is_dynamic_port(cls, port: int) -> bool:
        """
        Check if a port is a dynamic/ephemeral port (49152-65535).

        Args:
            port: Port number

        Returns:
            True if dynamic, False otherwise
        """
        return 49152 <= port <= 65535

    @classmethod
    def get_common_ports(cls) -> List[int]:
        """
        Get list of commonly-used ports.

        Returns:
            List of port numbers that are frequently used

        Example:
            common = ServiceDetector.get_common_ports()
            # [20, 21, 22, 23, 25, 53, 69, 70, 79, 80, 88, 110, 143, ...]
        """
        return [port for port, service in cls.PORT_SERVICES.items() if service.common]

    @classmethod
    def get_top_ports(cls, count: int = 100) -> List[int]:
        """
        Get the most common ports to scan.

        Args:
            count: Number of ports to return (default 100)

        Returns:
            List of port numbers sorted by commonality

        Example:
            top_ports = ServiceDetector.get_top_ports(50)
            results = scanner.scan_ports(top_ports)
        """
        common_ports = cls.get_common_ports()
        return common_ports[:count]

    @classmethod
    def search_service(cls, keyword: str) -> List[Service]:
        """
        Search for services by keyword.

        Args:
            keyword: Service name or description keyword (case-insensitive)

        Returns:
            List of matching Service objects

        Example:
            results = ServiceDetector.search_service("sql")
            # Returns all services with "sql" in name/description
        """
        keyword_lower = keyword.lower()
        matches = []

        for port, service in cls.PORT_SERVICES.items():
            if (keyword_lower in service.name.lower() or
                keyword_lower in service.description.lower()):
                matches.append(service)

        return matches

    @classmethod
    def get_port_category(cls, port: int) -> str:
        """
        Get the category of a port (well-known, registered, or dynamic).

        Args:
            port: Port number

        Returns:
            String describing the port category

        Example:
            >>> ServiceDetector.get_port_category(22)
            "Well-known Port (0-1023)"
            >>> ServiceDetector.get_port_category(3306)
            "Registered Port (1024-49151)"
            >>> ServiceDetector.get_port_category(55000)
            "Dynamic/Ephemeral Port (49152-65535)"
        """
        if cls.is_well_known_port(port):
            return "Well-known Port (0-1023)"
        elif cls.is_registered_port(port):
            return "Registered Port (1024-49151)"
        elif cls.is_dynamic_port(port):
            return "Dynamic/Ephemeral Port (49152-65535)"
        else:
            return "Invalid Port (> 65535)"

    @classmethod
    def format_result(cls, port: int, state: str) -> str:
        """
        Format a port scan result with service name.

        Args:
            port: Port number
            state: Port state (OPEN, CLOSED, FILTERED)

        Returns:
            Formatted result string

        Example:
            result = ServiceDetector.format_result(22, "OPEN")
            print(result)  # "[+] 22/tcp OPEN → SSH (Secure Shell)"
        """
        service_name = cls.get_service_name(port)
        symbol = "[+]" if state == "OPEN" else "[-]" if state == "CLOSED" else "[?]"

        if service_name == "Unknown":
            return f"{symbol} {port}/tcp {state}"
        else:
            description = cls.get_service_description(port)
            return f"{symbol} {port}/tcp {state} → {service_name} ({description})"

    @classmethod
    def get_all_services(cls) -> Dict[int, Service]:
        """
        Get all known services.

        Returns:
            Dictionary of port → Service mappings

        Example:
            all_services = ServiceDetector.get_all_services()
            print(f"Knows about {len(all_services)} services")
        """
        return cls.PORT_SERVICES.copy()

    @classmethod
    def add_custom_service(cls, port: int, service: Service) -> None:
        """
        Add a custom service mapping.

        Useful for local services not in IANA registry.

        Args:
            port: Port number
            service: Service object

        Example:
            custom = Service(
                8080,
                "myapp",
                "tcp",
                "My Custom Application"
            )
            ServiceDetector.add_custom_service(8080, custom)
        """
        cls.PORT_SERVICES[port] = service


# Helper function for quick lookups
def get_service_info(port: int) -> Dict[str, str]:
    """
    Quick helper function to get all service info for a port.

    Args:
        port: Port number

    Returns:
        Dictionary with service details

    Example:
        info = get_service_info(22)
        # {
        #     'name': 'ssh',
        #     'description': 'Secure Shell (SSH)',
        #     'category': 'Well-known Port (0-1023)'
        # }
    """
    service = ServiceDetector.get_service(port)

    return {
        'name': service.name.upper() if service else 'Unknown',
        'description': service.description if service else 'Unknown Service',
        'protocol': service.protocol if service else 'tcp',
        'category': ServiceDetector.get_port_category(port),
        'common': service.common if service else False
    }
