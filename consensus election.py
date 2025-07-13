class ElectionEngine:
    def __init__(self, alpha=1.2, beta=1.5, gamma=0.8):
        self.alpha = alpha  # 声誉激励指数
        self.beta = beta    # 负载惩罚系数
        self.gamma = gamma  # 公平调节系数
    
    def select_candidates(self, nodes, reputation_scores, 
                         min_reputation=0.65, max_load=0.8):
        candidates = []
        for node in nodes:
            reputation = reputation_scores.get(node.id, 0.5)
            load = node.get_current_load()
            
            if reputation >= min_reputation and load <= max_load:
                candidates.append(node)
        return candidates

    def elect_leader(self, candidates):
        if not candidates:
            return None
            
        weights = []
        gini = self._calculate_gini([c.reputation for c in candidates])
        
        for candidate in candidates:
            rep = candidate.reputation
            load = candidate.get_current_load()
            
            # 计算选举权重
            rep_factor = rep ** self.alpha
            load_penalty = math.exp(-self.beta * max(0, load - 0.7))
            fairness_adjust = math.exp(-self.gamma * gini)
            
            weight = rep_factor * load_penalty * fairness_adjust
            weights.append(weight)
        
        # 概率抽样
        total_weight = sum(weights)
        probabilities = [w / total_weight for w in weights]
        
        # 随机选择领导者
        return np.random.choice(candidates, p=probabilities).id

    def _calculate_gini(self, values):
        sorted_vals = sorted(values)
        n = len(sorted_vals)
        cum_values = np.cumsum(sorted_vals)
        return (n + 1 - 2 * np.sum(cum_values) / cum_values[-1]) / n