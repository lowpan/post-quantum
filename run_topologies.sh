#!/bin/bash

set -e

NUM_ITERATIONS=10
SCENARIOS=("no_cryptography" "rsa" "kyber")
TOPOLOGIES=(1 4 12)

LOG_DIR="log"
LOG_FILE="${LOG_DIR}/run_topologies.log"

mkdir -p "$LOG_DIR"

echo "Starting a new set of tests in: $(date)" > "$LOG_FILE"
echo "========================================================" >> "$LOG_FILE"

echo "========================================================"
echo "Starting automated test suite..."
echo "Number of iterations per scenario: ${NUM_ITERATIONS}"
echo "Scenarios: ${SCENARIOS[*]}"
echo "Topologies: ${TOPOLOGIES[*]}"
echo "Detailed output will be saved to: ${LOG_FILE}"
echo "========================================================"

for scenario in "${SCENARIOS[@]}"; do
    echo ""
    echo "--------------------------------------------------------"
    echo "STARTING SCENARIO: ${scenario}"
    echo "--------------------------------------------------------"

    for topo_id in "${TOPOLOGIES[@]}"; do
        echo "   --- STARTING Topology ${topo_id} ---"
        
        for i in $(seq 1 $NUM_ITERATIONS); do
            echo "      -> Running ${scenario} - Topology ${topo_id} - Iteration ${i}"
            
            {
                echo ""
                echo "--- LOG START: Scenario=${scenario}, Topology=${topo_id}, Iteration=${i} @ $(date) ---"
                sudo python3 network.py -s "${scenario}" -t "${topo_id}" -i "${i}" -b
                echo "--- LOG END: Run completed ---"
            } >> "$LOG_FILE" 2>&1

            echo "      -> Iteration ${i} completed."
            
            sleep 2
        done
        
        echo "   --- Topology ${topo_id} for ${scenario} completed. ---"

        if [[ "$topo_id" != "${TOPOLOGIES[-1]}" ]]; then
            echo "   Waiting 5 seconds before the next topology..."
            sleep 5
        fi
    done
    
    echo "--------------------------------------------------------"
    echo "SCENARIO ${scenario} COMPLETED."
    echo "--------------------------------------------------------"
done

echo ""
echo "========================================================"
echo "ALL TESTS AND ITERATIONS HAVE BEEN COMPLETED."
echo "Check the '${LOG_FILE}' file for detailed output."
echo "========================================================"
