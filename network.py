#!/usr/bin/env python

import sys
import subprocess
import argparse 
from time import sleep

from containernet.net import Containernet
from containernet.node import DockerSensor
from containernet.cli import CLI
from containernet.energy import Energy as DockerEnergy

from mininet.log import info, setLogLevel
from mininet.term import makeTerm
from mn_wifi.energy import Energy as WifiEnergy
from mn_wifi.sixLoWPAN.link import LoWPAN

from topologies import *
from utils import docker_cp, get_crypto_args, get_kyber_keys, get_rsa_keys, set_parser

def set_topo(topo_id, net_obj, common_params, crypto_args_root, crypto_args_node):
    if topo_id == 1:
        return topology_1(net_obj, common_params, crypto_args_root, crypto_args_node)
    elif topo_id == 2:
        return topology_2(net_obj, common_params, crypto_args_root, crypto_args_node)
    elif topo_id == 3:
        return topology_3(net_obj, common_params, crypto_args_root, crypto_args_node)
    elif topo_id == 4:
        return topology_4(net_obj, common_params, crypto_args_root, crypto_args_node)
    elif topo_id == 5:
        return topology_5(net_obj, common_params, crypto_args_root, crypto_args_node)
    elif topo_id == 6:
        return topology_6(net_obj, common_params, crypto_args_root, crypto_args_node)
    elif topo_id == 7:
        return topology_7(net_obj, common_params, crypto_args_root, crypto_args_node)
    elif topo_id == 8:
        return topology_8(net_obj, common_params, crypto_args_root, crypto_args_node)
    elif topo_id == 9:
        return topology_9(net_obj, common_params, crypto_args_root, crypto_args_node)
    elif topo_id == 10:
        return topology_10(net_obj, common_params, crypto_args_root, crypto_args_node)
    elif topo_id == 11:
        return topology_11(net_obj, common_params, crypto_args_root, crypto_args_node)
    elif topo_id == 12:
        return topology_12(net_obj, common_params, crypto_args_root, crypto_args_node)
    else:
        info(f"*** Invalid topology ID: {topo_id}. Using default topology.\n")
        sensor1 = net_obj.addSensor('sensor1', ip6='fe80::1/64', dodag_root=True, **common_params, **crypto_args_root)
        sensor2 = net_obj.addSensor('sensor2', ip6='fe80::2/64', **common_params, **crypto_args_node)
        sensor3 = net_obj.addSensor('sensor3', ip6='fe80::3/64', **common_params, **crypto_args_node)
        sensor4 = net_obj.addSensor('sensor4', ip6='fe80::4/64', **common_params, **crypto_args_node)

        net_obj.configureNodes()

        info("*** Adding links\n")
        net_obj.addLink(sensor1, sensor2, cls=LoWPAN)
        net_obj.addLink(sensor2, sensor3, cls=LoWPAN)
        net_obj.addLink(sensor3, sensor4, cls=LoWPAN)

        info("*** Starting network\n")
        net_obj.build()
        return {"sensor1": sensor1, "sensor2": sensor2, "sensor3": sensor3, "sensor4": sensor4}

def topology():
    "Create a network."
    net = Containernet()
    dimage = 'ramonfontes/lowpan-post-quantum'
    scenario_name = "no_cryptography"
    iteration_num_str = 1
    
    # --- Argument Parsing with argparse --- #
    parser = set_parser()
    parsed_args = parser.parse_args(sys.argv[1:])

    scenario_name = parsed_args.scenario_name
    iteration_num_str = parsed_args.iteration_num
    batch_mode_active = parsed_args.batch
    topology_id_arg = parsed_args.topology_id
    output_file_base = f"{scenario_name}_{iteration_num_str}_{topology_id_arg}"

    info(f"*** Configuring scenario: {scenario_name}, iteration: {iteration_num_str}, topology: {topology_id_arg}\n")
    info(f"*** Output files base: {output_file_base}\n")

    args1, args2 = get_crypto_args(scenario_name)
    pcap_file_name_in_container = f"{output_file_base}.pcap"
    
    info("*** Configuring nodes\n")
    
    common_sensor_params = {
        'cls': DockerSensor, 'dimage': dimage, 'cpu_shares': 10,
        'volumes': ["/tmp/.X11-unix:/tmp/.X11-unix:rw"], # Para X11 forwarding
        'environment': {"DISPLAY": ":0"}, 'privileged': True, 'panid': '0xbeef',
        'voltage': 3.7, 'storing_mode': 2 # storing_mode=2 para todos como no seu exemplo
    }
    
    nodes: dict = set_topo(topology_id_arg, net, common_sensor_params, args1, args2)
    print( f"*** Nodes created: {nodes.keys()}\n")

    info("*** Configuring energy model\n")
    DockerEnergy(net.sensors)
    
    info("*** Configuring RPLD\n")
    net.configRPLD(net.sensors)
    
    if batch_mode_active: 
        container_name = "mn.sensor1"
        
        tcpdump_cmd = f"bash -c 'tcpdump -i sensor1-pan0 -w /{pcap_file_name_in_container} -v;'"
        makeTerm(nodes["sensor1"], title=f'sensor1_tcpdump_{scenario_name}_{iteration_num_str}', cmd=tcpdump_cmd)

        capture_duration = 60
        for t in range(0, capture_duration):
                print(f"\rCapturing... {t+1}/{capture_duration}s", end="", flush=True)
                sleep(1)

        print("\nStopping tcpdump...")
        subprocess.run(["docker", "exec", container_name, "killall", "-s", "SIGINT", "tcpdump"])
        
        sleep(1)

        print("\nSaving file to host...")
        pcap_file_on_host = f"./results/{output_file_base}.pcap"
        docker_cp(f"{container_name}:/{pcap_file_name_in_container}", pcap_file_on_host)
    else:
        info("*** Starting CLI\n")
        CLI(net)
    
    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
