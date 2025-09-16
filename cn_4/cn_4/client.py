import cv2
import socket
import numpy as np

# Client configuration
CLIENT_IP = "0.0.0.0"  # listen on all interfaces
CLIENT_PORT = 9999
CHUNK_SIZE = 4096

# Create UDP socket and bind
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((CLIENT_IP, CLIENT_PORT))

print("Client listening... Press 'q' to quit.")

buffer = b""

while True:
    packet, _ = sock.recvfrom(CHUNK_SIZE + 1)
    marker, chunk = packet[0:1], packet[1:]
    buffer += chunk

    # If marker=1 → last chunk of frame
    if marker == b'1':
        # Decode frame
        frame = cv2.imdecode(np.frombuffer(buffer, np.uint8), cv2.IMREAD_COLOR)
        buffer = b""

        if frame is not None:
            cv2.imshow("UDP Video Stream", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

sock.close()
cv2.destroyAllWindows()
print("Client stopped.")
