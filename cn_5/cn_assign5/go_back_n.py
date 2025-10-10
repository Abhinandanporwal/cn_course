import random
import time

TOTAL_FRAMES = 10       
WINDOW_SIZE = 4         
LOSS_PROBABILITY = 0.2   
TRANSMISSION_DELAY = 0.5

def send_frames(start, end):
    """Simulate sending frames from start to end (inclusive)."""
    print(f"Sending frames {start} to {end}")
    time.sleep(TRANSMISSION_DELAY)

    if random.random() < LOSS_PROBABILITY:
        lost_frame = random.randint(start, end)
        print(f"Frame {lost_frame} lost, retransmitting frames {lost_frame} to {end}")
        return lost_frame - 1
    else:
        print(f"ACK {end} received")
        return end

def go_back_n_arq(total_frames, window_size, loss_prob):
    random.seed(time.time())

    base = 0  
    next_frame = 0

    while base < total_frames:
        end_frame = min(base + window_size - 1, total_frames - 1)
        ack = send_frames(base, end_frame)

        if ack < end_frame:
            time.sleep(1)
            base = ack + 1
            continue
        else:
            base = ack + 1
            next_frame = base + window_size - 1
            if base < total_frames:
                next_start = base
                next_end = min(next_start + window_size - 1, total_frames - 1)
                print(f"Window slides to {next_start} to {next_end}")

        print("-" * 45)
        time.sleep(0.5)

    print("\n All frames transmitted successfully!")

if __name__ == "__main__":
    go_back_n_arq(TOTAL_FRAMES, WINDOW_SIZE, LOSS_PROBABILITY)
