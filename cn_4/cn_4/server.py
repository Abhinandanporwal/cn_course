import cv2
import socket
import math
import time

# Server configuration
SERVER_IP = "127.0.0.1"   # localhost (change if on LAN)
SERVER_PORT = 9999
CHUNK_SIZE = 4096  # bytes

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Open video file (or 0 for webcam)
cap = cv2.VideoCapture("sample.mp4")
fps = cap.get(cv2.CAP_PROP_FPS) or 25
frame_interval = 1.0 / fps

print("Server started... Streaming video")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Resize frame for faster transfer
    frame = cv2.resize(frame, (640, 480))

    # Encode frame as JPEG
    encoded, buffer = cv2.imencode(".jpg", frame)
    data = buffer.tobytes()

    # Split into chunks
    total_chunks = math.ceil(len(data) / CHUNK_SIZE)
    for i in range(total_chunks):
        start = i * CHUNK_SIZE
        end = start + CHUNK_SIZE
        chunk = data[start:end]

        # Add marker: b'1' if last chunk, else b'0'
        marker = b'1' if i == total_chunks - 1 else b'0'
        sock.sendto(marker + chunk, (SERVER_IP, SERVER_PORT))

    time.sleep(frame_interval)

cap.release()
sock.close()
print("Server stopped.")
