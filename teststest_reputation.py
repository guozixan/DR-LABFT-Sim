from consensus.reputation import ReputationModel
import time

def test_reputation_calculation():
    rep_model = ReputationModel()
    node_id = "node_1"
    
    # 初始声誉
    assert rep_model.get_scores().get(node_id, 0.5) == 0.5
    
    # 更新行为
    rep_model.update_behavior(node_id, {"valid": True, "response_time": 0.1})
    rep_model.update_behavior(node_id, {"valid": True, "response_time": 0.12})
    
    # 检查声誉提升
    score1 = rep_model.get_scores()[node_id]
    assert score1 > 0.5
    
    # 添加不良行为
    rep_model.update_behavior(node_id, {"valid": False, "response_time": 0.5})
    score2 = rep_model.get_scores()[node_id]
    assert score2 < score1
    
    # 测试重置
    rep_model.reset_reputation(node_id)
    assert rep_model.get_scores()[node_id] < 0.5 * score1

def test_malicious_detection():
    detector = ByzantineDetector()
    node_id = "malicious_node"
    
    # 发送一系列异常消息
    for _ in range(10):
        msg = {"valid": False, "delay": 0.3, "duplicate": True}
        if not detector.check_message(msg):
            break
    
    # 应检测到恶意节点
    assert detector.is_malicious(node_id)