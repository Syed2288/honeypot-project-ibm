import socket
import json
from datetime import datetime

HOST = "0.0.0.0"
PORT = 8888
LOG_FILE = "logs.json"
ip_tracker = {}


def save_log(entry):
    try:
        with open(LOG_FILE, "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append(entry)

    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=4)


def start_honeypot():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)

    # ✅ CORRECT INDENTATION
    print("🔥 Honeypot Started Successfully")
    print(f"📡 Listening on PORT {PORT}...")
    print("🛡️ Waiting for attackers...\n")

    while True:
        client_socket, addr = server.accept()
        ip = addr[0]
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        ip_tracker[ip] = ip_tracker.get(ip, 0) + 1

        # ✅ FIXED BLOCK
        log_entry = {
            "timestamp": time_now,
            "ip": ip,
            "attempts": ip_tracker[ip],
            "type": "Brute Force Attempt" if ip_tracker[ip] >= 3 else "Unauthorized Access",
            "status": "Blocked",
            "port": PORT,
            "protocol": "TCP",
            "message": "Multiple suspicious attempts detected! Possible brute force attack blocked."
                       if ip_tracker[ip] >= 3
                       else "Unauthorized access attempt detected. Connection denied."
        }

        save_log(log_entry)

        client_socket.send(log_entry["message"].encode())
        client_socket.close()

        # ✅ IMPROVED OUTPUT
        print("\n🚨 New Connection Detected!")
        print(f"📅 Time      : {time_now}")
        print(f"🌐 IP        : {ip}")
        print(f"🔁 Attempts  : {ip_tracker[ip]}")
        print(f"⚠️ Type      : {log_entry['type']}")
        print(f"💬 Message   : {log_entry['message']}")
        print("-" * 40)


if __name__ == "__main__":
    start_honeypot()