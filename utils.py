#selecting network interfaces

from typing import List, Optional, Dict

import psutil #retrieving information about the system
from psutil._common import snicaddr #store the address of a network interface

def format_mb(size_in_bytes: int) -> str:
     """Format the size in bytes to MB."""
     return f"{size_in_bytes / 1024 / 1024:.2f} MB"
 
def select_network_interfaces(prefer_interfaces: Optional[List[str]] = None) -> Dict[str, List[snicaddr]]:
     """
    Select network interfaces based on a preference list or common defaults.

    Args:
    prefer_interfaces (Optional[List[str]]):
        A list of network interface names to prefer. If None, common defaults are used.

    Returns:
        Dict[str, List[snicaddr]]:
            A dictionary of network interfaces and their addresses.
    """
     common_network_interfaces = ["eth0", "en0", "wlan0"]
     nis = psutil.net_if_addrs() #retrieve information about network interfaces
     names = set(nis.keys())
     print(f"Available network interfaces: {', '.join(names)}")
     selector = set(common_network_interfaces) if prefer_interfaces is None else set(prefer_interfaces)
     selector = selector.intersection(names)
     return {network_name: nis[network_name] for network_name in selector}
 
 