class ByzantineDetector:
    def __init__(self, instant_threshold=1.8, cumulative_threshold=0.9, window_size=5):
        self.instant_threshold = instant_threshold
        self.cumulative_threshold = cumulative_threshold
        self.window_size = window_size
        self.anomaly_scores = defaultdict(lambda: deque(maxlen=window_size))
        self.malicious_nodes = set()
    
    def check_message(self, message):
        sender = message.sender
        anomaly_score = self._calculate_anomaly_score(message)
        
        # 更新异常分数记录
        self.anomaly_scores[sender].append(anomaly_score)
        
        # 瞬时阈值检测
        if anomaly_score > self.instant_threshold:
            self._handle_malicious(sender, 'instant')
            return False
        
        # 累积阈值检测
        if len(self.anomaly_scores[sender]) == self.window_size:
            avg_score = sum(self.anomaly_scores[sender]) / self.window_size
            if avg_score > self.cumulative_threshold:
                self._handle_malicious(sender, 'cumulative')
                return False
        
        return True
    
    def _calculate_anomaly_score(self, message):
        # 基于12个维度的行为指标计算异常分数
        score = 0
        if not message.valid:
            score += 0.5
        if message.delay > config.MAX_DELAY:
            score += 0.3
        if message.duplicate_signature:
            score += 1.0
        # 其他指标...
        return score
    
    def _handle_malicious(self, node_id, detection_type):
        if detection_type == 'instant':
            # 立即隔离
            self.malicious_nodes.add(node_id)
            self._trigger_view_change(node_id)
        else:
            # 渐进式降权
            self._reputation_penalty(node_id)
            self._audit_node(node_id)
    
    def is_malicious(self, node_id):
        return node_id in self.malicious_nodes