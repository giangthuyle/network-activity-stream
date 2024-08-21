#Process network packets when they are "sniffed" using Scapy. 
#This callback will be called every time a new network packet is captured,
#And it will update the network status and add the packet to a queue for later processing.

from typing import Set

from shared_state import network_activity_state, packet_queue

def sniff_callback_builder(source_ips: Set[str]):
    def callback(packet):
        packet_size = len(packet)
        
        #Updated shared state
        packet_queue.put(packet)
        if packet.haslayer("IP"):
            ip_layer = packet["IP"]
            
            #Check if packet is sent or received
            if ip_layer.src in source_ips:
                network_activity_state.last_second_sent_size += packet_size
            elif ip_layer.dst in source_ips:
                network_activity_state.last_second_received_size += packet_size
                
    return callback
            