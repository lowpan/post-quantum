from mininet.log import info, error, setLogLevel
from mn_wifi.sixLoWPAN.link import LoWPAN

setLogLevel('info')

def topology_1(net_obj, common_params, crypto_args_root, crypto_args_node):
    """
    1 
    |
    2
    """
    try:
        info("*** Creating topology:\n"
             " 1\n"
             " |\n"
             " 2\n")
        sensor1 = net_obj.addSensor('sensor1', ip6='fe80::1/64', dodag_root=True, **common_params, **crypto_args_root)
        sensor2 = net_obj.addSensor('sensorA', ip6='fe80::2/64', **common_params, **crypto_args_node)

        net_obj.configureNodes()

        info("*** Adding links\n")
        net_obj.addLink(sensor1, sensor2, cls=LoWPAN)

        info("*** Starting network\n")
        net_obj.build()
        return {"sensor1": sensor1, "sensor2": sensor2}
    except Exception as e:
        error(f"Failed to build star_topology_example: {e}\n")
        return None
    
def topology_2(net_obj, common_params, crypto_args_root, crypto_args_node):
    """
        1
        |
        2
       / \ 
      3   4
    """
    try:
        info("*** Creating topology:\n"
             "   1\n"
             "   |\n"
             "   2\n"
             "  / \\\n"
             " 3   4\n")
        sensor1 = net_obj.addSensor('sensor1', ip6='fe80::1/64', dodag_root=True, **common_params, **crypto_args_root)
        sensor2 = net_obj.addSensor('sensor2', ip6='fe80::2/64', **common_params, **crypto_args_node)
        sensor3 = net_obj.addSensor('sensor3', ip6='fe80::3/64', **common_params, **crypto_args_node)
        sensor4 = net_obj.addSensor('sensor4', ip6='fe80::4/64', **common_params, **crypto_args_node)

        net_obj.configureNodes()

        info("*** Adding links\n")
        net_obj.addLink(sensor1, sensor2, cls=LoWPAN)
        net_obj.addLink(sensor2, sensor3, cls=LoWPAN)
        net_obj.addLink(sensor2, sensor4, cls=LoWPAN)

        info("*** Starting network\n")
        net_obj.build()
        return {"sensor1": sensor1, "sensor2": sensor2, "sensor3": sensor3, "sensor4": sensor4}
    except Exception as e:
        error(f"Failed to build topology_2: {e}\n")
        return None
    
def topology_3(net_obj, common_params, crypto_args_root, crypto_args_node):
    """
    K1,4 (Star graph with 1 center, 4 leaves)
          A   B   
           \ /
            1
           / \
          C   D
    Node 1 is the center (root).
    Nodes A, B, C, D are leaves.
    """
    try:
        info("*** Creating topology: K1,4 (Star graph, 1 center, 4 leaves)\n"
             "    A---1---B\n"
             "       / \\\n"
             "      C   D\n")
        sensor1 = net_obj.addSensor('sensor1', ip6='fe80::1/64', dodag_root=True, **common_params, **crypto_args_root)
        sA = net_obj.addSensor('sA', ip6='fe80::10/64', **common_params, **crypto_args_node)
        sB = net_obj.addSensor('sB', ip6='fe80::11/64', **common_params, **crypto_args_node)
        sC = net_obj.addSensor('sC', ip6='fe80::12/64', **common_params, **crypto_args_node)
        sD = net_obj.addSensor('sD', ip6='fe80::13/64', **common_params, **crypto_args_node)

        net_obj.configureNodes()

        info("*** Adding links for K1,4\n")
        net_obj.addLink(sensor1, sA, cls=LoWPAN)
        net_obj.addLink(sensor1, sB, cls=LoWPAN)
        net_obj.addLink(sensor1, sC, cls=LoWPAN)
        net_obj.addLink(sensor1, sD, cls=LoWPAN)

        info("*** Starting network for K1,4 (calling build)\n")
        net_obj.build()
        return {"sensor1": sensor1, "sA": sA, "sB": sB, "sC": sC, "sD": sD, "description": "K1,4"}
    except Exception as e:
        error(f"Failed to build topology_3 (K1,4): {e}\n")
        return None

