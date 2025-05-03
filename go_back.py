import threading
import queue
import random
import time

class GoBackNServer(threading.Thread):
    TOTAL_PACKETS = 10
    WINDOW_SIZE = 4

    def __init__(self, channel, ack_channel):
        super().__init__()
        self.channel = channel
        self.ack_channel = ack_channel
        self.base = 0
        self.next_seq_num = 0
        self.timer_active = False

    def run(self):
        while self.base < self.TOTAL_PACKETS:
            # Send packets within the window
            while self.next_seq_num < self.base + self.WINDOW_SIZE and self.next_seq_num < self.TOTAL_PACKETS:
                print(f"[SERVER] Sending packet {self.next_seq_num}")
                self.channel.put(self.next_seq_num)
                self.next_seq_num += 1
                self.sleep(0.1)

            # Process ACKs
            while not self.ack_channel.empty():
                ack = self.ack_channel.get()
                print(f"[SERVER] ACK received for packet {ack}")
                if ack >= self.base:
                    self.base = ack + 1

            # If timeout (simulate with delay), resend all from base
            if self.base < self.next_seq_num:
                print(f"[SERVER] Timeout occurred. Resending from packet {self.base}")
                for i in range(self.base, self.next_seq_num):
                    print(f"[SERVER] Resending packet {i}")
                    self.channel.put(i)
                    self.sleep(0.1)

            self.sleep(0.5)

        print("\n[SERVER] All packets sent and acknowledged.")

    def sleep(self, seconds):
        try:
            time.sleep(seconds)
        except KeyboardInterrupt:
            pass

class GoBackNClient(threading.Thread):
    def __init__(self, channel, ack_channel):
        super().__init__()
        self.channel = channel
        self.ack_channel = ack_channel
        self.expected = 0
        self.rand = random.Random()

    def run(self):
        while True:
            try:
                packet = self.channel.get_nowait()
            except queue.Empty:
                continue

            if self.rand.random() < 0.2:
                print(f"    [CLIENT] Packet {packet} lost!")
                continue

            if packet == self.expected:
                print(f"    [CLIENT] Packet {packet} received correctly. Sending ACK.")
                self.ack_channel.put(packet)
                self.expected += 1
            else:
                print(f"    [CLIENT] Packet {packet} out of order. Discarded.")
                # Send ACK for last correctly received (expected-1)
                self.ack_channel.put(self.expected - 1)

            self.sleep(0.1)

            if self.expected >= GoBackNServer.TOTAL_PACKETS:
                break

    def sleep(self, seconds):
        try:
            time.sleep(seconds)
        except KeyboardInterrupt:
            pass

# --- Main execution ---
if __name__ == "__main__":
    channel = queue.Queue()
    ack_channel = queue.Queue()

    server = GoBackNServer(channel, ack_channel)
    client = GoBackNClient(channel, ack_channel)

    server.start()
    client.start()

    server.join()
    client.join()
