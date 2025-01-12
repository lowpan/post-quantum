import os
import re
import sys
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import glob
from scapy.all import rdpcap
from scapy.layers.inet6 import IPv6
from scapy.layers.inet6 import ICMPv6ND_RA, ICMPv6RPL

def extract_number(filename):
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else float('inf')

# Função para ler dados de um arquivo e extrair as informações
def read_data_from_file(file_path):
    timestamps = []
    values = []  # To store tx values
    packets = rdpcap(file_path)

    # Defining ICMPv6 RPL types and codes
    ICMPV6_RPL_DIO_TYPE = 155
    ICMPV6_Cripto1 = 144
    ICMPV6_Cripto2 = 145
    rpl_codes = {
        128: "DIS", 129: "DIO", 130: "DAO", 131: "DAOACK",
        0: "DIS", 1: "DIO", 2: "DAO", 3: "DAOACK"
    }

    # Filtering ICMPv6 RPL packets
    for id, packet in enumerate(packets):
        if packet.haslayer(IPv6) and packet.haslayer(ICMPv6RPL):
            icmp_code = packet[ICMPv6RPL].code
            if packet[ICMPv6RPL].type == ICMPV6_RPL_DIO_TYPE:
                # Handle specific message codes
                if icmp_code == ICMPV6_Cripto1:
                    print(f"Chave Pública {file_path[:-5]}: {len(packet)}")
                elif icmp_code == ICMPV6_Cripto2:
                    print(f"Chave Privada {file_path[:-5]}: {len(packet)}")
                elif icmp_code in rpl_codes:
                    label = rpl_codes[icmp_code]
                    print(f"{label} {file_path[:-5]}: {len(packet)}")
                    values.append(len(packet))
                    timestamps.append(id)

    return timestamps, values



file_paths = ['kyber.pcap', 'rsa.pcap', 'sem_criptografia.pcap']

# Definindo cores e estilos fixos
colors = ["tab:orange", "tab:blue", "tab:green", "tab:red", "tab:purple"]
linestyles = ['--', '-.', ':', '-', '--']

# Criando um único gráfico para todos os arquivos
fig, ax1 = plt.subplots(figsize=(10, 4))

# Plotando todas as curvas no mesmo gráfico
for idx, file_path in enumerate(file_paths):
    timestamps, values1 = read_data_from_file(file_path)
    label_name = file_path.split('/')[-1].replace("_", " ")

    # Usando cores e estilos de forma cíclica
    ax1.plot(
        timestamps, 
        values1, 
        linestyle=linestyles[idx % len(linestyles)],
        label=f'{label_name[:-5]}',
        color=colors[idx % len(colors)]
    )

    xy0 = (10, 122.5)
    xy1 = (11.5, 30.5)
    ax1.annotate('Sensor2', xy0, xy1, arrowprops=dict(arrowstyle='<-', color='k', shrinkA=0, shrinkB=0))

    xy0 = (17, 141.5)
    xy1 = (21.5, 30.5)
    ax1.annotate('Sensor3', xy0, xy1, arrowprops=dict(arrowstyle='<-', color='k', shrinkA=0, shrinkB=0))

    xy0 = (25, 160.5)
    xy1 = (31.5, 30.5)
    ax1.annotate('Sensor4', xy0, xy1, arrowprops=dict(arrowstyle='<-', color='k', shrinkA=0, shrinkB=0))

# Configurações dos eixos
ax1.set_xticks([])
ax1.set_ylabel('Bytes', fontsize=16)
ax1.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax1.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
ax1.legend(loc='upper left', fontsize=12)
ax1.set_ylim(0, 250)

# Configurações finais
plt.title("Criptografia x Sem Criptografia", fontsize=18, fontweight="bold")
plt.tight_layout()
plt.savefig("comparacao.eps")
plt.show()