def topology_4(net_obj, common_params, crypto_args_root, crypto_args_node):
    """
    2x3 Grid (or C3 x P2)
    s11 -- s12 -- s13
     |      |      |
    s21 -- s22 -- s23
    s11 is the root.
    """
    try:
        info("*** Creating topology: 2x3 Grid\n"
             "    s11 -- s12 -- s13\n"
             "     |      |      |\n"
             "    s21 -- s22 -- s23\n")

        sensor1 = net_obj.addSensor('sensor1', ip6='fe80::1/64', dodag_root=True, **common_params, **crypto_args_root)
        s12 = net_obj.addSensor('s12', ip6='fe80::2/64', **common_params, **crypto_args_node)
        s13 = net_obj.addSensor('s13', ip6='fe80::3/64', **common_params, **crypto_args_node)
        s21 = net_obj.addSensor('s21', ip6='fe80::4/64', **common_params, **crypto_args_node)
        s22 = net_obj.addSensor('s22', ip6='fe80::5/64', **common_params, **crypto_args_node)
        s23 = net_obj.addSensor('s23', ip6='fe80::6/64', **common_params, **crypto_args_node)

        net_obj.configureNodes()

        info("*** Adding links for 2x3 Grid\n")
        net_obj.addLink(sensor1, s12, cls=LoWPAN)
        
        net_obj.addLink(s12, s13, cls=LoWPAN)
        net_obj.addLink(s21, s22, cls=LoWPAN)
        net_obj.addLink(s22, s23, cls=LoWPAN)
        
        net_obj.addLink(sensor1, s21, cls=LoWPAN)
        net_obj.addLink(s12, s22, cls=LoWPAN)
        net_obj.addLink(s13, s23, cls=LoWPAN)

        info("*** Starting network for 2x3 Grid (calling build)\n")
        net_obj.build()
        return {"sensor1": sensor1, "s12": s12, "s13": s13, "s21": s21, "s22": s22, "s23": s23, "description": "2x3 Grid"}
    except Exception as e:
        error(f"Failed to build topology_4 (2x3 Grid): {e}\n")
        return None

def topology_5(net_obj, common_params, crypto_args_root, crypto_args_node):
    """
    C5 (Cycle graph with 5 nodes)
        s1 -- s2
       /      \
      s5      s3
       \      /
        --s4--
    s1 is the root.
    """
    try:
        info("*** Creating topology: C5 (Cycle of 5 nodes)\n"
             "        s1 -- s2\n"
             "       /      \\\n"
             "      s5      s3\n"
             "       \\      /\n"
             "        --s4--\n")
        
        sensor1 = net_obj.addSensor('sensor1', ip6='fe80::1/64', dodag_root=True, **common_params, **crypto_args_root)
        s2 = net_obj.addSensor('s2', ip6='fe80::2/64', **common_params, **crypto_args_node)
        s3 = net_obj.addSensor('s3', ip6='fe80::3/64', **common_params, **crypto_args_node)
        s4 = net_obj.addSensor('s4', ip6='fe80::4/64', **common_params, **crypto_args_node)
        s5 = net_obj.addSensor('s5', ip6='fe80::5/64', **common_params, **crypto_args_node)

        net_obj.configureNodes()

        info("*** Adding links for C5\n")
        net_obj.addLink(sensor1, s2, cls=LoWPAN)
        net_obj.addLink(s2, s3, cls=LoWPAN)
        net_obj.addLink(s3, s4, cls=LoWPAN)
        net_obj.addLink(s4, s5, cls=LoWPAN)
        net_obj.addLink(s5, sensor1, cls=LoWPAN)

        info("*** Starting network for C5 (calling build)\n")
        net_obj.build()
        return {"sensor1": sensor1, "s2": s2, "s3": s3, "s4": s4, "s5": s5, "description": "C5"}
    except Exception as e:
        error(f"Failed to build topology_5 (C5): {e}\n")
        return None

def topology_6(net_obj, common_params, crypto_args_root, crypto_args_node):
    """
    K3 (Complete graph with 3 nodes - triangle)
      s1
     /  \
    s2 -- s3
    s1 is the root.
    """
    try:
        info("*** Creating topology: K3 (Triangle)\n"
             "        s1\n"
             "       /  \\\n"
             "      s2 -- s3\n")

        sensor1 = net_obj.addSensor('sensor1', ip6='fe80::1/64', dodag_root=True, **common_params, **crypto_args_root)
        s2 = net_obj.addSensor('s2', ip6='fe80::2/64', **common_params, **crypto_args_node)
        s3 = net_obj.addSensor('s3', ip6='fe80::3/64', **common_params, **crypto_args_node)

        net_obj.configureNodes()

        info("*** Adding links for K3\n")
        net_obj.addLink(sensor1, s2, cls=LoWPAN)
        net_obj.addLink(sensor1, s3, cls=LoWPAN)
        net_obj.addLink(s2, s3, cls=LoWPAN)

        info("*** Starting network for K3 (calling build)\n")
        net_obj.build()
        return {"sensor1": sensor1, "s2": s2, "s3": s3, "description": "K3"}
    except Exception as e:
        error(f"Failed to build topology_6 (K3): {e}\n")
        return None

