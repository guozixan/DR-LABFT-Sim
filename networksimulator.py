class NetworkSimulator:
    def __init__(self, num_nodes, byzantine_ratio):
        self.nodes = {}
        self.messages = []
        self.latency_model = LatencyModel()
        self.byzantine_ratio = byzantine_ratio
        
        # 创建节点
        byzantine_count = int(num_nodes * byzantine_ratio)
        for i in range(num_nodes):
            is_byzantine = (i < byzantine_count)
            node = Node(f"node_{i}", is_byzantine)
            node.connect_network(self)
            self.nodes[node.id] = node
    
    def broadcast(self, message):
        # 记录消息
        self.messages.append(message)
        
        # 模拟网络延迟
        latency = self.latency_model.get_latency(message.sender, message.destination)
        
        # 传递消息到所有目标节点（考虑拜占庭行为）
        for node_id, node in self.nodes.items():
            if message.destination == 'ALL' or message.destination == node_id:
                if node.is_byzantine and random.random() < 0.3:
                    # 拜占庭节点可能修改或丢弃消息
                    if random.choice([True, False]):
                        modified_msg = self._modify_message(message)
                        threading.Timer(latency, node.receive_message, [modified_msg]).start()
                else:
                    threading.Timer(latency, node.receive_message, [message]).start()
    
    def run_simulation(self, duration, tps):
        start_time = time.time()
        request_count = 0
        
        while time.time() - start_time < duration:
            # 生成交易请求
            if random.random() < tps / config.TPS_DIVISOR:
                node_id = random.choice(list(self.nodes.keys()))
                request = self._generate_request()
                self.nodes[node_id].start_request(request)
                request_count += 1
            
            # 处理节点消息
            for node in self.nodes.values():
                node.process_messages()
            
            time.sleep(config.SIMULATION_TICK)
        
        return self._collect_metrics(request_count)
    
    def _collect_metrics(self, total_requests):
        metrics = {
            'throughput': 0,
            'avg_latency': 0,
            'gini_index': self._calculate_gini(),
            'queue_status': {},
            'byzantine_detected': 0
        }
        
        # 收集性能指标...
        return metrics

class LatencyModel:
    def get_latency(self, sender, receiver):
        # 模拟网络延迟（基于地理分布）
        return random.uniform(0.05, 0.15)  # 50-150ms