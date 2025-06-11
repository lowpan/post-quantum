import os
from matplotlib.patches import Patch
import matplotlib.pyplot as plt
import numpy as np
from scapy.all import rdpcap, Packet
from scapy.layers.inet6 import IPv6, ICMPv6RPL

def pretty_label(label_stem):
    if label_stem.startswith("kyber"):
        return "AES"
    elif label_stem.startswith("no_cryptography"):
        return "No Cryptography"
    return label_stem

def get_last_representative_packet_sizes(file_path):
    """
    Reads a .pcap file and finds the sizes of the last representative DIO (from root),
    DAO (for root) and DAO-ACK (from root) packages found in the file.
    Returns a dictionary in the format {"DIO": size, "DAO": size, "DAO-ACK": size}.
    """
    try:
        packets = rdpcap(file_path)
    except Exception as e:
        return {"DIO": 0, "DAO": 0, "DAO-ACK": 0}

    packet_sizes = {"DIO": 0, "DAO": 0, "DAO-ACK": 0}
    ICMPV6_RPL_TYPE = 155
    
    codes = {
        "DIO": [1, 129],
        "DAO": [2, 130],
        "DAO-ACK": [3, 131]
    }

    for packet in packets:
        if packet.haslayer(ICMPv6RPL) and packet[ICMPv6RPL].type == ICMPV6_RPL_TYPE:
            code = packet[ICMPv6RPL].code
            is_from_root = packet[IPv6].src == "fe80::1"
            is_to_root = packet[IPv6].dst == "fe80::1"

            if code in codes["DIO"] and is_from_root:
                packet_sizes["DIO"] = len(packet)
            elif code in codes["DAO"] and is_to_root:
                packet_sizes["DAO"] = len(packet) if len(packet) > packet_sizes["DAO"]  else packet_sizes["DAO"]
            elif code in codes["DAO-ACK"] and is_from_root:
                packet_sizes["DAO-ACK"] = len(packet)
            
    return packet_sizes

PCAP_FOLDER = "results"
OUTPUT_FOLDER = "output/"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

TOPOLOGIES_TO_PLOT = [1, 4, 12]
ITERATION_NUM = 1

CRYPTO_SCENARIOS = ["no_cryptography", "kyber"]
PACKET_TYPES = ["DIO", "DAO", "DAO-ACK"]

results = {topo_id: {scenario: {} for scenario in CRYPTO_SCENARIOS} for topo_id in TOPOLOGIES_TO_PLOT}

for topo_id in TOPOLOGIES_TO_PLOT:
    for scenario in CRYPTO_SCENARIOS:
        file_name = f"{scenario}_{ITERATION_NUM}_{topo_id}.pcap"
        file_path = os.path.join(PCAP_FOLDER, file_name)
        
        if os.path.exists(file_path):
            packet_lengths = get_last_representative_packet_sizes(file_path)
            results[topo_id][scenario] = packet_lengths
        else:
            
            results[topo_id][scenario] = {"DIO": 0, "DAO": 0, "DAO-ACK": 0}

fig, ax = plt.subplots(figsize=(14, 8))

bar_width = 0.08
pkt_group_spacing = 0.4
scenario_group_spacing = 0.8
pkt_colors = {"DIO": "#c93c37", "DAO": "#2f75b6", "DAO-ACK": "#4fbd4f"} 
topo_hatches = {"1": "", "4": "///", "12": "xxx"}
background_colors = ['#f0f0f0', '#eaf5ff'] 

current_pos = 0.5 
for i, scenario in enumerate(CRYPTO_SCENARIOS):

    scenario_group_start = current_pos - pkt_group_spacing / 2
    

    for j, pkt_type in enumerate(PACKET_TYPES):
    
        for k, topo_id in enumerate(TOPOLOGIES_TO_PLOT):
            data = results[topo_id][scenario].get(pkt_type, 0)
            
            rects = ax.bar(current_pos, data, bar_width, 
                           color=pkt_colors[pkt_type],
                           hatch=topo_hatches[str(topo_id)],
                           edgecolor='black',
                           linewidth=0.8)
            
        
            if data > 0:
                ax.bar_label(rects, padding=3, fontsize=8, fmt='%d')

            current_pos += bar_width
        
    
        current_pos += pkt_group_spacing
        
    scenario_group_end = current_pos - pkt_group_spacing * 0.7
    

    ax.axvspan(scenario_group_start, scenario_group_end, 
               facecolor=background_colors[i], alpha=0.5, zorder=0)


    group_center = (scenario_group_start + scenario_group_end) / 2
    ax.text(group_center, 240, pretty_label(scenario), 
            ha='center', va='top', fontsize=15, weight='bold',
            bbox=dict(boxstyle="square,pad=0.3", fc="white", ec="none", alpha=0.5))
    

    current_pos += scenario_group_spacing

ax.set_title("RPL Control Packet Sizes by Scenario and Topology", fontsize=16, pad=20)
ax.set_ylabel("Packet Size (Bytes)", fontsize=12)

ax.set_xticks([])
ax.set_xlabel("")

all_values = [size for topo_res in results.values() for scen_res in topo_res.values() for size in scen_res.values()]
if all_values:
    ax.set_ylim(bottom=0, top=max(all_values) * 1.25)

ax.yaxis.grid(True, linestyle='--', which='major', color='grey', alpha=0.6)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.tick_params(axis='x', length=0)

legend_elements = [
    Patch(facecolor='white', edgecolor='black', hatch=topo_hatches['1'], label='Topologia 1'),
    Patch(facecolor='white', edgecolor='black', hatch=topo_hatches['4'], label='Topologia 4'),
    Patch(facecolor='white', edgecolor='black', hatch=topo_hatches['12'], label='Topologia 12'),
    Patch(facecolor='white', edgecolor='white', label=''),
    Patch(facecolor=pkt_colors['DIO'], label='DIO'),
    Patch(facecolor=pkt_colors['DAO'], label='DAO'),
    Patch(facecolor=pkt_colors['DAO-ACK'], label='DAO-ACK'),
]
ax.legend(handles=legend_elements, title="Legenda", loc='upper left', bbox_to_anchor=(0.01, 0.95), fontsize=9)

plt.tight_layout(rect=[0, 0, 1, 0.95])

output_filename = os.path.join(OUTPUT_FOLDER, "packet_size_symmetric.png")
plt.savefig(output_filename, dpi=300)
plt.close(fig)