def topology_7(net_obj, common_params, crypto_args_root, crypto_args_node):
    """
    K4 / C4 / 2x2 Grid (Square graph)
    s1 -- s2
    |    |
    s4 -- s3
    s1 is the root.
    """
    try:
        info("*** Creating topology: C4 (Square)\n"
             "      s1 -- s2\n"
             "      |    |\n"
             "      s4 -- s3\n")

        sensor1 = net_obj.addSensor('sensor1', ip6='fe80::1/64', dodag_root=True, **common_params, **crypto_args_root)
        s2 = net_obj.addSensor('s2', ip6='fe80::2/64', **common_params, **crypto_args_node)
        s3 = net_obj.addSensor('s3', ip6='fe80::3/64', **common_params, **crypto_args_node)
        s4 = net_obj.addSensor('s4', ip6='fe80::4/64', **common_params, **crypto_args_node)

        net_obj.configureNodes()

        info("*** Adding links for C4\n")
        net_obj.addLink(sensor1, s2, cls=LoWPAN)
        net_obj.addLink(s2, s3, cls=LoWPAN)
        net_obj.addLink(s3, s4, cls=LoWPAN)
        net_obj.addLink(s4, sensor1, cls=LoWPAN)

        info("*** Starting network for C4 (calling build)\n")
        net_obj.build()
        return {"sensor1": sensor1, "s2": s2, "s3": s3, "s4": s4, "description": "C4"}
    except Exception as e:
        error(f"Failed to build topology_7 (C4): {e}\n")
        return None

def topology_8(net_obj, common_params, crypto_args_root, crypto_args_node):
    """
    K2,3 (Complete bipartite graph)
    Group U (2 nodes): u1, u2
    Group V (3 nodes): v1, v2, v3
    u1 (root) is in Group U.
        u1          u2
       / | \      / | \
      v1 v2 v3  v1 v2 v3
    """
    try:
        info("*** Creating topology: K2,3 (Complete Bipartite)\n"
                "        u1          u2\n"
                "       / | \\      / | \\\n"
                "      v1 v2 v3  v1 v2 v3\n")

        sensor1 = net_obj.addSensor('sensor1', ip6='fe80::1/64', dodag_root=True, **common_params, **crypto_args_root)
        u2 = net_obj.addSensor('u2', ip6='fe80::2/64', **common_params, **crypto_args_node)

        v1 = net_obj.addSensor('v1', ip6='fe80::10/64', **common_params, **crypto_args_node)
        v2 = net_obj.addSensor('v2', ip6='fe80::11/64', **common_params, **crypto_args_node)
        v3 = net_obj.addSensor('v3', ip6='fe80::12/64', **common_params, **crypto_args_node)

        net_obj.configureNodes()

        info("*** Adding links for K2,3\n")
        net_obj.addLink(sensor1, v1, cls=LoWPAN)
        net_obj.addLink(sensor1, v2, cls=LoWPAN)
        net_obj.addLink(sensor1, v3, cls=LoWPAN)
        
        net_obj.addLink(u2, v1, cls=LoWPAN)
        net_obj.addLink(u2, v2, cls=LoWPAN)
        net_obj.addLink(u2, v3, cls=LoWPAN)

        info("*** Starting network for K2,3 (calling build)\n")
        net_obj.build()
        return {"sensor1": sensor1, "u2": u2, "v1": v1, "v2": v2, "v3": v3, "description": "K2,3"}
    except Exception as e:
        error(f"Failed to build topology_8 (K2,3): {e}\n")
        return None

