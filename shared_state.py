import queue

class NetworkActivityState:
    def __init__(self):
        self.last_second_received_size = 0
        self.last_second_sent_size = 0
        self.last_report_time = 0
        
#Create a single instance of this state to be shared across the modules
network_activity_state = NetworkActivityState()
packet_queue = queue.Queue()


