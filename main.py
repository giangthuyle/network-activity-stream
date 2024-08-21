import argparse 
import threading
import signal
import sys

from scapy.all import sniff 

from packet_sniffer import sniff_callback_builder
from utils import select_network_interfaces
from reports.console_report import periodic_report
from reports.pcap_report import write_to_file_worker, flush_packets_to_file

def parse_argument():
    parse = argparse.ArgumentParser(description="Network activity capture tool")
    parse.add_argument(
        "-i", "--interface",
        type = str,
        nargs= "+",
        help="List of network interfaces to monitor. If not provided, the default interfaces will be used."
    )
    return parse.parse_args()

def signal_handler(sig, frame):
    """
    Handle termination signals (e.g., Ctrl+C).
    This function flushes the packet queue to a file before exiting.
    """
    print("Termination signal received. Flushing remaining packets to file...")
    flush_packets_to_file()
    sys.exit(0)
    
def start_reports():
    """
    Start the reports threads for writing packets to file and reporting network activity.

    This function initializes and starts two daemon threads:
    1. write_worker_thread: Responsible for writing captured packets to files in chunks.
    2. size_report_thread: Responsible for periodically reporting the network activity (received and sent sizes).

    Both threads run indefinitely in the background as daemon threads.
    """
    write_worker_thread = threading.Thread(target=write_to_file_worker, daemon=True)
    write_worker_thread.start()

    size_report_thread = threading.Thread(target=periodic_report, daemon=True)
    size_report_thread.start()

def main():
    # Register the signal handler for SIGINT (Ctrl+C)
    signal.signal(signal.SIGINT, signal_handler)
    
    args = parse_argument()

    start_reports()
    print(args.interface)
    # Select network interfaces based on CLI input or defaults
    if args.interface:
        network_interfaces = select_network_interfaces(prefer_interfaces=args.interfaces)
    else:
        network_interfaces = select_network_interfaces()
    
    interfaces_names = list(network_interfaces.keys())
    local_ips = set()
    for name, addresses in network_interfaces.items():
        for address in addresses:
            local_ips.add(address.address)
    
    # Sniffing packets on all network interfaces
    print(f"Sniffing packets from {' '.join(interfaces_names)}...")
    sniff(iface=interfaces_names, prn=sniff_callback_builder(local_ips))


if __name__ == "__main__":
    main()
    