def topology_9(net_obj, common_params, crypto_args_root, crypto_args_node):
    """
    F2 (Friendship graph F2, also called Bull graph or Bowtie/Hourglass)
    Two triangles sharing a common vertex.
      s2 -- s1 -- s4
       \  /  \  /
        s3    s5
    s1 is the central shared vertex and root.
    """
    try:
        info("*** Creating topology: F2 (Bowtie/Hourglass)\n"
             "        s2 -- s1 -- s4\n"
             "         \\  /  \\  /\n"
             "          s3    s5\n")

        sensor1 = net_obj.addSensor('sensor1', ip6='fe80::1/64', dodag_root=True, **common_params, **crypto_args_root)
        s2 = net_obj.addSensor('s2', ip6='fe80::2/64', **common_params, **crypto_args_node)
        s3 = net_obj.addSensor('s3', ip6='fe80::3/64', **common_params, **crypto_args_node)
        s4 = net_obj.addSensor('s4', ip6='fe80::4/64', **common_params, **crypto_args_node)
        s5 = net_obj.addSensor('s5', ip6='fe80::5/64', **common_params, **crypto_args_node)

        net_obj.configureNodes()

        info("*** Adding links for F2\n")
        net_obj.addLink(sensor1, s2, cls=LoWPAN)
        net_obj.addLink(sensor1, s3, cls=LoWPAN)
        net_obj.addLink(s2, s3, cls=LoWPAN)
        
        net_obj.addLink(sensor1, s4, cls=LoWPAN)
        net_obj.addLink(sensor1, s5, cls=LoWPAN)
        net_obj.addLink(s4, s5, cls=LoWPAN)
        
        info("*** Starting network for F2 (calling build)\n")
        net_obj.build()
        return {"sensor1": sensor1, "s2": s2, "s3": s3, "s4": s4, "s5": s5, "description": "F2 (Bowtie)"}
    except Exception as e:
        error(f"Failed to build topology_9 (F2): {e}\n")
        return None

def topology_10(net_obj, common_params, crypto_args_root, crypto_args_node):
    """
    W5 (Wheel graph with 5 outer vertices + 1 center = 6 nodes total)
    The image labels it W6, but visually it's W5.
    sC (center, root) connected to s1,s2,s3,s4,s5 which form a C5.
         s1--s2
        /|  /|
       sC--s3|
        \|/ |
         s5--s4
    """
    try:
        info("*** Creating topology: W5 (Wheel graph - 1 center, 5 outer)\n"
             "           s1--s2\n"
             "          /|  /|\n"
             "         sC--s3|\n"
             "          \\|/ |\n"
             "           s5--s4\n")

        sensor1 = net_obj.addSensor('sensor1', ip6='fe80::1/64', dodag_root=True, **common_params, **crypto_args_root)
        s1 = net_obj.addSensor('s1', ip6='fe80::2/64', **common_params, **crypto_args_node)
        s2 = net_obj.addSensor('s2', ip6='fe80::3/64', **common_params, **crypto_args_node)
        s3 = net_obj.addSensor('s3', ip6='fe80::4/64', **common_params, **crypto_args_node)
        s4 = net_obj.addSensor('s4', ip6='fe80::5/64', **common_params, **crypto_args_node)
        s5 = net_obj.addSensor('s5', ip6='fe80::6/64', **common_params, **crypto_args_node)

        net_obj.configureNodes()

        info("*** Adding links for W5\n")
        net_obj.addLink(sensor1, s1, cls=LoWPAN)
        net_obj.addLink(sensor1, s2, cls=LoWPAN)
        net_obj.addLink(sensor1, s3, cls=LoWPAN)
        net_obj.addLink(sensor1, s4, cls=LoWPAN)
        net_obj.addLink(sensor1, s5, cls=LoWPAN)
        
        net_obj.addLink(s1, s2, cls=LoWPAN)
        net_obj.addLink(s2, s3, cls=LoWPAN)
        net_obj.addLink(s3, s4, cls=LoWPAN)
        net_obj.addLink(s4, s5, cls=LoWPAN)
        net_obj.addLink(s5, s1, cls=LoWPAN)
        
        info("*** Starting network for W5 (calling build)\n")
        net_obj.build()
        return {"sensor1": sensor1, "s1": s1, "s2": s2, "s3": s3, "s4": s4, "s5": s5, "description": "W5"}
    except Exception as e:
        error(f"Failed to build topology_10 (W5): {e}\n")
        return None

