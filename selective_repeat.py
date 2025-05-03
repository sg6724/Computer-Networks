import threading
import queue
import random
import time

class SelectiveRepeatServer(threading.Thread):
    TOTAL_PACKETS = 10
    WINDOW_SIZE = 4

    def __init__(self, channel, ack_channel):
        super().__init__()
        self.channel = channel
        self.ack_channel = ack_channel
        self.acked = [False] * self.TOTAL_PACKETS

    def run(self):
        base = 0
        while base < self.TOTAL_PACKETS:
            # Send all packets in window that aren't acked
            for i in range(base, min(base + self.WINDOW_SIZE, self.TOTAL_PACKETS)):
                if not self.acked[i]:
                    print(f"[SERVER] Sending packet {i}")
                    self.channel.put(i)
                    self.sleep(0.1)

            # Process ACKs
            while not self.ack_channel.empty():
                ack = self.ack_channel.get()
                print(f"[SERVER] ACK received for packet {ack}")
                self.acked[ack] = True

            # Slide window
            while base < self.TOTAL_PACKETS and self.acked[base]:
                base += 1

            self.sleep(0.5)

        print("\n[SERVER] All packets sent and acknowledged.")

    def sleep(self, seconds):
        try:
            time.sleep(seconds)
        except KeyboardInterrupt:
            pass

class SelectiveRepeatClient(threading.Thread):
    def __init__(self, channel, ack_channel):
        super().__init__()
        self.channel = channel
        self.ack_channel = ack_channel
        self.received = [False] * SelectiveRepeatServer.TOTAL_PACKETS
        self.rand = random.Random()

    def run(self):
        while True:
            try:
                packet = self.channel.get_nowait()
            except queue.Empty:
                continue

            if self.received[packet]:
                print(f"    [CLIENT] Duplicate packet {packet} ignored.")
                continue

            if self.rand.random() < 0.2:
                print(f"    [CLIENT] Packet {packet} lost!")
                continue

            print(f"    [CLIENT] Packet {packet} received. Sending ACK.")
            self.received[packet] = True
            self.ack_channel.put(packet)
            self.sleep(0.1)

            if self.all_received():
                break

    def all_received(self):
        return all(self.received)

    def sleep(self, seconds):
        try:
            time.sleep(seconds)
        except KeyboardInterrupt:
            pass

# --- Main execution ---
if __name__ == "__main__":
    channel = queue.Queue()
    ack_channel = queue.Queue()

    server = SelectiveRepeatServer(channel, ack_channel)
    client = SelectiveRepeatClient(channel, ack_channel)

    server.start()
    client.start()

    server.join()
    client.join()
