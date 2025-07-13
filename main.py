from network.simulator import NetworkSimulator
import time
import json

def run_experiment(nodes, byzantine_ratio, tps, duration):
    print(f"Starting experiment: {nodes} nodes, {byzantine_ratio*100}% Byzantine, {tps} TPS")
    
    start_time = time.time()
    simulator = NetworkSimulator(nodes, byzantine_ratio)
    metrics = simulator.run_simulation(duration, tps)
    elapsed = time.time() - start_time
    
    print(f"Experiment completed in {elapsed:.2f}s")
    print(json.dumps(metrics, indent=2))
    
    return metrics

if __name__ == "__main__":
    # 基础场景实验
    run_experiment(nodes=20, byzantine_ratio=0.2, tps=150, duration=60)
    
    # 可扩展性实验
    for nodes in [10, 20, 30, 40]:
        run_experiment(nodes=nodes, byzantine_ratio=0.2, tps=150, duration=30)
    
    # 负载变化实验
    for tps in [50, 100, 150, 200]:
        run_experiment(nodes=20, byzantine_ratio=0.2, tps=tps, duration=30)