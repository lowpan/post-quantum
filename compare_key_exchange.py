import os
import matplotlib.pyplot as plt
import numpy as np
from scapy.all import rdpcap
from scapy.layers.inet6 import IPv6, ICMPv6RPL

def pretty_label(label_stem):
    if label_stem.startswith("kyber"):
        return "Kyber"
    elif label_stem.startswith("rsa"):
        return "RSA"
    return label_stem

def get_key_exchange_time(file_path):
    """
    Reads a .pcap file and calculates the key exchange time, measured between root receiving
    the first public key (PK) and root sending the last DIS message.
    Returns the duration in seconds.
    """
    try:
        packets = rdpcap(file_path)
    except Exception as e:
        
        return 0.0

    ICMPV6_RPL_TYPE = 155
    codes = {
        "PK": 144,
        "DIS": 128
    }
    
    t0 = 0.0 
    t_final = 0.0


    for packet in packets:
        if packet.haslayer(ICMPv6RPL) and packet[ICMPv6RPL].type == ICMPV6_RPL_TYPE:
            code = packet[ICMPv6RPL].code
            is_from_root = packet.getlayer(IPv6).src == "fe80::1"
            is_to_root = packet.getlayer(IPv6).src == "fe80::2"

        
            if code == codes["PK"] and is_to_root:
                t0 = float(packet.time)
            
        
            elif code == codes["DIS"] and is_from_root:
                t_final = float(packet.time)
    

    total_time = t_final - t0 if t_final > t0 else 0.0
    
    return total_time

PCAP_FOLDER = "results/"
OUTPUT_FOLDER = "output/"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

TOPOLOGY_ID = 1
NUM_ITERATIONS = 10
CRYPTO_SCENARIOS = ["rsa", "kyber"]

results_per_scenario = {scenario: [] for scenario in CRYPTO_SCENARIOS}


for scenario in CRYPTO_SCENARIOS:
    for i in range(1, NUM_ITERATIONS + 1):
        file_name = f"{scenario}_{i}_{TOPOLOGY_ID}.pcap"
        file_path = os.path.join(PCAP_FOLDER, file_name)
        
        if os.path.exists(file_path):
            exchange_time = get_key_exchange_time(file_path)
            if exchange_time > 0:
                results_per_scenario[scenario].append(exchange_time)
               
            

average_times_cs = {}
for scenario, times_list in results_per_scenario.items():
    if times_list:
    
        average_sec = np.mean(times_list)
        average_times_cs[scenario] = average_sec * 1000
    else:
        average_times_cs[scenario] = 0
    

labels = [pretty_label(s) for s in CRYPTO_SCENARIOS]
values_cs = [average_times_cs.get(s, 0) for s in CRYPTO_SCENARIOS]
colors = ['tab:blue', 'tab:orange']

fig, ax = plt.subplots(figsize=(8, 6))

bars = ax.bar(labels, values_cs, color=colors, width=0.5, zorder=3)

ax.bar_label(bars, fmt='%.4f ms', padding=3, fontsize=11, weight='bold')

ax.set_title("Average Key Exchange Time by Cryptography Scenario", fontsize=16, pad=20)
ax.set_ylabel("Average Time (milliseconds)", fontsize=12)
ax.set_xlabel("Cryptography Scenario", fontsize=12)

if values_cs:
    ax.set_ylim(bottom=0, top=max(values_cs) * 1.20 if max(values_cs) > 0 else 100)

ax.yaxis.grid(True, linestyle='--', which='major', color='grey', alpha=0.7, zorder=0)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)

plt.tight_layout()

output_filename = os.path.join(OUTPUT_FOLDER, "key_exchange_time_comparison.png")
plt.savefig(output_filename, dpi=300)

plt.close(fig)


