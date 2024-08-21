#Handles the recording of captured network packets from the queue into .pcapchunked files.

import queue
from scapy.all import wrpcap

from shared_state import packet_queue
from utils import format_mb

CHUNK_SIZE = 100 * 1024 * 1024  # 100 MB
output_file_prefix = "captured/captured_chunk_"
current_chunk_size = 0
chunk_index = 0
packets = []

def write_to_file_worker():
    """
    Worker thread that writes packets to files in chunks.
    """
    global current_chunk_size, chunk_index, packets
    
    while True:
        try:
            # Get a packet from the queue
            packet = packet_queue.get(timeout=1)
            packet_size = len(packet)
            packets.append(packet)
            current_chunk_size += packet_size
            
            # Check if the current chunk size exceeds the CHUNK_SIZE
            if current_chunk_size >= CHUNK_SIZE:
                # Write the chunk to a file
                output_file = f"{output_file_prefix}{chunk_index}.pcap"
                wrpcap(output_file, packets)
                print(f"Saved chunk {chunk_index} with size {format_mb(current_chunk_size)} to {output_file}")
                
             # Reset for the next chunk
                chunk_index += 1
                packets = []
                current_chunk_size = 0

        except queue.Empty:
            continue # Continue if the queue is empty
def flush_packets_to_file():
    """
    Flush the remaining packets in the queue to a file.
    """
    global current_chunk_size, chunk_index, packets

    if packets:
        output_file = f"{output_file_prefix}{chunk_index}.pcap"
        wrpcap(output_file, packets)
        print(f"Flushed remaining packets to {output_file} with size {format_mb(current_chunk_size)}")

        # Reset the packet list and chunk size
        packets = []
        current_chunk_size = 0