def topology_11(net_obj, common_params, crypto_args_root, crypto_args_node):
    """
    C6 (Cycle graph with 6 nodes)
        s1 -- s2
       /        \
      s6        s3
       \        /
        s5 -- s4
    s1 is the root.
    """
    try:
        info("*** Creating topology: C6 (Cycle of 6 nodes)\n"
             "        s1 -- s2\n"
             "       /        \\\n"
             "      s6        s3\n"
             "       \\        /\n"
             "        s5 -- s4\n")
        
        sensor1 = net_obj.addSensor('sensor1', ip6='fe80::1/64', dodag_root=True, **common_params, **crypto_args_root)
        s2 = net_obj.addSensor('s2', ip6='fe80::2/64', **common_params, **crypto_args_node)
        s3 = net_obj.addSensor('s3', ip6='fe80::3/64', **common_params, **crypto_args_node)
        s4 = net_obj.addSensor('s4', ip6='fe80::4/64', **common_params, **crypto_args_node)
        s5 = net_obj.addSensor('s5', ip6='fe80::5/64', **common_params, **crypto_args_node)
        s6 = net_obj.addSensor('s6', ip6='fe80::6/64', **common_params, **crypto_args_node)

        net_obj.configureNodes()

        info("*** Adding links for C6\n")
        net_obj.addLink(sensor1, s2, cls=LoWPAN)
        net_obj.addLink(s2, s3, cls=LoWPAN)
        net_obj.addLink(s3, s4, cls=LoWPAN)
        net_obj.addLink(s4, s5, cls=LoWPAN)
        net_obj.addLink(s5, s6, cls=LoWPAN)
        net_obj.addLink(s6, sensor1, cls=LoWPAN)

        info("*** Starting network for C6 (calling build)\n")
        net_obj.build()
        return {"sensor1": sensor1, "s2": s2, "s3": s3, "s4": s4, "s5": s5, "s6": s6, "description": "C6"}
    except Exception as e:
        error(f"Failed to build topology_11 (C6): {e}\n")
        return None

def topology_12(net_obj, common_params, crypto_args_root, crypto_args_node):
    """
    3x3 Grid
    s11 -- s12 -- s13
     |      |      |
    s21 -- s22 -- s23
     |      |      |
    s31 -- s32 -- s33
    s11 is the root.
    """
    try:
        info("*** Creating topology: 3x3 Grid\n"
             "    s11 -- s12 -- s13\n"
             "     |      |      |\n"
             "    s21 -- s22 -- s23\n"
             "     |      |      |\n"
             "    s31 -- s32 -- s33\n")

        sensor1 = net_obj.addSensor('sensor1', ip6='fe80::1/64', dodag_root=True, **common_params, **crypto_args_root)
        sensor2 = net_obj.addSensor('sensor2', ip6='fe80::2/64', **common_params, **crypto_args_node)
        sensor3 = net_obj.addSensor('sensor3', ip6='fe80::3/64', **common_params, **crypto_args_node)
        sensor4 = net_obj.addSensor('sensor4', ip6='fe80::4/64', **common_params, **crypto_args_node)
        sensor5 = net_obj.addSensor('sensor5', ip6='fe80::5/64', **common_params, **crypto_args_node)
        sensor6 = net_obj.addSensor('sensor6', ip6='fe80::6/64', **common_params, **crypto_args_node)
        sensor7 = net_obj.addSensor('sensor7', ip6='fe80::7/64', **common_params, **crypto_args_node)
        sensor8 = net_obj.addSensor('sensor8', ip6='fe80::8/64', **common_params, **crypto_args_node)
        sensor9 = net_obj.addSensor('sensor9', ip6='fe80::9/64', **common_params, **crypto_args_node)

        net_obj.configureNodes()

        net_obj.addLink(sensor1, sensor2, cls=LoWPAN)
        net_obj.addLink(sensor1, sensor4, cls=LoWPAN)
        net_obj.addLink(sensor2, sensor3, cls=LoWPAN)
        net_obj.addLink(sensor2, sensor5, cls=LoWPAN)
        net_obj.addLink(sensor3, sensor6, cls=LoWPAN)
        
        net_obj.addLink(sensor4, sensor5, cls=LoWPAN)
        net_obj.addLink(sensor4, sensor7, cls=LoWPAN)
        net_obj.addLink(sensor5, sensor6, cls=LoWPAN)
        net_obj.addLink(sensor5, sensor8, cls=LoWPAN)
        net_obj.addLink(sensor6, sensor9, cls=LoWPAN)
        
        net_obj.addLink(sensor7, sensor8, cls=LoWPAN)
        net_obj.addLink(sensor8, sensor9, cls=LoWPAN)

        net_obj.build()
        return {"sensor1": sensor1, "sensor2": sensor2, "sensor3": sensor3, "sensor4": sensor4, "sensor5": sensor5, "sensor6": sensor6, "sensor7": sensor7, "sensor8": sensor8, "sensor9": sensor9}
    except Exception as e:
        error(f"Failed to build topology_12 (3x3 Grid): {e}\n")
        return None
