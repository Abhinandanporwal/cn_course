import random
import time

FRAME_LOSS_PROBABILITY = 0.3
TIMEOUT = 2
TOTAL_FRAMES = 5

def send_frame(frame_number):
    """Simulate sending a frame, possibly lost."""
    print(f"Sending Frame {frame_number}")
    time.sleep(0.5)
    if random.random() < FRAME_LOSS_PROBABILITY:
        print(f"Frame {frame_number} lost, retransmitting ...")
        return False
    else:
        time.sleep(0.5)
        print(f"ACK {frame_number} received")
        return True

def stop_and_wait_arq():
    current_frame = 0
    while current_frame < TOTAL_FRAMES:
        success = send_frame(current_frame)
        if not success:
            time.sleep(TIMEOUT)
            print(f"Timeout! Retransmitting Frame {current_frame} ...")
            continue
        else:
            current_frame += 1
        print("-" * 40)
    print("\nAll frames transmitted successfully ✅")

if __name__ == "__main__":
    random.seed(time.time())
    stop_and_wait_arq()
