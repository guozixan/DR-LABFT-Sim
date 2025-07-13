class Node:
    def __init__(self, node_id, is_byzantine=False):
        self.id = node_id
        self.is_byzantine = is_byzantine
        self.consensus = DR_LABFT(node_id, self)
        self.network = None
        self.reputation = 0.8 if not is_byzantine else 0.3
        self.load = 0.0
        self.message_queue = deque()
    
    def connect_network(self, network):
        self.network = network
    
    def receive_message(self, message):
        if message.destination == self.id or message.destination == 'ALL':
            self.message_queue.append(message)
    
    def process_messages(self):
        while self.message_queue:
            message = self.message_queue.popleft()
            self.consensus.process_message(message)
    
    def send_message(self, message_type, data, destination='ALL'):
        message = Message(
            sender=self.id,
            destination=destination,
            type=message_type,
            data=data,
            timestamp=time.time()
        )
        self.network.broadcast(message)
    
    def start_request(self, request):
        self.consensus.start_consensus(request)
    
    def get_current_load(self):
        return min(1.0, len(self.message_queue) / config.QUEUE_LOAD_FACTOR)
    
    def malicious_behavior(self):
        if self.is_byzantine:
            # 拜占庭节点行为：随机选择一种攻击
            attack_type = random.choice([
                'double_spend', 'delay', 'invalid_signature', 'silent'
            ])
            # 执行攻击...