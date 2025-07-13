class ReputationModel:
    def __init__(self, window_size=100, decay_factor=0.85):
        self.window_size = window_size
        self.decay_factor = decay_factor
        self.behavior_history = {}
        self.reputation_scores = {}
        self.metrics_weights = {
            'proposal_accept_rate': 0.15,
            'response_time_std': -0.12,
            'vote_consistency': 0.18,
            'invalid_signatures': -0.10,
            'resource_contribution': 0.20,
            'connectivity': 0.10,
            'behavior_deviation': -0.15
        }

    def update_behavior(self, node_id, message):
        if node_id not in self.behavior_history:
            self.behavior_history[node_id] = deque(maxlen=self.window_size)
        
        behavior = self._extract_behavior(message)
        self.behavior_history[node_id].append(behavior)
        self._calculate_reputation(node_id)

    def _extract_behavior(self, message):
        return {
            'timestamp': time.time(),
            'type': message.type,
            'response_time': message.response_time,
            'valid': message.valid,
            'resource_usage': message.resource_usage
        }

    def _calculate_reputation(self, node_id):
        behaviors = list(self.behavior_history[node_id])
        if not behaviors:
            self.reputation_scores[node_id] = 0.5
            return
        
        scores = {}
        # 计算各项指标得分
        scores['proposal_accept_rate'] = self._calc_accept_rate(behaviors)
        scores['response_time_std'] = self._calc_response_std(behaviors)
        # 其他指标计算...
        
        # 加权计算综合声誉
        weighted_sum = sum(scores[metric] * weight 
                          for metric, weight in self.metrics_weights.items())
        
        # 应用时间衰减
        prev_score = self.reputation_scores.get(node_id, 0.5)
        self.reputation_scores[node_id] = (
            self.decay_factor * weighted_sum + 
            (1 - self.decay_factor) * prev_score
        )

    def get_scores(self):
        return self.reputation_scores.copy()
    
    def reset_reputation(self, node_id):
        if node_id in self.reputation_scores:
            self.reputation_scores[node_id] = max(0.1, self.reputation_scores[node_id] * 0.5)