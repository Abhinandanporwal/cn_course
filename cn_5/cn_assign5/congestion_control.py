import matplotlib.pyplot as plt
import math

def tcp_congestion_control(total_rounds=60, loss_rounds=None, ssthresh_init=16):
    if loss_rounds is None:
        loss_rounds = {18, 30, 45}

    cwnd = 1.0
    ssthresh = float(ssthresh_init)
    history = []
    phase = "Slow Start"

    for r in range(total_rounds):
        history.append(cwnd)
        if r in loss_rounds:
            print(f"Round {r}: LOSS detected! ssthresh={math.floor(cwnd/2)}, cwnd reset to 1")
            ssthresh = max(2.0, math.floor(cwnd / 2.0))
            cwnd = 1.0
            phase = "Timeout -> Slow Start"
            continue
        if cwnd < ssthresh:
            cwnd += 1.0
            phase = "Slow Start"
        else:
            cwnd += 1.0 / cwnd
            phase = "Congestion Avoidance"

        cwnd = min(cwnd, 200.0)
    rounds = list(range(total_rounds))
    plt.figure(figsize=(9, 4.5))
    plt.plot(rounds, history, linewidth=2)
    plt.title("TCP Congestion Control: cwnd vs Transmission Rounds")
    plt.xlabel("Transmission Rounds (RTTs)")
    plt.ylabel("Congestion Window (cwnd in MSS)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("cwnd_plot.png", dpi=150)
    plt.show()

    print("\nSimulation complete! Plot saved as 'cwnd_plot.png'")
    return history


if __name__ == "__main__":
    tcp_congestion_control(total_rounds=60, ssthresh_init=16)
